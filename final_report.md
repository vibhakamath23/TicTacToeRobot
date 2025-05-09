# Problem

The chosen challenge of this project was to create a system using an XRP that could play at least one move of a tic tac toe exchange against a human opponent. 
The purpose of defining this goal was to gain more experience in dexterous control, precise movement on a small scale, and camera vision. 

**Required Components:**

- XRP needs to show autonomous behavior
- At least one camera
- MQTT server for robot-operator or robot-robot communication
- Multiple “stages”
- Have a human user input
- Use formal control methods such as state machines, behaviors-based control, or behavior trees
- Use some form of localization (e.g., line following, wall following, APRIL tag detection, forward kinematics, sensor fusion, etc.)

Beginning this project, baseline completion was defined as the system being able to grip some kind of pointer and play at least one valid move against a human player. This would be done by the XRP and the gripper moving to "point" to the square the robot desired to play in response to a starting human move.

# Approach

See this [Folder of Project Images](https://drive.google.com/drive/folders/1O4_QI9AdfXaA_f8W-MEcr27GEszFtbWz?usp=drive_link) for components and setup. 

This project works with an XRP serving as a rotating base, a 3D-printed gripper arm with two joints (so the system has three degrees of freedom overall), a lasercut tic tac toe board made of April tags, and a Huskylens Camera mounted above the board. 

Across two separate workspaces, this project works by using a single file for game logic ('TicTacToeGame.py') that uses an eye-in-the-sky camera constantly monitoring
the Tic Tac Toe board made of nine April Tags. As pieces are played and April tags are covered, this file translates this to a live in-code instantiation of the game board
and uses a tree-based Minimax algorithm to determine the best optimal move for the robot. This algorithm uses the order in which April tags are covered to differentiate between player moves and robot moves (the human opponent always goes first). 

Along with running the file with game logic, a second file must also be run concurrently to define movement for the XRP through an MQTT server ('XRP_MQTT.py'). This defines each of the nine orientations the XRP must move to in order to "point" at each of the nine spaces on the board to indicate a robot move. When integer messages 1-9 are sent to the MQTT server, the robot will move to this translated position (Position one is space (row,columm ; (0,0)) on the board, moving left to right across each row, top to bottom. So position nine is space (2,2)). Once this MQTT connection is defined and set up, the 'TicTacToeGame.y' uses the server to publish such integer messages as part of the game logic whenever the robot plays a move. 

# Results

This project was able to fulfill not only the outlined baseline completion state but achieve a stretch goal of playing an entire tic tac toe game against a human opponent through "pointing" at spaces. The human opponent plays for the robot (blue pieces) as well as their own moves (red pieces). The in-code representation of the board also prints in terminal as the game proceeds, updated with both robot and human moves for clarity in the case of robot malfunction or innacuracy. The game will not proceed or accept further moves unless the human opponent covers the correct space that the robot indicates. 

Note that in the main demo video, the gripper system is unplugged and inactive. The original goal was to have the gripper holding a "pointer" in the final state so it could indicate moves more clearly. However, a large blocker was the XRP board having only two servo ports, so only either the arm or the gripper system could be controlled at one time. An attempt was made to use an Arduino to control all four required servos and then run the Arduino through the XRP board using a UART connection. However, this caused highly irregular movement and presented numerous functional issues in integrating the XRP librairies with those of Arduino, and would also often cause either the servos, Arduino, or XRP board to overheat. Ultimately, the most successful and safest implementation was to run just the arm servos with nothing in the gripper jaws for a final demo. However, the gripper is fully functional on its own (a video of this also included at the end of the following demo link). A future implementation to improve this project would be to run with a different microcontroller entirely that supports four servos and XRP's dual motors at once, so the gripper could be used in all tests. This could help accomplish another stretch goal of the original project, which was to have a gripper that could actually place the robot's own pieces on the board rather than rely on the human opponent to place its moves.

[Demo Video Linked Here](https://youtu.be/_sDs2gQzWTI)

# Impact

Dexterous control, camera vision, and human-robot interaction as explored through this project are integral to many developing robotic fields, including medical (particularly surgical) robotics. The intention behind this work was to understand these topics on a deeper level to better conceptualize how they may be implemented in modern surgical systems.

In particular, surgical robotics relies heavily on the seamless coordination between sensing, real-time decision-making, and precise actuation, all of which were key elements in this project. Developing this tic tac toe robot required integrating computer vision with logic-based decision making, and then translating those decisions into physical, spatially accurate movements. These same capabilities are critical when, for example, a surgical robot must visually identify anatomical features, determine an optimal path for incision or manipulation, and execute that plan with millimeter-level precision.

Additionally, the implementation of a behavior-based control system using formal logic (e.g., state machines and tree structures like Minimax) mirrors the planning frameworks often used in surgical robotics to prioritize tasks, avoid collisions, and adapt to unpredictable environments. Even the use of MQTT to simulate surgeon-robot communication parallels real-world networked systems where robotic components must reliably exchange information with operators and auxiliary systems.

Though simplified, this project offered hands-on experience with the underlying principles of robotic autonomy and human-robot collaboration. By grappling with the mechanical limitations, integration challenges, and communication protocols, I gained valuable insights into the real-world engineering tradeoffs that influence the design of medical robotic systems – insights that could inform future work and creative problem-solving in the field.


