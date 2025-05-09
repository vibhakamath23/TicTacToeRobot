# TicTacToeRobot
Contains functional code and documentation for an Experiential Robotics Platform (XRP) Robot that can play a game of tic tac toe against a human user. Created as part of Tufts University's ME134 Robotics course in Spring 2025. 

Execution of this code requires running two separate workspaces: One to define communication between the XRP and an MQTT server, and another to connect to the Huskylens Camera and run game logic through this MQTT server. To begin, download the folders 'Camera & Game' and 'XRP & MQTT' separately into two workspace configs in VSCode with the MicroPico extension installed, and then follow the consequent directions to run each part respectively. 

# Components Required
- Huskylens Camera connected to computer through USB with camera mount
- XRP with functional [Gripper](https://www.printables.com/model/919002-xrp-robot-servo-arm-with-grippers/related) connected to computer through USB and battery powered
- 3 x 3 Tic Tac Toe board made of nine April tags

See the folder of images in `final_report.md` for positioning and setup of components before running.

Note that this README is oriented for users that are on macOS. If using another operating system, terminal commands will differ, and the `mqttconnect.py` file used for MQTT communication in 'Camera & Game' will need to be modified. 

# Part One: XRP & MQTT

Along with files to set up the MQTT server, this folder also contains `ServoCalibration.py`, which can be used to redefine the hardcoded degrees and angles used in the position functions in `XRP_MQTT.py`. This file allows for trial and error testing of the XRP + Gripper system to determine which degree values for each degree of freedom of the system (XRP base and arm joints) correspond to the orientation required for each space on the board. If using a different XRP system than the original in this project, first run the existing position functions, and if they do not line up properly with the spaces on the tic tac toe board being used, use the calibration file to find appropriate degree values. Secondly, `ServoCalibration.py` also contains code to individually control the gripper jaws of the XRP system, as this functionality is not integrated into game code for this implementation of the project. 

To begin with setting up the MQTT server, change the Wifi SSID and PW values in `config.txt` as appropriate in the MQTT folder, as well as the MQTT broker IP in `config.txt` and `mqttconnect.py`. You can also customize your `CLIENT_ID` in `mqttconnect.py`.

Next, make sure your Pico is connected through the MicroPico extension at the bottom of your VSCode terminal, and then run `XRP_MQTT.py` to connect to the server. A "Connection Successful!" message will print in terminal upon completion. 

Once this appears, MQTT Explorer or any other MQTT client can be used to publish integer messages to `topic/TicTacToePosition`, and the XRP should move to the appropriate orientation for each given position. 

`XRP_MQTT.py` also contains publishing testing code within an included `If False` block. To troubleshoot any issues with publishing, change this to `If True` and edit as needed.

# Part Two: Camera & Game

Once successful connection with the MQTT server has been established, the second part of execution is to set up the camera and run game logic. First, add your Wifi SSID and PW in `config.txt` in this folder's MQTT library as well, the same as in Part One. Next, add the same server address and client ID into `mqttconnect.py`. Note that this file looks different than the one in the 'XRP & MQTT' folder, as it does not work with the MicroPico library. 

Connect the Huskylens and determine which port it is using (if using MAC) with:

```bash
ls /dev/tty*
```
Replace this as the appropriate USB serial port for the camera at the top of the 'TicTacToeGame.py' file. 

Then run the file within terminal with: 

```bash
python3 TicTacToeGame.py
```
This should begin the game. As long as this is running concurrently with 'XRP_MQTT.py', the XRP will play a full game against a human opponent! 

