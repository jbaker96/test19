import json
import os
import random
import numpy as np
import csv

import bottle
from bottle import HTTPResponse


@bottle.route("/")
def index():
    return "We really in this shit"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    #print(("START:", json.dumps(data)))

    response = {"color": "#FFC100", "headType": "tongue", "tailType": "curled"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

def FindTail(a, walls, checked, tail, count):
    headU = [0, -1]
    headD = [0, 1]
    headL = [-1, 0]
    headR = [1, 0]

    if a in walls:
        return False
    if a in checked:
        return False
    if a == tail:
        if count[0] == 1 and bottle.request.json['you']['health'] == 100:
            return False
        return True
    count[0] = count[0] + 1
    checked.extend([a])

    tailX = tail[0] - a[0]
    tailY = tail[1] - a[1]
    headU = [0, -1]
    headD = [0, 1]
    headL = [-1, 0]
    headR = [1, 0]

    if abs(tailX) >= abs(tailY):
        if tailX > 0:
            first = headR
            if tailY >= 0:
                second = headD
                third = headU
                last = headL
            else:
                second = headU
                third = headD
                last = headL
        else:
            first = headL
            if tailY >= 0:
                second = headD
                third = headU
                last = headR
            else:
                second = headU
                third = headD
                last = headR
    else:
        if tailY > 0:
            first = headD
            if tailX >= 0:
                second = headR
                third = headL
                last = headU
            else:
                second = headL
                third = headR
                last = headU
        else:
            first = headU
            if tailX >= 0:
                second = headR
                third = headL
                last = headD
            else:
                second = headL
                third = headR
                last = headD

    if (FindTail([a[0] + first[0], a[1] + first[1]], walls, checked, tail, count)) == True:
        return True
    if (FindTail([a[0] + second[0], a[1] + second[1]], walls, checked, tail, count)) == True:
        return True
    if (FindTail([a[0] + third[0], a[1] + third[1]], walls, checked, tail, count)) == True:
        return True
    if (FindTail([a[0] + last[0], a[1] + last[1]], walls, checked, tail, count)) == True:
        return True
    return False

def StandardFind(GoalX, GoalY, walls, HeadX, HeadY):
    if abs(GoalX) <= abs(GoalY):
        if GoalY > 0:
            if [HeadX, HeadY+1] not in walls:
                return 'down'
            elif GoalX >= 0:
                if [HeadX+1, HeadY] not in walls:
                    return 'right'
            elif GoalX < 0:
                if [HeadX-1, HeadY] not in walls:
                    return 'left'
            elif [HeadX, HeadY-1] not in walls:
                return 'up'

        if GoalY < 0:
            if [HeadX, HeadY-1] not in walls:
                return 'up'
            elif GoalX >= 0:
                if [HeadX+1, HeadY] not in walls:
                    return 'right'
            elif GoalX < 0:
                if [HeadX-1, HeadY] not in walls:
                    return 'left'
            elif [HeadX, HeadY+1] not in walls:
                return 'down'

    else:
        if GoalX > 0:
            if [HeadX+1, HeadY] not in walls:
                return 'right'
            elif GoalY >= 0:
                if [HeadX, HeadY+1] not in walls:
                    return 'down'
            elif GoalY < 0:
                if [HeadX, HeadY-1] not in walls:
                    return 'up'
            elif [HeadX-1, HeadY] not in walls:
                return 'left'

        if GoalX < 0:
            if [HeadX-1, HeadY] not in walls:
                return 'left'
            elif GoalY >= 0:
                if [HeadX, HeadY+1] not in walls:
                    return 'down'
            elif GoalY < 0:
                if [HeadX, HeadY-1] not in walls:
                    return 'up'
            elif [HeadX+1, HeadY] not in walls:
                return 'right'

def find_move(data):
    turn = data['turn']
    height = data['board']['height'] - 1 
    width = data['board']['width'] - 1 
    walls = []
    danger = []
    enemyheads = []
    enemytails = []
    checked = []
    center = [width//2, height//2]
    count = [1]
    h = 0
    w = 0
    while (h<=height):
        a = [[-1, h]]
        walls.extend(a)
        h = h + 1
    h = 0
    while (h<=height):
        a = [[width+1, h]]
        walls.extend(a)
        h = h + 1
    while (w<=width):
        a = [[w, -1]]
        walls.extend(a)
        w = w + 1
    w = 0
    while (w<=width):
        a = [[w, height+1]]
        walls.extend(a)
        w = w + 1

    ####################ME##########################
    me = data['you']['body'] 
    ID = data['you']['id'] 
    health = data['you']['health'] 
    length = len(me)
    HeadX = me[0]['x']
    HeadY = me[0]['y']
    TailX = me[length-1]['x']
    TailY = me[length-1]['y']
    tail = [TailX, TailY]
    for i in range(length - 1):
        a = [[me[i]['x'], me[i]['y']]]
        walls.extend(a)
    #if health == 100:
    #    if tail == [HeadX + 1, HeadY] or tail == [HeadX - 1, HeadY] or tail == [HeadX, HeadY + 1] or tail == [HeadX, HeadY - 1]:
    #        a = [tail]
    #        walls.extend(a)

    ####################OTHERS######################
    others = data['board']['snakes']
    for i in range(len(others)):
        if others[i]['id'] == ID:
            continue
        snake = others[i]
        threat = len(snake['body'])
        for j in range(len(snake['body'])):
            if j == len(snake['body']):
                a = [[snake['body'][j]['x'], snake['body'][j]['y']]]
                enemytails.extend(a)
                if snake['health'] != 100:
                    walls.extend(a)    
            else:    
                a = [[snake['body'][j]['x'], snake['body'][j]['y']]]
                walls.extend(a)
                if j == 0:
                    enemyheads.extend(a)
        if threat >= length:
            a = [[snake['body'][0]['x'] + 1, snake['body'][0]['y']]]
            danger.extend(a)
            a = [[snake['body'][0]['x'] - 1, snake['body'][0]['y']]]
            danger.extend(a)
            a = [[snake['body'][0]['x'], snake['body'][0]['y'] + 1]]
            danger.extend(a)
            a = [[snake['body'][0]['x'], snake['body'][0]['y'] - 1]]
            danger.extend(a)

    ####################ORDER GOALS & SAFETY NET##############################
    goal = []
    safetynet = []
    if health < 51:    
        FoodList = data['board']['food']
        j = 0
        while (j < len(FoodList)):
            b = abs(FoodList[j]['x'] - HeadX) + abs(FoodList[j]['y'] - HeadY)
            if j == 0:
                minval = b
                counter = j
            if b < minval:
                counter = j
                minval = b
            j = j + 1

        FoodX = FoodList[counter]['x']
        FoodY = FoodList[counter]['y']

        goal.append([FoodX, FoodY])
        goal.append(tail)
        goal.append(center)
        safetynet.append(tail)
        safetynet.append(center)
    else:
        goal.append(tail)
        #goal.append(center)
        safetynet.append(tail)
        #safetynet.append(center)

    #####################FIND BEST GOAL###########################
    if turn < 3:
        GoalX = (width//2) - HeadX
        GoalY = (height//2) - HeadY
        resp = StandardFind(GoalX, GoalY, walls, HeadX, HeadY)
        return (resp)
    else:
        for i in goal:
            for j in safetynet:
                #Check Left
                Left = 0
                if FindTail([HeadX - 1, HeadY], walls, checked, i, count) == True:
                    if FindTail(i, walls, checked, j, count) == True:
                        Left = count[0]
                        if [HeadX - 1, HeadY] in danger:
                            if i > 0 or j > 0:
                                Left = Left + 50
                            else:
                                Left = Left + 100
                #Reset
                count[0] = 1
                checked = []
                #Check Right
                Right = 0
                if FindTail([HeadX + 1, HeadY], walls, checked, i, count) == True:
                    if FindTail(i, walls, checked, j, count) == True:
                        Right = count[0]
                        if [HeadX + 1, HeadY] in danger:
                            if i > 0 or j > 0:
                                Right = Right + 50
                            else:
                                Right = Right + 100
                #Reset
                count[0] = 1
                checked = []
                #Check Up
                Up = 0
                if FindTail([HeadX, HeadY - 1], walls, checked, i, count) == True:
                    if FindTail(i, walls, checked, j, count) == True:    
                        Up = count[0]
                        if [HeadX, HeadY - 1] in danger:
                            if i > 0 or j > 0:
                                Up = Up + 50
                            else:
                                Up = Up + 100
                #Reset
                count[0] = 1
                checked = []
                #Check Down
                Down = 0
                if FindTail([HeadX, HeadY + 1], walls, checked, i, count) == True:
                    if FindTail(i, walls, checked, j, count) == True:
                        Down = count[0]
                        if [HeadX, HeadY + 1] in danger:
                            if i > 0 or j > 0:
                                Down = Down + 50
                            else:
                                Down = Down + 100
                #Reset
                count[0] = 1
                checked = []
                var = [Left, Right, Up, Down]
                check1 = max(var)
                if check1 == 0 or check1 > 100:
                    continue
                check2 = min(i for i in var if i > 0)
                pos = var.index(check2)   
                if pos == 0:
                    return ('left')
                if pos == 1:
                    return ('right')
                if pos == 2:
                    return ('up')
                if pos == 3:
                    return ('down') 


    i = 1
    directions = [[0,-1],[0,1],[-1,0],[1,0]]
    while i < 20:
        direction = random.choice(directions)
        if [direction[0]+HeadX, direction[1]+HeadY] not in walls:
            if direction == [0,-1]:
                return ('up')
            if direction == [0,1]:
                return ('down')
            if direction == [-1,0]:
                return ('left')
            if direction == [1,0]:
                return ('right')
        i = i + 1

def board_heuristic(data):
    matrix = []
    height = data['board']['height'] - 1 
    width = data['board']['width'] - 1
    matrix = [[0.2 for x in range(width+1)] for y in range(height+1)]
    board = np.array(matrix)

    me = data['you']['body'] 
    ID = data['you']['id'] 
    health = data['you']['health'] 
    length = len(me)
    HeadX = me[0]['x']
    HeadY = me[0]['y']
    walls = []
    TailX = me[length-1]['x']
    TailY = me[length-1]['y']
    tail = [TailX, TailY]
    for i in range(length):
        if i == 0:
            board[me[i]['y'], me[i]['x']] = -1
        elif i == length - 1 and health < 100:
            board[me[i]['y'], me[i]['x']] = 1
        else:
            board[me[i]['y'], me[i]['x']] = 0
    
    print(board)
    '''
    ####################OTHERS######################
    others = data['board']['snakes']
    for i in range(len(others)):
        if others[i]['id'] == ID:
            continue
        snake = others[i]
        threat = len(snake['body'])
        for j in range(len(snake['body'])):
            if j == len(snake['body']):
                a = [[snake['body'][j]['x'], snake['body'][j]['y']]]
                enemytails.extend(a)
                if snake['health'] != 100:
                    walls.extend(a)    
            else:    
                a = [[snake['body'][j]['x'], snake['body'][j]['y']]]
                walls.extend(a)
                if j == 0:
                    enemyheads.extend(a)
        if threat >= length:
            a = [[snake['body'][0]['x'] + 1, snake['body'][0]['y']]]
            danger.extend(a)
            a = [[snake['body'][0]['x'] - 1, snake['body'][0]['y']]]
            danger.extend(a)
            a = [[snake['body'][0]['x'], snake['body'][0]['y'] + 1]]
            danger.extend(a)
            a = [[snake['body'][0]['x'], snake['body'][0]['y'] - 1]]
            danger.extend(a)

    goal = []
    safetynet = []
    if health < 51:    
        FoodList = data['board']['food']
        j = 0
        while (j < len(FoodList)):
            b = abs(FoodList[j]['x'] - HeadX) + abs(FoodList[j]['y'] - HeadY)
            if j == 0:
                minval = b
                counter = j
            if b < minval:
                counter = j
                minval = b
            j = j + 1

        FoodX = FoodList[counter]['x']
        FoodY = FoodList[counter]['y']

        goal.append([FoodX, FoodY])
        goal.append(tail)
        goal.append(center)
        safetynet.append(tail)
        safetynet.append(center)
    else:
        goal.append(tail)
        goal.append(center)
        safetynet.append(tail)
        safetynet.append(center)'''
    #NeuralNetwork(board)

'''
def NeuralNetwork(inputs):
    input_nodes = len(inputs)
    hl1_nodes = 40
    hl2_nodes = 12
    output_nodes = 4
    W1_shape = (hl1_nodes, input_nodes)
    W2_shape = (hl2_nodes, hl1_nodes)
    W3_shape = (output_nodes, hl2_nodes)

    W1, W2, W3 = get_csv_weights()

def get_csv_weights():
'''

@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    #print(("MOVE:", json.dumps(data)))

    # Choose a random direction to move in
    # directions = ["up", "down", "left", "right"]
    move = find_move(data)

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = ""

    board_heuristic(data)

    response = {"move": move, "shout": shout}

    #print(response)

    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    #print(("END:", json.dumps(data)))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
