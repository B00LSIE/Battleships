from flask import Flask, render_template, request, jsonify
from components import create_battleships, filename, size, initialise_board, customPlace_battleships, writeFileBoards, openFileBoards , randomPlace_battleships, checkBoard
from mp_game_engine import aiTurn 
from game_engine import attack

app = Flask(__name__)

filenameJson = "placement.json"
playerBoard = initialise_board(size) 
emptyBoard = initialise_board(size)
battleshipsAI= create_battleships(filename)
battleshipsUser = create_battleships(filename)
aiBoard = randomPlace_battleships(emptyBoard , battleshipsAI)
prevAttacks = []


@app.route('/attack', methods=['GET'])
def process_attack():
    '''
    takes the x and y coordinate from the clientside 
    
    makes them into a tuple 
    
    uses them for the user attack
    ai then takes their turn 
    it then checks whether if all ships are still afloat 
    then responds accordingly
    '''
    if request.args:
        x = request.args.get('x')    #this requires a feedback and change to the board to show where the shot by the player has made
        y = request.args.get('y')
        attackCoords = ( x , y )
        userAttack = attack(attackCoords , aiBoard , battleshipsAI)
        aiAttack = aiTurn(playerBoard, prevAttacks, battleshipsUser)
        print(f"User Attack: {userAttack}")
        print(f"AI Attack: {aiAttack}")
        boolCheckAI = checkBoard(battleshipsUser)
        boolCheckUser = checkBoard(battleshipsAI)
        print(aiBoard)
        print(boolCheckUser)
        print(battleshipsAI)
        if boolCheckUser == True:
            print(boolCheckUser)
            return jsonify({"hit" : True ,'finished' : "Game Over! You win!"})
        if boolCheckAI == True:
            return jsonify({"hit" : True ,'finished' : "Game over! You lose!"})
        
        if userAttack == True:
            return jsonify({"hit" : True , "AI_Turn" : aiAttack}) 
        elif userAttack == False:
            return jsonify({"hit" : False , "AI_Turn" : aiAttack})
        
        
@app.route('/', methods=['GET'])
def root():
    '''
    renders the players board for the game
    '''
    return render_template('main.html', player_board=playerBoard)

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    '''
    generation of a board to be used to construct both player and the ai board
    takes the ships from the battleship text file and creates a dictionary
    when a GET mehtod is sent the response is the ships to be placed and the board size
    
    when a POST method is sent back to the server side, the data is extracted and the player's board is created
    with a message for confirmation'''
    newBoard = initialise_board(size)
    ships = create_battleships(filename)

    if request.method == 'GET':
        return render_template('placement.html', ships=ships, board_size=size)

    if request.method == 'POST':
        newData = request.get_json()
        print(newData)
        writeFileBoards(filenameJson, newData)
        global playerBoard
        playerBoard = customPlace_battleships(newBoard, filename, filenameJson)
        return jsonify({"message": "success"})

if __name__ == '__main__':
    app.template_folder = 'templates'
    app.run()
