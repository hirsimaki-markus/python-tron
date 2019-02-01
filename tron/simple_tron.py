"""command line single player tron"""

import time
import sys
import os
import msvcrt


def clear_screen():
    """clear command line"""
    os.system("cls")


def get_control():
    """return next keypress immediately"""
    return chr(ord(msvcrt.getch()))


def init_game(background = " ", player = "·", wall = "▄"):
    """returns initialized game elements"""

    score = 0
    board = [[background for i in range(41)] for i in range(41)]

    for i, item in enumerate(board[0]): # draw walls
        board[0][i] = wall
        board[-1][i] = wall
    for row in board:
        row[0] = wall
        row[-1] = wall
        
    board[20][20] = player # place player
    location = [20, 20] # save player position
    return board, background, player, wall, location, score


def game_loop(board, background, location, wall, player, score):
    """main game loop"""
    msvcrt.ungetch(b"w") # force feed first control
    direction_old = "w" # save force fed direction
    while True: # fallback loop to catch keypresses
        direction = get_control().lower()
        move_pending = True
        while not msvcrt.kbhit() or move_pending == True: # this loop breaks if keypress waiting. move pending enables one key buffer
            if direction == "w" and direction_old != "s": # direction old used to check that player doesnt move backwards
                board[location[0]][location[1]] = "▲" # leave trail
                if not board[location[0]-1][location[1]] == background:
                    exit()
                else:
                    board[location[0]-1][location[1]] = player # move
                    score += 1
                location = [location[0]-1,location[1]] # move location
            elif direction == "s" and direction_old != "w":
                board[location[0]][location[1]] = "▼" # leave trail
                if not board[location[0]+1][location[1]] == background:
                    exit()
                else:
                    board[location[0]+1][location[1]] = player # move
                    score += 1
                location = [location[0]+1,location[1]] # move location
            elif direction == "d" and direction_old != "a":
                board[location[0]][location[1]] = "►" # leave trail
                if not board[location[0]][location[1]+1] == background:
                    exit()
                else:
                    board[location[0]][location[1]+1] = player # move
                    score += 1
                location = [location[0],location[1]+1] # move location
            elif direction == "a" and direction_old != "d":
                board[location[0]][location[1]] = "◄" # leave trail
                if not board[location[0]][location[1]-1] == background:
                    exit()
                else:
                    board[location[0]][location[1]-1] = player # move
                    score += 1
                location = [location[0],location[1]-1] # move location
            elif direction == "x":
                exit()
            else:
                direction = direction_old #re use old direction if new was backwards

            direction_old = direction # store direction for next "move" comparison

            move_pending = False # this should enable one key buffer (or more??)






            clear_screen()
            print ("\n"+" "*37+"score:" +str(score)+"\n")
            for row in board:
                print ("  "+" ".join(row))
            print ("\n"+" "*26+"Move:WASD  Exit:X  Pause:other keys")

            time.sleep(1/((score+1)**0.8))


def main():
    """main game loop"""
    board, background, player, wall, location, score = init_game()
    game_loop(board, background, location, wall, player, score)


if __name__ == '__main__':
    main()