from servo import servo_motor
import time

s = servo_motor()

s.spin(40)
time.sleep(5)
s.spin(10)
time.sleep(5)
s.spin(90)