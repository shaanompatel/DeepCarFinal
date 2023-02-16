from sabertooth import motor
import time

m = motor()

motor.move()
print ("moving")
time.sleep(2)
 
motor.stop()
print ("stopped")
time.sleep(2)



motor.cleanup()