import RPi.GPIO as GPIO

class motor:
    def __init__(self):
        #self.GPIO_DRIVE_PIN = 17
        #self.DRIVE_FORWARD = True 
        #self.DRIVE_STOP = False

        # init drive motor
        GPIO.setmode(GPIO.BCM) 			# choose BCM to use GPIO numbers instead of pin numbers
        GPIO.setup(17, GPIO.OUT)    # change to output
        GPIO.setup(22, GPIO.OUT)    # change to output
        GPIO.output(17 , 0)
        GPIO.output(22 , 0)
        print("INFO: Setting up Motor Instance")

    def move(self):
        GPIO.output(17, 1)
        print("INFO: Moving")
    
    def move(self, speed):
        if (speed >= 40):
            GPIO.output(22, 0)
            GPIO.output(17, 1)
            print("INFO: Moving at Speed 40")
        elif (speed >= 20):
            GPIO.output(17, 0)
            GPIO.output(22, 1)
            print("INFO: Moving at Speed 20")
        else:
            GPIO.output(17, 0)
            GPIO.output(22, 0)
            print("INFO: Moving at Speed 0")

    def stop(self):
        GPIO.output(17, 0)
        GPIO.output (22, 0)
        print("INFO: Stopping Car")

    def cleanup(self):
        GPIO.output(17, 0)
        GPIO.output(22, 0)
        GPIO.cleanup()
        print ("INFO: Cleaning up GPIO")




