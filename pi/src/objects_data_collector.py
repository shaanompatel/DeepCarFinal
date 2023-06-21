#!/home/pi/.pyenv/shims/python
import readchar
from servo import servo_motor
from sabertooth import motor
import RPi.GPIO as GPIO
import cv2
import time
import os

# constants
ANGLE_STEP = 5
DEFAULT_ANGLE = 90
IMAGE_COUNT = 0
SPEED = 40

GPIO_DRIVE_PIN = 17
GPIO_DRIVE_SLOW_PIN = 16
DRIVE_FORWARD = True 
DRIVE_STOP = not DRIVE_FORWARD 
MOVING = False
SAVE_PATH = '/home/pi/deepcar/pi/objects_data'

# init drive motor
#GPIO.setmode(GPIO.BCM) 			# choose BCM to use GPIO numbers instead of pin numbers
#GPIO.setup(GPIO_DRIVE_PIN, GPIO.OUT)    # change to output
#GPIO.output(GPIO_DRIVE_PIN, DRIVE_STOP)

# init servo steering
s = servo_motor()
m = motor()
angle = DEFAULT_ANGLE 
s.spin(angle)

# initialize camera
cam = cv2.VideoCapture(0)
#cv2.namedWindow("Video Feed")

# start timer
capture_time = time.time()

while True:
	ret, frame = cam.read()
	if not ret:
		print("failed to grab frame")
		break
	#cv2.imshow("Video Feed", frame)
	t = time.time()

	keypress = readchar.readkey()

	if keypress == readchar.key.UP:
		#GPIO.output(GPIO_DRIVE_PIN, DRIVE_FORWARD)
		m.move(SPEED)
		MOVING = True
		print('Drive')

	if keypress == readchar.key.DOWN:
		#GPIO.output(GPIO_DRIVE_PIN, DRIVE_STOP)
		m.move(0)
		MOVING = False
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
		img_name = "opencv_fram_{}.jpg".format(IMAGE_COUNT)
		img_path = os.path.join(SAVE_PATH, img_name)
		cv2.imwrite(img_path, frame)
		print ("{} written!".format(img_name))
		IMAGE_COUNT += 1
		capture_time = time.time()
	
	if keypress == "1":
		SPEED = 20
		if MOVING:
			m.move(SPEED)
		#print("Moving at Speed {}".format(SPEED))
	
	if keypress == "2":
		SPEED = 40
		if MOVING:
			m.move(SPEED)
		#print("Moving at Speed {}".format(SPEED))


	if keypress == "q":
		print("Quit...")
		#GPIO.output(GPIO_DRIVE_PIN, DRIVE_STOP)
		m.move(0)
		m.cleanup()
		s.spin(DEFAULT_ANGLE)
		break
