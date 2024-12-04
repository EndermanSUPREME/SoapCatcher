import socket
import sys
import threading
import time
from pynput import keyboard

msgData = str("str")

def OnPress(key):
    global msgData
    try:
        if key == keyboard.Key.up:
            print("Up arrow key pressed")
            msgData = str("Up")
        elif key == keyboard.Key.down:
            print("Down arrow key pressed")
            msgData = str("Down")
        elif key == keyboard.Key.left:
            print("Left arrow key pressed")
            msgData = str("Left")
        elif key == keyboard.Key.right:
            print("Right arrow key pressed")
            msgData = str("Right")
    except Exception as e:
        print(f"Error: {e}")

def OnRelease(key):
    global msgData
    msgData = str("->")
    if key == keyboard.Key.esc:
        # Stop listener
        msgData = str("exit")
        return False

def Help():
    print(f"Usage: {sys.argv[0]} [IP] [PORT]")
    print("Enter no arguments for IP/PORT prompt input")
    exit()

def StartClient():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverIP = ""
    serverPORT = 0

    for a in sys.argv:
        if str(a) == "help" or str(a) == "--help" or str(a) == "-h":
            Help()

    if (len(sys.argv) != 3):
        serverIP = str(input("Enter Server IP >> "))
        serverPORT = int(input("Enter Server Port >> "))
    else:
        serverIP = str(sys.argv[1])
        serverPORT = int(sys.argv[2])

    try:
        clientsocket.connect((serverIP, serverPORT))

        # enter username on initial connection
        prompt = clientsocket.recv(64).decode()
        username = str(input(prompt))
        clientsocket.sendall(username.encode())

        print("Hold down the arrow keys. Press ESC to stop...")
        while True:
            global msgData
            if msgData == "exit":
                clientsocket.send(b'\n')
                print("[*] Killing Connection. . .")
                break
            clientsocket.send(msgData.encode())
            time.sleep(0.1)
    except Exception as e:
        print("Press ESC to kill Client...")
        print(f"Error: {e}")

def main():
    ClientThread = threading.Thread(target=StartClient, name='ClientThread')
    ClientThread.start()

    try:
        with keyboard.Listener(on_press=OnPress, on_release=OnRelease) as listener:
            listener.join()
    except Exception as e:
        print(f"Error: {e}")

    ClientThread.join()
    print("Client Program Ended")

if __name__ == "__main__":
    main()