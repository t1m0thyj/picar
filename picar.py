#!/usr/bin/env python3
import socket
import time

import MySQLdb
import RPi.GPIO as GPIO

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

DEBUG = True
FORWARD_PIN = 29
BACKWARD_PIN = 31
LEFT_PIN = 33
RIGHT_PIN = 35
TRIG_PIN = 38
ECHO_PIN = 40


class PiCar:
    def __init__(self):
        self.conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME,
                                    autocommit=True)
        self.motor1_state = 0  # Motor that drives forward or backward
        self.motor2_state = 0  # Motor that turns left or right
        self.command_history = []
        self.rear_blocked = False
        self.stop_button_pressed = False

        self.pwm_f = GPIO.PWM(FORWARD_PIN, 1000)
        self.pwm_f.start(0)
        self.pwm_b = GPIO.PWM(BACKWARD_PIN, 1000)
        self.pwm_b.start(0)

        ipv4 = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        with self.conn.cursor() as cur:
            cur.execute("UPDATE PiCar SET Value=%s WHERE Name='IP'", (ipv4,))
    
    def initialize(self):
        self.last_command = ""
        while self.last_command != "y":
            self.get_command()
        self.read_commands()
    
    def quit(self):
        self.stop_button_pressed = True
        self.conn.close()
        GPIO.cleanup()

    def get_command(self):
        command = self.last_command
        rear_blocked = self.rear_blocked
        with self.conn.cursor() as cur:
            while command == self.last_command and rear_blocked == self.rear_blocked:
                self.last_command = command
                self.rear_blocked = rear_blocked
                cur.execute("SELECT Value FROM PiCar WHERE Name='Command'")
                command = cur.fetchone()[0]
                distance = self.get_distance()
                self.rear_blocked = 0 < distance < 50
                if DEBUG and self.rear_blocked:
                    print("Ping: %d cm" % distance)
        if DEBUG and len(command):
            print(command)
        self.last_command = command
        return command
    
    def get_distance(self):
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)  # Start measuring distance
        GPIO.output(TRIG_PIN, False)
        start = time.time()

        pulse_start = 0
        while time.time() - start < 0.1:
            if GPIO.input(ECHO_PIN) == True:
                pulse_start = time.time()
                break
            time.sleep(0.0001)

        pulse_end = 0
        while time.time() - start < 0.1:
            if GPIO.input(ECHO_PIN) == False:
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
                self.update_gpio(command)
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
        elif "s" in command and (not self.rear_blocked):
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

    def update_gpio(self, command):
        speed = 100
        if "," in command:
            speed = int(command.split(",")[1])

        if self.motor1_state == 1:
            self.pwm_f.ChangeDutyCycle(speed)
            self.pwm_b.ChangeDutyCycle(0)
        elif self.motor1_state == 0:
            self.pwm_f.ChangeDutyCycle(0)
            self.pwm_b.ChangeDutyCycle(0)
        elif self.motor1_state == -1:
            self.pwm_f.ChangeDutyCycle(0)
            self.pwm_b.ChangeDutyCycle(speed)

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

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for pin in (FORWARD_PIN, BACKWARD_PIN, LEFT_PIN, RIGHT_PIN, TRIG_PIN):
        GPIO.setup(pin, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)
    time.sleep(2)

    try:
        car = PiCar()
        car.initialize()
    finally:
        car.quit()


if __name__ == "__main__":
    main()
