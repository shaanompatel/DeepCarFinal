import RPi.GPIO as GPIO

class motor:
    def __init__(self):
        GPIO_DRIVE_PIN = 17
        DRIVE_FORWARD = True 
        DRIVE_STOP = not DRIVE_FORWARD 

         # init drive motor
        GPIO.setmode(GPIO.BCM) 			# choose BCM to use GPIO numbers instead of pin numbers
        GPIO.setup(GPIO_DRIVE_PIN, GPIO.OUT)    # change to output
        GPIO.output(GPIO_DRIVE_PIN, DRIVE_STOP)

    def move(self, direction)
        GPIO.output(GPIO_DRIVE_PIN, direction)
		print('Moving:', str(direction))
    
    def cleanup(self):
        GPIO.output(GPIO_DRIVE_PIN, False)
        GPIO.cleanup()




