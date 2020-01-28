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
    pydict = {
        "color": "#FFC100",
        "headType": "tongue",
        "tailType": "curled"
    }
    jsonoutput = json.dumps(pydict)
    return jsonoutput
    
def FindTail(a, walls, checked, tail, count):
    headU = [0, -1]
    headD = [0, 1]
    headL = [-1, 0]
    headR = [1, 0]

    if a == tail:
        return True
    if a in walls:
        return False
    if a in checked:
        return False
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

@bottle.post('/move')
def move():
    data = bottle.request.json

###################WALLS##############################
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
    if health == 100:
        a = [tail]
        walls.extend(a)

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

        #GoalX = FoodX - HeadX
        #GoalY = FoodY - HeadY
        goal[0] = [FoodX, FoodY]
        goal[1] = tail
        goal[2] = center
        safetynet[0] = tail
        safetynet[1] = center
    else:
        goal[0] = tail
        goal[1] = center
        safetynet[0] = tail
        safetynet[1] = center

    #####################FIND BEST GOAL###########################
    if turn < 3:
        GoalX = (width//2) - HeadX
        GoalY = (height//2) - HeadY
        resp = StandardFind(GoalX, GoalY, walls, HeadX, HeadY)
        return move_response(resp)
    else:
        for i in goal:
            for j in safetynet:
                #Check Left
                Left = 0
                if FindTail([HeadX - 1, HeadY], walls, checked, goal[i], count) == True:
                    if FindTail(goal[i], walls, checked, tail[j], count) == True:
                        Left = count[0]
                        if [HeadX - 1, HeadY] in danger:
                            Left = Left + 100
                #Reset
                count[0] = 1
                checked = []
                #Check Right
                Right = 0
                if FindTail([HeadX + 1, HeadY], walls, checked, goal[i], count) == True:
                    if FindTail(goal[i], walls, checked, tail[j], count) == True:
                        Right = count[0]
                        if [HeadX + 1, HeadY] in danger:
                            Right = Right + 100
                #Reset
                count[0] = 1
                checked = []
                #Check Up
                Up = 0
                if FindTail([HeadX, HeadY - 1], walls, checked, goal[i], count) == True:
                    if FindTail(goal[i], walls, checked, tail[j], count) == True:    
                        Up = count[0]
                        if [HeadX, HeadY - 1] in danger:
                            Up = Up + 100
                #Reset
                count[0] = 1
                checked = []
                #Check Down
                Down = 0
                if FindTail([HeadX, HeadY + 1], walls, checked, goal[i], count) == True:
                    if FindTail(goal[i], walls, checked, tail[j], count) == True:
                        Down = count[0]
                        if [HeadX, HeadY + 1] in danger:
                            Down = Down + 100
                #Reset
                count[0] = 1
                checked = []
                var = [Left, Right, Up, Down]
                check1 = max(var)
                if check1 == 0:
                    continue
                check2 = min(i for i in var if i > 0)
                pos = var.index(check2)   
                if pos == 0:
                    return move_response('left')
                if pos == 1:
                    return move_response('right')
                if pos == 2:
                    return move_response('up')
                if pos == 3:
                    return move_response('down') 


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


@bottle.post('/end')
def end():
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