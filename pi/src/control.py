#!/home/pi/.pyenv/shims/python

import readchar
from servo import servo_motor
import RPi.GPIO as GPIO

# constants
ANGLE_STEP = 5
DEFAULT_ANGLE = 90

GPIO_DRIVE_PIN = 17
DRIVE_FORWARD = True 
DRIVE_STOP = not DRIVE_FORWARD 

# init drive motor
GPIO.setmode(GPIO.BCM) 			# choose BCM to use GPIO numbers instead of pin numbers
GPIO.setup(GPIO_DRIVE_PIN, GPIO.OUT)    # change to output
GPIO.output(GPIO_DRIVE_PIN, DRIVE_STOP)

# init servo steering
s = servo_motor()
angle = DEFAULT_ANGLE 
s.spin(angle)

while True:
	keypress = readchar.readkey()

	if keypress == readchar.key.UP:
		GPIO.output(GPIO_DRIVE_PIN, DRIVE_FORWARD)
		print('Drive')

	if keypress == readchar.key.DOWN:
		GPIO.output(GPIO_DRIVE_PIN, DRIVE_STOP)
		print('Stop')

	if keypress == readchar.key.LEFT:
		print('Turn Left')
		angle += ANGLE_STEP
		s.spin(angle)

	if keypress == readchar.key.RIGHT:
		print('Turn Right')
		angle -= ANGLE_STEP
		s.spin(angle)

	if keypress == readchar.key.CTRL_C:
		print("Quit...")
		GPIO.output(GPIO_DRIVE_PIN, DRIVE_STOP)
		GPIO.cleanup()
		break
