from components import initialise_board, create_battleships,simplePlace_battleships,randomPlace_battleships,customPlace_battleships 




size = 10
filename = "battleships.txt"
filenameJson = "placement.json"

def attack(coordinates : str , board : list , battleship : dict):
    '''
    takes the coordinates to then be used to be used to attack and determines whether a ship was there or it was a miss'''
    x = int(coordinates[0])
    y = int(coordinates[1])
    
    if 0 <= x < len(board) and 0 <= y < len(board[0]): # makes sure it is inside the biard 
        if board[x][y] is not None:    # to ensire it was a hit 
            name = board[x][y]
            print("Hit")
            
            if battleship[name] > 1: # deternines whether there are more than 1 space left by the ship 
                battleship[name] -= 1
            else:
                battleship.pop(name, None) # removes the ship from the dictionary to show it has been sunk
                print("You have sunk the " + name + "!")

            board[x][y] = None  # Update the board 
            return True
        else:
            print("Miss")
            return False
    else:
        print("Incorrect coordinates!")
        return False

def cli_coordinates_input(): # takes the x and y coordinates from the user to be used to attack the ai board
    attackCoordsX = input("Please input X coordinates you wish to attack") 
    attackCoordsY = input("Please input Y coordinate you wish to attack")
    attackCoords = (attackCoordsX , attackCoordsY)
    return attackCoords


def simple_game_loop():
    print("Welcome to Battleships!")
    board = initialise_board(size)
    battleships = create_battleships(filename)
    print(battleships)
    simplePlace_battleships(board , battleships)
    print(board)
    boolCheck = all(size == 0 for size in battleships)
    while battleships != boolCheck:
        attackCoords = cli_coordinates_input()
        attack(attackCoords , board , battleships)
        boolCheck = all(size == 0 for size in battleships)
    print("Game over! All ships have been sunk!")


simple_game_loop()