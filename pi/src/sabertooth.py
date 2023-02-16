import RPi.GPIO as GPIO

class motor:
    def __init__(self):
        #self.GPIO_DRIVE_PIN = 17
        #self.DRIVE_FORWARD = True 
        #self.DRIVE_STOP = False

        # init drive motor
        GPIO.setmode(GPIO.BCM) 			# choose BCM to use GPIO numbers instead of pin numbers
        GPIO.setup(17, GPIO.OUT)    # change to output
        GPIO.output(17 , 0)
        print("setting up motor instance")

    def move(self):
        GPIO.output(17, 1)
        print("moving")
    
    def move(self, speed):
        if (speed >= 40):
            GPIO.output(17, 1)
            print("INFO: Moving at Speed 40")
        elif (speed >= 20):
            #Add new GPIO mode here
            print("INFO: Moving at Speed 20")
        else:
            GPIO.output(17, 0)
            print("INFO: Moving at Speed 0")

            

    def stop(self):
        GPIO.output(17, 0)
        print("stopped")


    
    def cleanup(self):
        GPIO.output(17, 0)
        GPIO.cleanup()
        print ("cleaning up")




