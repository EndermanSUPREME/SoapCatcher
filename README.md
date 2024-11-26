# Soap Catcher
## Description
This assignment is focused on getting involved with Socket Servers to understand how the Transport Layer sends over the data and forms a connection. Along with seeing how the Application Layer handles sending and recieving the data. The setup involves a game being hosted on a Server where the player(s) are controlled through the connection of a Client.

## Project Assignment
<details>
<summary><strong>Instructions</strong></summary>

1. Using the code provided with the homework, and the pygame python library, continue
working on the client-server application of the “bucket catch” game.
2. The objective of the game is to collect as many falling objects as possible, similar to the
“bucket catch” game.
3. Rules of the game:
a. One bucket moves sideways (even up and down) to collect all falling objects.
b. Falling objects must be generated at random locations from the top of the screen
from the starting position on the X-axis.
c. Objects will fall faster as the game progresses.
d. Bucket also moves faster as the game progresses.
e. Player losses as soon as the first object touches the bottom of the screen.
4. A score must be displayed on the screen. No leaderboard is necessary.
5. GUI is not an important part of the homework, it is not necessary to implement any
visual elements outside of the basic elements to execute the game properly.
6. The server side will be in charge of displaying the game while the client side will be in
charge of the controls, you can set the controls to be with any keys from the keyboard,
preferable with the “WASD” or arrow keys.
7. Homework can be developed in pairs of two students, allowing for 2 people to work on
the 2 people’s project made specifically for 2 people and no less or more than 2 people.
8. The project will be evaluated during class time by the instructor and the grader together.
With students running the server and client side on two separate computers.
9. Project must be submitted to canvas as a .rar or .zip file containing all the source codes.

</details>

## To Build
If you want to run either client or server on Windows you must install [Python.exe](https://www.python.org/)
If you do not have Python installed on Unix run `sudo apt update && sudo apt install python3`
```bash
git clone https://github.com/EndermanSUPREME/SoapCatcher.git
```

## To Run
To start up the Game Server:<br>
`python GameServer.py`

To Connect to the Game Server as a Client:<br>
`python Client.py [GameServer IP] [GameSever Port]`

## How to Play
Once the Server detects the player has connected, the Play button will appear on the tkinter gui and you can play at your own leisure. The player uses the `WASD` keys to move around the gane canvas. The game objective is to `not drop the soap`. Bars of soap will periodically fall from the top of the game screen, catch as many bars of soap as you can. The game progressively gets more difficult by increasing the speed the soap falls at, as well as increasing the player speed.

### Preview Image
![Game_Preview_Image](https://github.com/user-attachments/assets/f86dc443-b307-40c5-99b0-90e99b3cb5bc)