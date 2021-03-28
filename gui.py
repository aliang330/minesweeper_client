import pygame
from pygame.locals import *
import sys
import random
import socket
import threading
import os
from board import Board
pygame.init()

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

game_width = 10  # Change this to increase size
game_height = 10  # Change this to increase size
numMine = 9  # Number of mines
grid_size = 32  # Size of grid (WARNING: macke sure to change the images dimension as well)
border = 16  # Top border
top_border = 16  # Left, Right, Bottom border
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
gameDisplay = pygame.display.set_mode((display_width, display_height), RESIZABLE)  # Create display
pygame.display.set_caption("Minesweeper")  # S Set the caption of window

hostname = "localhost"
port = 4444
HEADER_SIZE = 10
server_socket = None

spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")
spr_grid6 = pygame.image.load("Sprites/grid6.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_grid8 = pygame.image.load("Sprites/grid8.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")


class Grid:
    def __init__(self, xGrid, yGrid, val):
        self.xGrid = xGrid  # X pos of grid
        self.yGrid = yGrid  # Y pos of grid
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(border + self.xGrid * grid_size, top_border + self.yGrid * grid_size, grid_size, grid_size)
        self.val = val  # Value of the grid, -1 is mine
        if val == "-":
            self.is_dug = False
        else:
            self.is_dug = True
        if val == "F":
            self.is_flagged = True
            self.is_dug = False
        else:
            self.is_flagged = False

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        if self.val == "-":
            gameDisplay.blit(spr_grid, self.rect)
        elif self.val == "0":
            gameDisplay.blit(spr_emptyGrid, self.rect)
        elif self.val == "1":
            gameDisplay.blit(spr_grid1, self.rect)
        elif self.val == "2":
            gameDisplay.blit(spr_grid2, self.rect)
        elif self.val == "3":
            gameDisplay.blit(spr_grid3, self.rect)
        elif self.val == "4":
            gameDisplay.blit(spr_grid4, self.rect)
        elif self.val == "5":
            gameDisplay.blit(spr_grid5, self.rect)
        elif self.val == "6":
            gameDisplay.blit(spr_grid6, self.rect)
        elif self.val == "7":
            gameDisplay.blit(spr_grid7, self.rect)
        elif self.val == "8":
            gameDisplay.blit(spr_grid8, self.rect)
        elif self.val == "F":
            gameDisplay.blit(spr_flag, self.rect)

############################################################################################

def update_grid(board_string):
    board_string = board_string.replace(" ", "")
    global grid
    grid = []
    row = []
    col_count = 0
    row_count = 0
    for char in board_string:
        if char == "\n":
            grid.append(row)
            row = []
            row_count += 1
            col_count = 0
        else:
            row.append(Grid(col_count, row_count, char))
            col_count += 1
    # if len(grid) != game_height:
    #     update_screen_size(len(grid))



def game_loop():
    global grid
    grid = []

    # generate entire grid
    for j in range(game_height):
        row = []
        for i in range(game_width):
            row.append(Grid(i,j, "-"))
        grid.append(row)
    in_game = True

    while in_game:
        gameDisplay.fill(bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            if event.type == pygame.MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # If player left clicked of the grid
                                    if j.is_dug or j.is_flagged:
                                        pass
                                    else:
                                        client_request_string = f"d {j.xGrid} {j.yGrid}\n"
                                        server_socket.send(client_request_string.encode())
                                elif event.button == 3:
                                    # If the player right clicked
                                    if j.is_flagged:
                                        client_request_string = f"df {j.xGrid} {j.yGrid}\n"
                                        server_socket.send(client_request_string.encode())
                                    else:
                                        client_request_string = f"f {j.xGrid} {j.yGrid}\n"
                                        server_socket.send(client_request_string.encode())
        for i in grid:
            for j in i:
                j.drawGrid()
        pygame.display.update()

##################################################################################################
def receive(socket, signal):
    full_server_reponse = ""
    new_msg = True
    while signal:
        try:
            server_response_length = socket.recv(HEADER_SIZE).decode("utf-8")
            if server_response_length:
                print(server_response_length)
                remaining_bytes_to_read = int(server_response_length)
                while remaining_bytes_to_read != 0:
                    server_response_length = int(server_response_length)
                    server_response_chunk = socket.recv(remaining_bytes_to_read).decode("utf-8")
                    full_server_reponse += server_response_chunk
                    remaining_bytes_to_read = server_response_length - len(full_server_reponse)
                print(full_server_reponse, end="")
                update_grid(full_server_reponse)
                full_server_reponse = ""

        except:
            # print("You have been disconnected from the server")
            # signal = False
            pass
        

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((hostname, port))
except:
    print("Error")
    input("press enter to exit")
    sys.exit(0)

receiveThread = threading.Thread(target = receive, args = (server_socket, True))
receiveThread.start()


######################################################################################################

game_loop()
pygame.quit()