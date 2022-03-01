#import RPi.GPIO as GPIO
import pigpio


class servo_motor ():
    def __init__(self):
        self.servo = 15
        self.servo2 = 18
        self.pwm = pigpio.pi() 
        self.pwm.set_mode(self.servo, pigpio.OUTPUT)
        self.pwm.set_mode(self.servo2, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency( self.servo, 50 )
        self.pwm.set_PWM_frequency( self.servo2, 50 )

    def spin(self, val):

        if (val < 0) or (val > 180):
            print ("Please Enter a Value Between 0 and 180")
        else:
            value = (val*11.1111111) + 500
            value2 = (((val+5)*11.1111111))+500
            self.pwm.set_servo_pulsewidth( self.servo, value)
            self.pwm.set_servo_pulsewidth( self.servo2, value2)

        return None

    
