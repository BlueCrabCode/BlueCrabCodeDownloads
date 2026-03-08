import cubegame as cgame
import socketio as sio
from random import randint

window = cgame.display.window((850, 600))
controller = cgame.controller()

client = sio.Client()
client.connect('https://cubetopia.onrender.com', transports=['websocket', 'polling'])

playerpos = [0, 0]
playervel = [0, 0]
clientID = randint(0, 999999)
objects = []
players = {}

@client.on('movement')
def onmovement(data):
    if (not data['id'] in players): players[data['id']] = cgame.objects.rect((0, 0), (30, 30), (255, 190, 190))
    players[data['id']].pos = (data['x'], data['y'])

def newobject(x, y, w, h):
    rect = cgame.objects.rect((x, y), (w, h), (255, 255, 255))
    objects.append(rect)

def collision():
    rect = cgame.objects.rect((playerpos[0] - 5, playerpos[1] - 30), (30, 30), (255, 255, 255))
    for obj in objects:
        if (rect.collision(obj)): return True
        else: pass
    for player in players.values():
        if (player == players[clientID]): continue
        if (rect.collision(player)): return True
        else: pass

    return False

def update():
    if (controller.getkey('a')): playervel[0] -= (3.5 - -playervel[0]) / 5
    if (controller.getkey('d')): playervel[0] += (3.5 - playervel[0]) / 5
    if (not controller.getkey('a') and not controller.getkey('d')): playervel[0] *= 0.8

    playerpos[0] += playervel[0]
    if (collision()):
        playerpos[0] -= playervel[0]
        playervel[0] *= -0.2

    playervel[1] += 0.2
    playerpos[1] += 1
    if (controller.getkey('w') and collision()): playervel[1] = -6
    playerpos[1] -= 1

    playerpos[1] += playervel[1]
    if (collision()):
        playerpos[1] -= playervel[1]
        playervel[1] *= -0.2

    client.emit('senddata', {
        'name': 'movement',
        'value': {
            'id': clientID,
            'x': playerpos[0],
            'y': playerpos[1]
        }
    })

    window.fill((80, 80, 255))
    cgame.draw.rect((410, 285), (30, 30), (255, 255, 255))

    for obj in objects:
        newX = obj.pos[0] - playerpos[0] + 415
        newY = obj.pos[1] - playerpos[1] + 315
        cgame.draw.rect((newX, newY), obj.size, obj.color)

    for (key, rect) in players.items():
        if (key != clientID):
            newX = rect.pos[0] - playerpos[0] + 410
            newY = rect.pos[1] - playerpos[1] + 285
            cgame.draw.rect((newX, newY), rect.size, rect.color)

newobject(-200, 200, 450, 50)
newobject(200, 0, 50, 200)

window.setloop(update)
window.run()