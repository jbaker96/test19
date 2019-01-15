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

    color = "cyan"

    return start_response(color)








@bottle.post('/move')
def move():
    data = bottle.request.json
    height = data.board.height
    width = data.board.width

    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)


    if height = 20:
        return move_response('down')
    return move_response('right')










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