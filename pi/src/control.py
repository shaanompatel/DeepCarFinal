#!/home/pi/.pyenv/shims/python

import readchar
from servo import servo_motor
import RPi.GPIO as GPIO
import cv2
import time

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

# initialize camera
cam = cv2.VideoCapture(0)
cv2.namedWindow("Video Feed")

# start timer
capture_time = time.time()

while True:

	ret, frame = cam.read()
	if not ret:
		print("failed to grab frame")
		break
	cv2.imshow("Video Feed", frame)
	t = time.time()

	keypress = readchar.readkey()

	if keypress == readchar.key.UP:
		GPIO.output(GPIO_DRIVE_PIN, DRIVE_FORWARD)
		print('Drive')

	if keypress == readchar.key.DOWN:
		GPIO.output(GPIO_DRIVE_PIN, DRIVE_STOP)
		print('Stop')

	if keypress == readchar.key.LEFT:
		if (angle < 180 - ANGLE_STEP):
			print('Turn Left')
			angle += ANGLE_STEP
			s.spin(angle)
		else:
			print ("Staying at", str(angle))

	if keypress == readchar.key.RIGHT:
		if (angle > ANGLE_STEP):
			print('Turn Right')
			angle -= ANGLE_STEP
			s.spin(angle)
		else:
			print ("Staying at", str(angle))
	
	if (t - capture_time) > 1:
		img_name = "opencv_fram_{}.png".format(angle)
		cv2.imwrite(img_name, frame)
		print ("{} written!".format(img_name))
		capture_time = time.time()
			
	if keypress == readchar.key.CTRL_C:
		print("Quit...")
		GPIO.output(GPIO_DRIVE_PIN, DRIVE_STOP)
		s.spin(DEFAULT_ANGLE)
		GPIO.cleanup()
		break
