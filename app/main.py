import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Testing Shit out for real this time.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json
    #print(json.dumps(data))
    color = "FFDD33"
    headType = "tongue"
    tailType = "curled"
    return start_response(color, headType, tailType)

@bottle.post('/move')
def move():
    data = bottle.request.json
    #print(json.dumps(data))

    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)

    return move_response(direction)
"""
###################WALLS##############################
    height = data['board']['height'] - 1 ##data
    width = data['board']['width'] - 1 #data
    walls = []
    enemyheads = []
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
    me = ['you']['body'] #data
    ID = ['you']['id'] #data
    health = ['you']['health'] #data
    length = len(me)
    HeadX = me[0]['x']
    HeadY = me[0]['y']
    TailX = me[length-1]['x']
    TailY = me[length-1]['y']
    m = 1
    if health == 100:
        m = 0
    for i in range(length - 1):
        a = [[me[i]['x'], me[i]['y']]]
        walls.extend(a)

    ####################OTHERS######################
    others = ['board']['snakes'] #data
    for i in range(len(others)):
        if others[i]['id'] == ID:
            continue
        snake = others[i]
        for j in range(len(snake['body'])):
            a = [[snake['body'][j]['x'], snake['body'][j]['y']]]
            walls.extend(a)
            if j == 0:
                enemyheads.extend(a)

    ####################FIND FOOD OR TAIL########################
    FoodList = ['board']['food'] #data

    if health > 50 or len(FoodList) == 0:
        GoalX = TailX - HeadX
        GoalY = TailY - HeadY
    else:
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

        GoalX = FoodX - HeadX
        GoalY = FoodY - HeadY

    ########################MOVEMENT#############################
    if abs(GoalX) <= abs(GoalY):
        if GoalY > 0:
            if [HeadX, HeadY+1] not in walls:
                return move_response('down')
            elif GoalX >= 0:
                if [HeadX+1, HeadY] not in walls:
                    return move_response('right')
            elif GoalX < 0:
                if [HeadX-1, HeadY] not in walls:
                    return move_response('left')
            elif [HeadX, HeadY-1] not in walls:
                return move_response('up')

        if GoalY < 0:
            if [HeadX, HeadY-1] not in walls:
                return move_response('up')
            elif GoalX >= 0:
                if [HeadX+1, HeadY] not in walls:
                    return move_response('right')
            elif GoalX < 0:
                if [HeadX-1, HeadY] not in walls:
                    return move_response('left')
            elif [HeadX, HeadY+1] not in walls:
                return move_response('down')

    else:
        if GoalX > 0:
            if [HeadX+1, HeadY] not in walls:
                return move_response('right')
            elif GoalY >= 0:
                if [HeadX, HeadY+1] not in walls:
                    return move_response('down')
            elif GoalY < 0:
                if [HeadX, HeadY-1] not in walls:
                    return move_response('up')
            elif [HeadX-1, HeadY] not in walls:
                return move_response('left')

        if GoalX < 0:
            if [HeadX-1, HeadY] not in walls:
                return move_response('left')
            elif GoalY >= 0:
                if [HeadX, HeadY+1] not in walls:
                    return move_response('down')
            elif GoalY < 0:
                if [HeadX, HeadY-1] not in walls:
                    return move_response('up')
            elif [HeadX+1, HeadY] not in walls:
                return move_response('right')
    
    i = 1
    directions = [[0,-1],[0,1],[-1,0],[1,0]]
    while i < 20:
        direction = random.choice(directions)
        if [direction[0]+HeadX, direction[1]+HeadY] not in walls:
            if direction == [0,-1]:
                return move_response('up')
            if direction == [0,1]:
                return move_response('down')
            if direction == [-1,0]:
                return move_response('left')
            if direction == [1,0]:
                return move_response('right')
        i = i + 1

"""
@bottle.post('/end')
def end():
    data = bottle.request.json
    print(json.dumps(data))
    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )