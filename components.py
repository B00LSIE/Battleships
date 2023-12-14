import random
import json


size = 10 
filenameJson = "placement.json"
filename = "battleships.txt"
strategy = 'simple'

def initialise_board(size : int):
    ''' 
    generates an empty board to be used for ship placement
    '''
    board = []
    for i in range(0 , size):
        rows = [None] * size 
        board.append(rows)
    return board

def create_battleships(filename):
    '''
    takes the battleships from the battleship text file and transforms it into a dictionary 
    '''
    try:
        with open(filename, 'r') as battleshipFile:
            battleships = {}
            for i in battleshipFile:
                shiplist = i.strip().split(':')
                name = shiplist[0].strip()
                size = int(shiplist[1].strip())
                battleships[name] = size
            print(battleships)
    except FileNotFoundError:
        battleships = {}
        print("There has been a FileNotFoundError.")
    return battleships

def place_battleships(board , ships , strategy):
    if strategy == 'simple':
        return simplePlace_battleships(board , ships)
    elif strategy == 'random':
        return randomPlace_battleships(board , ships)
    elif strategy == 'custom':
        return customPlace_battleships(board , ships , filenameJson)

def simplePlace_battleships(board : list, ships):
    '''
    iterates through the list of ships takes the name and size placing the ships
    at the start of the new line
    '''
    for shipDetails in ships.items():
        name = shipDetails[0]
        size = shipDetails[1]
        for row in range(0 , len(board)):
            if (row + int(size)) <= len(board):
                if None in board[row][0 : int(size)]:
                    board[row][0 : int(size)] = [name] * int(size)
                    break
    return board

def randomPlace_battleships(board : list, filename):
    ''' 
    does the same as the simple place but instead of placing the ships at the start of a new line, it randomly places it on the board
    '''
    for shipDetails in filename.items():
        placed = False
        while not placed:
            name = shipDetails[0]
            size = shipDetails[1]
            x = random.randint(0, len(board) - 1)
            y = random.randint(0, len(board[0]) - 1)
            randomChoose = random.randint(0, 1)
            if randomChoose == 0:
                direction = 'horizontal'
            else:
                direction = 'vertical'

            if direction == 'horizontal' and (y + int(size)) <= len(board[0]):
                if None in board[x][y : y + int(size)]:
                    board[x][y : y + int(size)] = [name] * int(size)
                    placed = True
            elif direction == 'vertical' and (x + int(size)) <= len(board):
                if all([board[i][y] is None for i in range(x, x + int(size))]):
                    for i in range(0, int(size)):
                        board[x + i][y] = name
                    placed = True

        print(f"Placed {name} at ({x}, {y}) with direction {direction}")
        print(board)

    return board


def customPlace_battleships(board : list, filename, filenameJson):
    '''
    takes in the values of the dictionary and allows the player to be given the layout of the board from the clientside to place the ships
    '''
    if type(filenameJson) == str:
        shipData = openFileBoards(filenameJson)
    elif type(filenameJson) == dict:
        shipData = filenameJson
    battleships = create_battleships(filename)

    for name, size in battleships.items():
        coords = shipData.get(name)

        print(f"Placing {name} at {coords} on the board.")
        print(f"Coords variable: {coords}")

        if coords:
            x = int(coords[1])
            y = int(coords[0])
            direction = coords[2]

            if 0 <= x < len(board) and 0 <= y < len(board[0]):
                if direction == "h" and y + size <= len(board[0]) and all(board[x][y + i] is None for i in range(size)):
                    for i in range(size):
                        board[x][y + i] = name
                elif direction == "v" and x + size <= len(board) and all(board[x + i][y] is None for i in range(size)):
                    for i in range(size):
                        board[x + i][y] = name
    print(board)
    return board

def openFileBoards(filename):
    try:
        with open(filename, 'r') as boardPlacement:  # opens the file to be read
            shipData = json.load(boardPlacement)   # load the json contents  
            return shipData
    except FileNotFoundError:
        print(filename + " was not found (error).")

def writeFileBoards(filename, newData : dict):
    boardData = {}
    for shipName, details in newData.items():     # unpacks the name and shipData in the new data dictionary
        boardData[shipName] = [str(coord) for coord in details]  # convert the coordinates into a string 
    with open(filename, 'w') as file:
        json.dump(boardData, file) # writes the data back into the file but with the new data and not the old 

        
def checkBoard(battleships : dict):
    '''
    checks to see whether the battleship dictionary is empty to determine whether someone has won the game
    '''
    if battleships == {}:
        return True
    else:
        return False