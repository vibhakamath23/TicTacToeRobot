from XRPLib.differential_drive import DifferentialDrive
from XRPLib.servo import Servo
from MQTT.mqttconnect import *

# Add SSID and PW in config.txt
# Add MQTT broker IP in config.txt and mqttconnect.py

drivetrain = DifferentialDrive.get_default_differential_drive()
servo1 = Servo.get_default_servo(1)
servo2 = Servo.get_default_servo(2)
c = connect_mqtt()
c.ping()

'''
POSITION FUNCTIONS FOR XRP
- These define hardcoded degree values for each of the degrees of freedom on the XRP to reach 
each of the nine tic tac toe board squares, plus a default position to start at and return to
    - Use the ServoCalibration.py file to determine these values through trial and error
- XRP will hold at each position for 2 seconds, then return to default 
'''
def default_position(angle):
    drivetrain.turn(0-angle) # uses current angle returned from below functions to return to 0
    servo1.set_angle(140)
    servo2.set_angle(0)
    print("At default position.")

def position_one():
    drivetrain.turn(10)
    servo1.set_angle(120)
    servo2.set_angle(0)
    print("At position 1.")
    time.sleep(2)
    default_position(10) # feed current angle as a parameter to allow calculation back to 0

def position_two():
    drivetrain.turn(10)
    servo1.set_angle(110)
    servo2.set_angle(0)
    print("At position 2.")
    time.sleep(2)
    default_position(10)

def position_three():
    drivetrain.turn(7)
    servo1.set_angle(85)
    servo2.set_angle(60)
    print("At position 3.")
    time.sleep(2)
    default_position(7)

def position_four():
    drivetrain.turn(0)
    servo1.set_angle(120)
    servo2.set_angle(0)
    print("At position 4.")
    time.sleep(2)
    default_position(0)

def position_five():
    drivetrain.turn(0)
    servo1.set_angle(100)
    servo2.set_angle(45)
    print("At position 5.")
    time.sleep(2)
    default_position(0)

def position_six():
    drivetrain.turn(0)
    servo1.set_angle(65)
    servo2.set_angle(60)
    print("At position 6.")
    time.sleep(2)
    default_position(0)

def position_seven():
    drivetrain.turn(-10)
    servo1.set_angle(120)
    servo2.set_angle(0)
    print("At position 7.")
    time.sleep(2)
    default_position(-10)

def position_eight():
    drivetrain.turn(-10)
    servo1.set_angle(100)
    servo2.set_angle(45)
    print("At position 8.")
    time.sleep(2)
    default_position(-10)

def position_nine():
    drivetrain.turn(-8)
    servo1.set_angle(85)
    servo2.set_angle(60)
    print("At position 9.")
    time.sleep(2)
    default_position(-8)

# Map MQTT messages to their corresponding positions
position_map = {
    b'0': default_position,
    b'1': position_one,
    b'2': position_two,
    b'3': position_three,
    b'4': position_four,
    b'5': position_five,
    b'6': position_six,
    b'7': position_seven,
    b'8': position_eight,
    b'9': position_nine
}

if False:  # Set to True for publishing testing, this will test all positions 1 - 9
    for i in range(0, 10):  
        print("about to publish", i)
        message = str(i).encode()  # message in bytes to match the key format
        c.publish("topic/TicTacToePosition", message, retain=True)
        print(f"Published: {message.decode()}")
        time.sleep(2)  # Give time between publishes to allow processing

else:  # subscribing, used for actual run of game
    def handle_message(topic, msg):
        try:
            print(f"Received message: {msg}")
            
            # Call the appropriate position function based on the message
            if msg in position_map:
                position_map[msg]()  # Call the function for the received position
            else:
                print(f"Invalid position message: {msg.decode()}")
                
        except Exception as e:
            print(f"Exception: {e}")
    
    c.set_callback(handle_message)
    c.subscribe("topic/TicTacToePosition")  # Subscribe to the topic for position messages

    while True:
        try:
            c.wait_msg()
        except Exception as e:
            print(f"Exception: {e}")


