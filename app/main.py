import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
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
    print(json.dumps(data))
    color = "gold"
    return start_response(color)

@bottle.post('/move')
def move():
    data = bottle.request.json
###################WALLS##############################
    height = data['board']['height'] - 1
    width = data['board']['width'] - 1
    walls = []
    h = 0
    w = 0

    while (h<height):
        a = [[-1, h]]
        walls.extend(a)
        h = h + 1
    h = 0
    while (h<height):
        a = [[width+1, h]]
        walls.extend(a)
        h = h + 1
    while (w<width):
        a = [[w, -1]]
        walls.extend(a)
        w = w + 1
    w = 0
    while (w<width):
        a = [[w, height+1]]
        walls.extend(a)
        w = w + 1
    ####################ME##########################
    me = data['you']['body']
    health = data['you']['health']
    length = len(me)
    m = 1
    HeadX = me[0]['x']
    HeadY = me[0]['y']
    if health == 100:
        m = 0
    for i in range((length) - m):
        a = [[me[i]['x'],me[i]['y']]]
        walls.extend(a)
    ####################OTHERS######################
    others = data['board']['snakes']
    for i in range(len(others)):
        o = 1
        snake = others[i]
        if snake['health'] == 100:
            o = 0
        for j in range(len(snake['body']) - o):
            a = [[snake['body'][j]['x'], snake['body'][j]['y']]]
            walls.extend(a)
    ####################TEST########################
    directions = [[0,-1],[0,1],[-1,0],[1,0]]
    i = 1
    while i < 5:
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
        else:
            directions.remove(direction)
        i = i + 1

    return move_response('left')
    ####################TURN_0######################
    



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