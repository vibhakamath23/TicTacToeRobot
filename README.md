# TicTacToeRobot
Contains functional code and documentation for an Experiential Robotics Platform (XRP) Robot that can play a game of tic tac toe against a human user. Created as part of Tufts University's ME134 Robotics course in Spring 2025. 

Execution of this code requires running two separate workspaces: One to define communication between the XRP and an MQTT server, and another to connect to the Huskylens Camera and run game logic through this MQTT server. To begin, download the folders 'Camera & Game' and 'XRP & MQTT' separately into two workspace configs into VSCode with the MicroPico extension installed, and then follow the consequent directions to run each part respectively. 

# Components Required
- Huskylens Camera connected to computer through USB
- XRP and Gripper connected to computer through USB and battery powered

# PART ONE: XRP & MQTT

Note: Along with setting up the MQTT server, this folder also contains 'ServoCalibration.py', which can be used to redefine the hardcoded degrees and angles used in the position functions in 'XRP_MQTT.py'. This file allows for trial and error testing of the XRP + Gripper system to determine which degree values for each degree of freedom of the system (XRP base and arm joints) correspond to the orientation required for each space on the board. If using a different XRP system than the original in this project, first run the existing position functions, and if they do not line up properly with the spaces on the tic tac toe board being used, use the calibration file to find appropriate degree values.

To begin with setting up the MQTT server, add your Wifi SSID and PW in 'config.txt', and change the MQTT broker IP in 'config.txt' and 'mqttconnect.py' as appropriate. 

Next, run 'XRP_MQTT.py' through the MicroPico extension to connect to the server. A "Connection Successful!" message will print in terminal upon completion. 

Once this appears, MQTT Explorer can be used to publish integer messages to 'topic/TicTacToePosition', and the XRP should move to the appropriate orientation for each given position. This is all that needs to be run for this part.

'XRP_MQTT.py' also contains publishing testing code within an included 'If False' block. To troubleshoot any issues with publishing, change this to 'If True' and edit as needed.

# PART TWO: Camera & Game

Once successful connection with the MQTT server has been established, the second part of execution is to set up the camera and run game logic. Connect the Huskylens and determine which port (if using MAC) with:

```bash
ls /dev/tty*
```
Replace this as the appropriate USB serial port in the 'TicTacToeGame.py' file. 

Then run the file within terminal with: 

```bash
python3 TicTacToeGame.py
```
This should begin the game. As long as this is running concurrently with 'XRP_MQTT.py', the XRP will play a full game against a human opponent!

