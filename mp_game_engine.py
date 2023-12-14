from components import initialise_board, create_battleships,simplePlace_battleships,randomPlace_battleships,customPlace_battleships , filenameJson , filename
from game_engine import attack,cli_coordinates_input
import random


size = 10
players = {}
previousAttacks = []

filename = 'battleships.txt'
#2player1Name = input("Please type your username here. ")


def aiTurn(userBoard : list, previousattacks : list, battleship : dict):
    '''
    this loops through, creating the coordinates for an attack and then carrying out the attack changing the player's board
    '''
    while True:
        aiAttackCoords = generate_attack(previousattacks, userBoard)
        print("The AI has attacked the coordinates", aiAttackCoords)
        aiAttack = attack(aiAttackCoords, userBoard, battleship)
        return aiAttackCoords

def userTurn(aiBoard : list , battleship : dict, coordinates : str): 
    ''' takes the ai board , ai battleships and the coordinates from the user or clientside 
    then using the attack function to execute the attack and change the board accordingly 
    '''
    userAttack = attack(coordinates , aiBoard , battleship)
    return userAttack


def generate_attack(previousAttacks : list , board : list):
    '''
    takes the previous attacks and loops through generating new coordinates until one that has not been used 
    is the sent to be used for the ai to attack the player'''
    newAttack = False
    while newAttack == False:
        x = random.randint(0 , len(board) - 1 )
        y = random.randint(0 , len(board) - 1 )
        attackCoords = [ x , y ]
        if attackCoords in previousAttacks:
            newAttack = False 
        else: 
            newAttack = True
            break
    return attackCoords

def ai_opponent_game_loop():
    print("Welcome to battleships!")
    userBoard = initialise_board(size)
    aiBoard = initialise_board(size)
    aiBattleships = create_battleships(filename)
    userBattleships = create_battleships(filename)
    print("AI battleships: " , aiBattleships)
    print("User battleships: " , userBattleships)
    aiBoard = randomPlace_battleships(aiBoard , aiBattleships)
    userBoard = customPlace_battleships(userBoard ,filename , filenameJson)
    print("userBoard: \n" ,userBoard)
    print("aiBoard: \n" , aiBoard)
    boolCheckAI = all(size == 0 for size in aiBattleships)
    boolCheckUser = all(size == 0 for size in userBattleships)
    print("Player goes first!")
    while boolCheckAI == False and boolCheckUser == False:
        coordinates = cli_coordinates_input()
        userTurn(aiBoard , aiBattleships , coordinates)
        boolCheckAI = all(size == 0 for size in aiBattleships) 
        if boolCheckAI == True:
            print("Game over you won!")
            break
        print("AI turn now!")
        aiTurn(userBoard , previousAttacks , userBattleships)
        print(userBoard)
        boolCheckUser = all(size == 0 for size in userBattleships)
        if boolCheckUser == True :
            print("Game over! you lose.")  


ai_opponent_game_loop()