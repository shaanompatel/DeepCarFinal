from servo import servo_motor
import cv2
import time
import readchar
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)

s = servo_motor()
angle = 90
s.spin(90)

#cam = cv2.VideoCapture(0)
# aaaaaaaaaaaaaaaaaaaacv2.namedWindow("test")

# start timer
#capture_time = time.time()

while True:
    #ret, frame = cam.read()
    # if not ret:
    #print("failed to grab frame")
    # break
    #cv2.imshow("test", frame)
    t = time.time()
    #print("Input: ")
    if repr(readchar.readchar()) == "'d'":
        angle += 5
        s.spin(angle)
    if repr(readchar.readchar()) == "'a'":
        angle -= 5
        s.spin(angle)
    if repr(readchar.readchar()) == "'f'":
        GPIO.output(27, 1)
        print("starting motor")
    if repr(readchar.readchar()) == "'s'":
        GPIO.output(27, 0)
        print ("stopping motor")
    if repr(readchar.readchar()) == "'g'":
        break
    # if (t - capture_time) > 10000000:
    #img_name = "opencv_frame_{}.png".format(angle)
    #cv2.imwrite(img_name, frame)
    #print("{} written!".format(img_name))

    #capture_time = time.time()
GPIO.output(27, 0)
GPIO.cleanup()
