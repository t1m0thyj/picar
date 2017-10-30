#!/usr/bin/env python3
import subprocess
import time

import MySQLdb
import RPi.GPIO as GPIO

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

FORWARD_PIN = 29
BACKWARD_PIN = 31
LEFT_PIN = 33
RIGHT_PIN = 35
DEBUG = True

#---------------------------
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
TRIG = 38
ECHO = 40
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
time.sleep(2)


class PiCar:
    def __init__(self):
        self.conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME,
                                    autocommit=True)
        self.motor1_state = 0  # Motor that drives forward or backward
        self.motor2_state = 0  # Motor that turns left or right
        self.command_history = []
        self.stop_button_pressed = False

        hostname = subprocess.check_output(["hostname", "-I"]).split()
        ipv4 = [ip for ip in hostname if b":" not in ip][-1]
        with self.conn.cursor() as cur:
            cur.execute("UPDATE PiCar SET Value=%s WHERE Name='IP'", (ipv4,))

    def __del__(self):
        self.stop_button_pressed = True
        self.conn.close()
    
    def initialize(self):
        self.last_command = ""
        while self.last_command != "y":
            self.get_command()
        self.read_commands()

    def get_command(self):
        command = self.last_command
        with self.conn.cursor() as cur:
            while command == self.last_command:
                self.last_command = command
                cur.execute("SELECT Value FROM PiCar WHERE Name='Command'")
                command = cur.fetchone()[0]
                distance = self.get_distance()
                if distance > 0 and distance < 50:
                    print("Distance from rear: %d" % distance)
                    command += "@"
        if DEBUG:
            print(command)
        self.last_command = command
        return command
    
    def get_distance(self):
        GPIO.output(TRIG, True)
        time.sleep(0.00001)      # Start/begin/commence measuring distance
        GPIO.output(TRIG, False)

        start = time.time()
        pulse_start = 0
        while time.time() - start < 0.1:
            if GPIO.input(ECHO) == True:
                pulse_start = time.time()
                break
            time.sleep(0.0001)

        pulse_end = 0
        while time.time() - start < 0.1:
            if GPIO.input(ECHO) == False:
                pulse_end = time.time()
                break
            time.sleep(0.0001)

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150
        #print(round(distance, 2))

        return round(distance, 2)

    def read_commands(self):
        stopped = False
        while not self.stop_button_pressed:
            command = self.get_command()
            if len(self.command_history) > 0:
                self.command_history[-1][1] = time.time() - self.command_history[-1][1]

            if command != "r":
                self.command_history.append([command, time.time()])
                self.update_motor_states(command)
                self.update_gpio()
                if command == "x":
                    stopped = True
                    break
            else:
                self.autopilot()
        if stopped:
            self.initialize()

    def update_motor_states(self, command, autopilot=False):
        self.motor1_state = 0
        self.motor2_state = 0
        
        if ("w" in command and "s" in command) or ("w" not in command and "s" not in command):
            pass
            # same as default (0)
            # self.command_history[-1][0] = self.command_history[-1][0].replace("w", "").replace("s", "")
        elif "w" in command:
            self.motor1_state = 1
        elif "s" in command and (not "@" in command):
            self.motor1_state = -1

        if ("a" in command and "d" in command) or ("a" not in command and "d" not in command):
            pass
            # same as default (0)
            # self.command_history[-1][0] = self.command_history[-1][0].replace("a", "").replace("d", "")
        elif "a" in command:
            self.motor2_state = -1
        elif "d" in command:
            self.motor2_state = 1

        if autopilot:
            self.motor1_state *= -1
            #self.motor2_state *= -1

        if DEBUG:
            print("M1: %d, M2: %d" % (self.motor1_state, self.motor2_state))

    def update_gpio(self):
        if self.motor1_state == 1:
            GPIO.output(FORWARD_PIN, 1)
            GPIO.output(BACKWARD_PIN, 0)
        elif self.motor1_state == 0:
            GPIO.output(FORWARD_PIN, 0)
            GPIO.output(BACKWARD_PIN, 0)
        elif self.motor1_state == -1:
            GPIO.output(FORWARD_PIN, 0)
            GPIO.output(BACKWARD_PIN, 1)

        if self.motor2_state == 1:
            GPIO.output(LEFT_PIN, 0)
            GPIO.output(RIGHT_PIN, 1)
        elif self.motor2_state == 0:
            GPIO.output(LEFT_PIN, 0)
            GPIO.output(RIGHT_PIN, 0)
        elif self.motor2_state == -1:
            GPIO.output(LEFT_PIN, 1)
            GPIO.output(RIGHT_PIN, 0)

    def autopilot(self):
        print(self.command_history)
        while len(self.command_history) > 0:
            command = self.command_history[-1]
            self.update_motor_states(command[0], True)
            self.update_gpio()
            if DEBUG:
                print("%s, %.2f" % (command[0], command[1]))
            self.command_history.remove(command)  # needs work
            if command[0]:
                time.sleep(command[1])  # needs work
        self.motor1_state = 0
        self.motor2_state = 0


def main():
    if DEBUG:
        print("Welcome to the Pi Car Connection Service!")

    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setwarnings(False)
    for pin in (FORWARD_PIN, BACKWARD_PIN, LEFT_PIN, RIGHT_PIN):
        GPIO.setup(pin, GPIO.OUT)

    car = PiCar()
    car.initialize()


if __name__ == "__main__":
    main()
