"""Two player tron clone"""

import os
import msvcrt
import time
import random

def clear_screen():
    """clear command line"""
    os.system("cls")

def get_char():
    """return next keypress immediately"""
    return chr(ord(msvcrt.getch()))

def initialize_board(background = " ", wall = "▄", width = 40, height = 40):
    """returns initialized board"""

    if width < 5: width = 10 # force minimum size
    if height < 5: height = 10 # force minimum size

    board = [[background for i in range(width)] for i in range(height)]
    for i, item in enumerate(board[0]):
        board[0][i] = wall
        board[-1][i] = wall
    for row in board:
        row[0] = wall
        row[-1] = wall

    start_width = int(width/4) # lazy "rounding"
    start_height = int(height/2) # lazy "rounding"

    board[start_height][start_width] = "·"
    location1 =  [start_height, start_width] # player 1 location

    board[start_height][start_width*3] = "·"
    location2 = [start_height, start_width*3] # player 2 location

    return board, background, location1, location2

def draw_board(board):
    """draws board"""
    print("\n", "  TRON CLONE", (len(board[0]*2)-34)*" ", "CONTROLS: WASD + IJKL", "\n")
    for row in board:
        print("   "+" ".join(row))

def move_pending():
    """returns true/false if keyboard hit is pending in msvcrt buffer"""
    return msvcrt.kbhit()

def parse_controls(char, d1_old, d2_old):
    """parses control key compared to previous controls"""
    backwards_check = {"w": "s", "a": "d", "i": "k", "j": "l",
                       "s": "w", "d": "a", "k": "i", "l": "j"
                      } # dictionary to check 
    if char not in "wasdijkl": # invalid control
        return d1_old, d2_old
    elif backwards_check[char] == d1_old or backwards_check[char] == d2_old: # check that move wasnt backwards
         return d1_old, d2_old
    elif char in "wasd":
        return char, d2_old
    elif char in "ijkl":
        return d1_old, char

def move_player(direction, location, board, background):
    """moves players by one square and leaves trail. returns used direction and new location. also returns true/false if game is over"""
    if direction == "w" or direction == "i":
        board[location[0]][location[1]] = "▲" # leave trail
        if not board[location[0]-1][location[1]] == background:
            board[location[0]-1][location[1]] = "#"
            return direction, location, True
        else:
            board[location[0]-1][location[1]] = "·" # move
        location = [location[0]-1,location[1]] # move location
    if direction == "s" or direction == "k":
        board[location[0]][location[1]] = "▼" # leave trail
        if not board[location[0]+1][location[1]] == background:
            board[location[0]+1][location[1]] = "#"
            return direction, location, True
        else:
            board[location[0]+1][location[1]] = "·" # move
        location = [location[0]+1,location[1]] # move location
    if direction == "d" or direction == "l":
        board[location[0]][location[1]] = "►" # leave trail
        if not board[location[0]][location[1]+1] == background:
            board[location[0]][location[1]+1] = "#"
            return direction, location, True
        else:
            board[location[0]][location[1]+1] = "·" # move
        location = [location[0],location[1]+1] # move location
    if direction == "a" or direction == "j":
        board[location[0]][location[1]] = "◄" # leave trail
        if not board[location[0]][location[1]-1] == background:
            board[location[0]][location[1]-1] = "#"
            return direction, location, True
        else:
            board[location[0]][location[1]-1] = "·" # move
        location = [location[0],location[1]-1] # move location
    return direction, location, False

def play_round(location1, location2, board, background):
    """main gameplay loop. returns winner"""
    msvcrt.ungetch(b"g") # force feed arbitary key to skip first get_char
    d1_old = "d" # force starting direction
    d2_old = "j" # force starting direction
    speed = 0
    while True:
        d1, d2 = parse_controls(get_char(), d1_old, d2_old)
        buffered_move = True # this should enable control buffer # uncomentto enable buffer
        while not move_pending() or buffered_move == True: #uncomment to enable buffer
            speed += 1

            movefirst = random.getrandbits(1)

            if movefirst == 1:
                d1_old, location1, gameover1 = move_player(d1, location1, board, background)
                d2_old, location2, gameover2 = move_player(d2, location2, board, background)
            else:
                d2_old, location2, gameover2 = move_player(d2, location2, board, background)
                d1_old, location1, gameover1 = move_player(d1, location1, board, background)

            buffered_move = False # this should enable control buffer # use this to enable buffer. allows blocking other players move
            clear_screen()
            draw_board(board)
            time.sleep(1/((speed+1)**0.8))


            if gameover1 == True: # wasd collided
                return "IJKL"
            if gameover2 == True: # ijkl collided
                return "WASD"





def main():
    """main game loop"""
    board, background, location1, location2 = initialize_board()
    winner = play_round(location1, location2, board, background)
    print ("\n"+(len(board[0])-2)*" "+winner, "WINS!")



if __name__ == '__main__':
    main()



# "valikot" skaalaamaan
# buffer/blokkaus ongelma