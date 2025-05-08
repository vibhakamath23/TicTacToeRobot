from machine import Pin, PWM
import time
from time import sleep
from XRPLib.servo import Servo
from XRPLib.differential_drive import DifferentialDrive

'''
XRP + ARM CALIBRATION
- Use this code to determine the values required by the XRP + Gripper system
for each of the degrees of freedom (XRP, Arm Joint 1, Arm Joint 2).
- Designed for trial and error testing, allowing manual input for each degree
'''

# Get both servos
servo1 = Servo.get_default_servo(1)
servo2 = Servo.get_default_servo(2)

try:
    while True:
        DriveTrainangle = input("Enter angle between 180 and -180 for XRP to turn:")
        Servo1angle = input("Enter angle between 0 and 180 for servo 1: ")
        Servo2angle = input("Enter angle between 0 and 180 for servo 2: ")
        if Servo1angle.lower() == 'q':
            break
        try:
            Servo1angle = float(Servo1angle)
            Servo2angle = float(Servo2angle)
            DriveTrainangle = float(DriveTrainangle)
            if 0 <= Servo1angle <= 180 and 0 <= Servo2angle <= 180:
                drivetrain.turn(DriveTrainangle)
                servo1.set_angle(Servo1angle)
                servo2.set_angle(Servo2angle)
                print(f"Turned. both servos moved to their degrees.")
            else:
                print("Please enter a valid angle between 0 and 180.")
        except ValueError:
            print("Invalid input. Please enter a number.")

except KeyboardInterrupt:
    pass

# Optionally release both servos
servo1.free()
servo2.free()
drivetrain.set_speed(0,0)
print("Servos released.")




'''
GRIPPER CODE
- Use this code to control the gripper itself
- Can be run before tic tac toe game to hold pointer within gripper jaws
'''

Servo2 = Servo.get_default_servo(2)
Servo1 = Servo.get_default_servo(1)

try:
    while True:
        angle = input("Enter angle between 0 and 180 (or 'q' to quit): ")
        if angle.lower() == 'q':
            break
        try:
            angle = float(angle)
            if 0 <= angle <= 180:
                Servo1.set_angle(angle)
                Servo2.set_angle(-angle)
                print(f"Moved to {angle} degrees.")
            else:
                print("Please enter a valid angle between 0 and 180.")
        except ValueError:
            print("Invalid input. Please enter a number.")

except KeyboardInterrupt:
    pass
