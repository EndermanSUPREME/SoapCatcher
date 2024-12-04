import pygame, threading, socket, random, time
import tkinter as tk
from tkinter import messagebox

hostname = ""
IPAddr = ""
PORT = 8888
RUNNING = True
RUNGAME = False
PLAYERCONNECTED = False
KILLPROGRAM = False
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
root = tk.Tk()

# only pack once so we dont overlap packing causing display issues
usernameList = tk.Label(root, text="")
usernameList.pack(pady=10)

class Player:
    def __init__(self,connection,address,x,y):
        self.connection = connection
        self.address = address
        self.x = x
        self.y = y
        self.size = 0
        self.username = ""
        self.icon = pygame.image.load("hands_.png")
        self.recvBuffer = b''

    def SetUsername(self,name:str):
        self.username = name
    def GetUsername(self):
        return self.username

    def GetPosX(self):
        return self.x
    def GetPosY(self):
        return self.y
    def SetPosX(self,x):
        self.x = x
    def SetPosY(self,y):
        self.y = y
        
    def GetSize(self):
        return self.size
    def SetSize(self,size):
        self.size = size
    def GetPlayerIcon(self):
        return self.icon
    def SetPlayerIcon(self,img):
        self.icon = img

    def GetRecvBuffer(self):
        return self.recvBuffer
    def SetRecvBuffer(self,recvBuffer):
        self.recvBuffer = recvBuffer

    def GetConnection(self):
        return self.connection
    def GetAddress(self):
        return self.address

class FallingParticle:
    def __init__(self, x, y):
        self.x = x  # Set the x position
        self.y = y  # Set the y position
        
    def SetPosX(self, x):
        self.x = x

    def SetPosY(self, y):
        self.y = y

    def GetPosX(self):
        return self.x

    def GetPosY(self):
        return self.y
    
ConnectedPlayers = []

def GetNetworkIP():
    try:
        # Create a dummy socket connection to get the IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to a public IP (it doesn't have to be reachable)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"Error: {e}")
        return None

# Check at runtime if the player has connected
# when the player connects we then allow the
# button responsible to run the game be available
def ViewConnection():
    global root,PLAYERCONNECTED

    if PLAYERCONNECTED:
        sbutton = tk.Button(root, text="Start", command=ReadyGame)
        sbutton.pack(pady=10)  # Add some vertical padding
    else:
        root.after(100, ViewConnection)

def DisplayPlayers():
    global root,ConnectedPlayers,usernameList

    # Display connected users to the handler tkinter window
    usernames = ""
    for players in ConnectedPlayers:
        usernames = usernames + f"{players.GetUsername()}\n"

    names=f"Connected Players:\n{usernames}"
    usernameList.config(text=names)

    root.after(100, DisplayPlayers)

def GameStatus():
    global root,RUNNING,rbutton,flabel

    if RUNNING == False:
        rbutton = tk.Button(root, text="Retry", command=ReadyGame)
        rbutton.pack(pady=10)  # Add some vertical padding
        
        flabel = tk.Label(root, text="Oh nyo, yuwu wowst! >w<")
        flabel.pack()
    else:
        rbutton.destroy()
        flabel.destroy()
        root.after(100, GameStatus)

def ServerHandle():
    global root,RUNNING
    root.title("Server Panel")

    label = tk.Label(root, text="Server Controls")
    label.pack()

    # Create a button and add it to the window
    ebutton = tk.Button(root, text="Shutdown", command=ServerShutDown)
    ebutton.pack(pady=10)  # Add some vertical padding

    root.geometry("200x200")

    ViewConnection()
    DisplayPlayers()
    GameStatus()

    root.mainloop()

def ConnectClient(connection, address, PlayerData):
    global PLAYERCONNECTED,KILLPROGRAM
    try:
        if RUNNING:
            print(f"[+] Incoming Connection from {address}\n")

            # Get player name from connected client
            msg = "Enter Username > "
            connection.sendall(msg.encode())
            playerUsername = connection.recv(12).decode()
            PlayerData.SetUsername(playerUsername)

            PLAYERCONNECTED = True
            # Handle Single Connection
            while KILLPROGRAM == False:
                recvBuffer = connection.recv(64) # size of recv bytes we allow
                PlayerData.SetRecvBuffer(recvBuffer)

                if KILLPROGRAM == True:
                    break

                if len(recvBuffer) > 0:
                    if recvBuffer.decode() == "\n":
                        print(f"{address} has Disconnected")
                        # remove player session on disconnection
                        for player in ConnectedPlayers:
                            if player.GetAddress() == address:
                                ConnectedPlayers.remove(player)
                        break
                    if recvBuffer.decode() != "str":
                        print(f"Recv -> {address} | {recvBuffer.decode()}")
    except Exception as e:
        print(f"Error: {e}")

def RunServer():
    try:
        global hostname,IPAddr,PORT
        global serversocket,RUNNING,PLAYERCONNECTED
        global KILLPROGRAM,RUNGAME,ConnectedPlayers

        PlayerThreads = []

        hostname = socket.gethostname()
        IPAddr = GetNetworkIP()
        PORT = 8888

        print(f"Your Computer Name is: {hostname}")
        print(f"Your Computer IP Address is: {IPAddr}")

        serversocket.bind((str(IPAddr), PORT))
        serversocket.listen(10) # queue connections
        print(f"[+] Server Active | {IPAddr}:{PORT}\n")

        print("[*] Listening for Players. . .")
        while RUNNING:
            connection, address = serversocket.accept()

            # Dont allow connections while the game is running
            if RUNGAME:
                connection.sendall(b"Connection Denied: Game is in Progress.")
                connection.close()
            else:
                PlayerSession = Player(connection,address,0,0)
                playerThread = threading.Thread(target=ConnectClient,args=[connection,address,PlayerSession])
                ConnectedPlayers.append(PlayerSession)
                PlayerThreads.append(playerThread)
                playerThread.start()

        # Close connection to all players
        for p in ConnectedPlayers:
            p.GetConnection().close()

        # Ensure all the player threads have ended
        for t in PlayerThreads:
            t.join()
        
    except Exception as e:
        print(f"Error: {e}")

def BucketGame():
    try:
        global RUNNING,RUNGAME,root,ConnectedPlayers

        # Initialize Pygame
        pygame.init()

        RUNGAME = True

        # Set up the display
        window_width, window_height = 800, 600
        screen = pygame.display.set_mode((window_width, window_height))
        font = pygame.font.Font(None, 36)
        playerTagFont = pygame.font.Font(None, 24)
        pygame.display.set_caption("Ender's Bucket Game")

        # Define colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        UN = (100, 50, 100)

        # Setup All Players
        # Player properties
        square_size = 50
        x = window_width // 2 - square_size // 2
        y = window_height // 2 - square_size // 2
        speed = 2
        playerImg = pygame.image.load("hands_.png")
        playerImg = pygame.transform.scale(playerImg, (square_size, square_size))

        for p in ConnectedPlayers:
            p.SetPosX(x + random.randrange(square_size // 2, window_width - (square_size // 2)))
            p.SetPosY(y)
            p.SetSize(square_size)
            p.SetPlayerIcon(playerImg)

        # Falling Particle properties
        fallingParticleSize = 50
        fallSpeed = 1
        particle_image = pygame.image.load("soap_.png")
        particle_image = pygame.transform.scale(particle_image, (fallingParticleSize, fallingParticleSize))
        FallingParticles = []

        # Extra
        Duration = 5 # Set the duration to wait (in seconds)
        DiffcultyTimer = 30 # Set the duration to wait (in seconds)
        Chance = 80 # Set the duration to wait (in seconds)
        sTime = time.time() # Record the start time
        gTime = time.time() # Record the global start time
        Points = 0

        # Main game loop
        while RUNNING:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUNNING = False  # Exit the loop if the window is closed
                    RUNGAME = False  # Allow new players to join the next game session

            # End game when no players exist
            if len(ConnectedPlayers) == 0:
                RUNNING = False  # Exit the loop if the window is closed
                RUNGAME = False  # Allow new players to join the next game session

            # Everything we want happening during gameplay
            # occurs below this point

            cTime = time.time()
            if cTime - gTime >= DiffcultyTimer:
                fallSpeed = fallSpeed + 1
                speed = speed + 1
                if Duration > 2:
                    Duration = Duration - 1
                if Chance > 15:
                    Chance = Chance - 5
                gTime = cTime

            # Fill the screen with a color (RGB)
            screen.fill(BLACK)  # Clear to draw next Frame

    #=======================================================
    #       RANDOM PARTICLE SPAWN
            cTime = time.time()
            if random.randint(0, 100) > Chance and cTime - sTime >= Duration:
                # spawn in the number of particles as there are players
                for i in range(0,len(ConnectedPlayers)):
                    FallingParticles.append(FallingParticle(random.randint(0, window_width - fallingParticleSize), 5))

                sTime = cTime

            # Points Display
            ScoreText = font.render(f"Score: {Points}", True, WHITE)
            screen.blit(ScoreText, (10, 10))

            for p in FallingParticles:
                if p.GetPosY() >= window_height:
                    RUNNING = False
                    RUNGAME = False
                    pygame.quit()

                fallPos = p.GetPosY() + fallSpeed
                p.SetPosY(fallPos)

                for PlayerSession in ConnectedPlayers:
                    player = pygame.Rect(PlayerSession.GetPosX(), PlayerSession.GetPosY(), PlayerSession.GetSize(), PlayerSession.GetSize())
                    particleSubject = pygame.Rect(p.GetPosX(), p.GetPosY(), fallingParticleSize, fallingParticleSize)

                    # Catch falling object
                    if player.colliderect(particleSubject):
                        FallingParticles.remove(p)
                        Points = Points + 1
                        ScoreText = font.render(f"Score: {Points}", True, WHITE)
                        screen.blit(ScoreText, (10, 10))
                    else:
                        # pygame.draw.rect(screen, RED, particleSubject)
                        screen.blit(particle_image, (p.GetPosX(), p.GetPosY()))

    #=======================================================

    #=======================================================
    #       PLAYER MOVEMENT

            # Track all Player Movement
            for p in ConnectedPlayers:
                y = p.GetPosY()
                x = p.GetPosX()

                if p.GetRecvBuffer().decode() == "Up":
                    y -= speed
                if p.GetRecvBuffer().decode() == "Down":
                    y += speed
                if p.GetRecvBuffer().decode() == "Left":
                    x -= speed
                if p.GetRecvBuffer().decode() == "Right":
                    x += speed

                # Keep the square within the window boundaries
                x = max(0, min(window_width - square_size, x))
                y = max(window_height/2, min(window_height - square_size, y))

                p.SetPosX(x)
                p.SetPosY(y)

                # Draw the player
                # pygame.draw.rect(screen, WHITE, (x, y, square_size, square_size))
                screen.blit(p.GetPlayerIcon(), (x, y))

                # Render player name
                playerName = playerTagFont.render(p.GetUsername(), True, WHITE)
                screen.blit(playerName, (x - playerName.get_size()[0], y + square_size))
    #=======================================================

            # Update the display
            pygame.display.flip()

            # Control the frame rate
            pygame.time.Clock().tick(60)

        # Clean up and close the window
        RUNGAME = False
        pygame.quit()
    except:
        return None

def ServerShutDown():
    messagebox.showinfo("Message", "Initiating Server Shutdown")
    global RUNNING,KILLPROGRAM,serversocket,root,ConnectedPlayers

    RUNNING = False
    KILLPROGRAM = True

    # disconnect all sessions
    for players in ConnectedPlayers:
        try:
            players.GetConnection.close()
        finally:
            continue

    try:
        # Initiate Shutdown
        serversocket.close()
    finally:
        None

    # Use a fake socket to exit from the server.accept() loop
    try:
        fakeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fakeSocket.connect((IPAddr, PORT))
    finally:
        None

    try:
        # Kill GUI
        root.destroy()
    finally:
        None

    print("[*] Server Shutting Down. . .")

def ReadyGame():
    global bucketGameThread, RUNNING

    if RUNNING == False:
        RUNNING = True
        bucketGameThread = threading.Thread(target=BucketGame, name='BucketGameThread')

    bucketGameThread.start()

bucketGameThread = threading.Thread(target=BucketGame, name='BucketGameThread')
rbutton = tk.Button(root, text="Retry", command=ReadyGame)
flabel = tk.Label(root, text="Oh nyo, yuwu wowst! >w<")

def main():
    global bucketGameThread

    print("[*] Preparing Threads. . .")
    serverThread = threading.Thread(target=RunServer, name='ServerThread')
    serverThread.start() # start thread

    ServerHandle()
    serverThread.join() # wait for thread to finish

    print("End Of Program!")

if __name__ == "__main__":
    main()