# picar
Raspberry Pi controlled first-person view RC car

## Requirements
* Raspberry Pi
* RC car rewired with [L298N motor drive controller board](https://www.aliexpress.com/item/Free-Shipping-New-Dual-H-Bridge-DC-Stepper-Motor-Drive-Controller-Board-Module-L298N-MOTOR-DRIVER/32769190826.html) connected to motors
* Pi camera connected with ribbon cable
* Ultrasonic distance sensor ([HC-SR04](https://www.aliexpress.com/item/Free-shipping-1pcs-Ultrasonic-Module-HC-SR04-Distance-Measuring-Transducer-Sensor-for-Arduino-Samples-Best-prices/32640823431.html)) for rear object detection
* Web host with remote SQL access ([HelioHost](https://www.heliohost.org/) and [VimlyHost](https://vimlyhost.net/) are free ones)

## Installation
* Clone this repository to your Pi from https://github.com/t1m0thyj/picar.git
* Follow [the instructions on eLinux.org](https://elinux.org/RPi-Cam-Web-Interface#Installation_Instructions) to install the RPi Web Cam Interface 
* Run `sudo apt-get install python3-mysqldb` to install [MySQLdb for Python 3](https://packages.debian.org/stretch/python/python3-mysqldb)
* Create a *config.py* script in the same folder as *picar.py*, that defines the variables `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` for your online database
* If necessary, change the constants at the top of *picar.py* that specify what GPIO pins are used by the motor control board and ultrasonic sensor
* Upload the files in the *website* directory to your web host
* Create a MySQL database on your web host with columns "Name" and "Value", and add rows with the values ("Command", "") and ("IP", NULL)

## Usage
Run the script *picar.py* on your Pi, and load the website in your browser. The camera only works over a local network, because there would be too much latency if the stream was transmitted over the Internet.

To run the Python script automatically when the Pi boots, add this line to the file *~/.config/lxsession/LXDE-pi/autostart* (replace the path with the folder containing *picar.py*):

`@lxterminal -e python3 /home/pi/Desktop/picar.py`
