class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __repr__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.z)

    def getplane(self, scene):
        cpos = scene.camera.position

        deltaZ = self.z - cpos.z
        if (deltaZ <= 0): deltaZ = 1e-5

        deltaX = (self.x - cpos.x) * 300 / deltaZ
        deltaY = (self.y - cpos.y) * 300 / deltaZ

        deltaX = scene.screenwidth / 2 + deltaX
        deltaY = scene.screenheight / 2 - deltaY

        return Vector2(deltaX, deltaY)

class Model:
    def __init__(self):
        self.position = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)

        self.vectors = []
        self.pairs = []
        self.faces = []

        self.color = 'white'
        self.outline = 'gray'

    def forward(self, angle=None, scale=1):
        from math import radians, sin, cos
        angle = radians(self.rotation.y) + angle if (angle != None) else radians(self.rotation.y)
        
        return self.position + Vector3(sin(angle) * scale, 0, cos(angle) * scale)

    def _getworldvectors(self):
        mvecs = [self.position + v for v in self.vectors]
        mvecs = self._rotationMatrixY(mvecs)
        return mvecs

    def _rotationMatrixY(self, vectors):
        from math import cos, sin, radians
        angle = radians(self.rotation.y) * -1

        sinAngle = sin(angle)
        cosAngle = cos(angle)

        rotated = []

        for v in vectors:
            vx = v.x - self.position.x
            vy = v.y - self.position.y
            vz = v.z - self.position.z

            newX = vx * cosAngle - vz * sinAngle
            newZ = vz * cosAngle + vx * sinAngle

            rotated.append(Vector3(
                newX + self.position.x,
                vy + self.position.y,
                newZ + self.position.z
            ))

        return rotated

class Controller:
    def __init__(self, scene):
        self._keys = {}
        self._mousepos = Vector2(0, 0)
        self._mousedelta = Vector2(0, 0)
        self._mousedown = False
        self._scene = scene

        self._omcfs = []

        scene._tkWindow.bind('<KeyPress>', self._onkeydown)
        scene._tkWindow.bind('<KeyRelease>', self._onkeyup)
        scene._tkWindow.bind('<Motion>', self._onmousemove)
        scene._tkWindow.bind('<Button-1>', self._onmouseclick)

    def getkey(self, key):
        return self._keys.get(key, False)

    def getmousepos(self):
        return self._mousepos

    def getmousedelta(self):
        return self._mousedelta

    def onmouseclick(self, func):
        self._omcfs.append(func)

    def _onkeydown(self, event):
        self._keys[event.keysym] = True

    def _onkeyup(self, event):
        self._keys[event.keysym] = False

    def _onmousemove(self, event):
        newpos = Vector2(event.x, event.y)
        self._mousedelta = newpos - self._mousepos
        self._mousepos = newpos

        def reset(): self._mousedelta = Vector2(0, 0)
        self._scene._tkWindow.after(1, lambda: reset())

    def _onmouseclick(self, event):
        for func in self._omcfs: func()

class PlaneObjects:
    class Frame:
        def __init__(self, parent, pos, rpos, size, rsize, color):
            from tkinter import Frame as tkFrame
            self._tkinstance = tkFrame(
                parent._tkWindow if (type(parent) == Scene) else parent._tkinstance,
                width=size.x, height=size.y, bg=color)
            self._tkinstance.place(x=pos.x, y=pos.y, relx=rpos.x, rely=rpos.y, relwidth=rsize.x, relheight=rsize.y)

        def setPosition(self, pos, rpos):
            self._tkinstance.place(x=pos.x, y=pos.y)

        def setSize(self, size, rsize):
            self._tkinstance.config(width=size.x, height=size.y)
            self._tkinstance.place(relwidth=rsize.x, relheight=rsize.y)

        def setColor(self, color):
            self._tkinstance.config(bg=color)

    class Text:
        def __init__(self, parent, text, pos, rpos, fcolor, bcolor, fsize):
            from tkinter import Label as tkLabel
            self._tkinstance = tkLabel(
                parent._tkWindow if (type(parent) == Scene) else parent._tkinstance,
                text=text, fg=fcolor, bg=bcolor, font=('Arial', fsize) )
            self._tkinstance.place(x=pos.x, y=pos.y, relx=rpos.x)

        def setText(self, text):
            self._tkinstance.config(text=text)

        def setPosition(self, pos, rpos):
            self._tkinstance.place(x=pos.x, y=pos.y)

        def setFontColor(self, fcolor):
            self._tkinstance.config(fg=fcolor)

        def setBackgroundColor(self, bcolor):
            self._tkinstance.config(bg=bcolor)

        def setFontSize(self, fsize):
            self._tkinstance.config(font=('Arial', fsize))

    class Button:
        def __init__(self, parent, text, pos, rpos, size, rsize, fcolor, bcolor, fsize, command):
            from tkinter import Button as tkButton
            self._tkinstance = tkButton(
                parent._tkWindow if (type(parent) == Scene) else parent._tkinstance,
                text=text, fg=fcolor, bg=bcolor, font=('Arial', fsize), command=command)
            self._tkinstance.place(x=pos.x, y=pos.y, relx=rpos.x, width=size.x, height=size.y, relwidth=rsize.x, relheight=rsize.y)

        def setText(self, text):
            self._tkinstance.config(text=text)

        def setPosition(self, pos, rpos):
            self._tkinstance.place(x=pos.x, y=pos.y)

        def setSize(self, size, rsize):
            self._tkinstance.place(width=size.x, height=size.y, relwidth=rsize.x, relheight=rsize.y)

        def setFontColor(self, fcolor):
            self._tkinstance.config(fg=fcolor)

        def setBackgroundColor(self, bcolor):
            self._tkinstance.config(bg=bcolor)

        def setFontSize(self, fsize):
            self._tkinstance.config(font=('Arial', fsize))

        def setCommand(self, command):
            self._tkinstance.config(command=command)

    class Display:
        def __init__(self, parent, pos, rpos, size, rsize, bcolor):
            from tkinter import Canvas as tkCanvas
            self._tkinstance = tkCanvas(
                parent._tkWindow if (type(parent) == Scene) else parent._tkinstance,
                width=size.x, height=size.y, bg=bcolor)
            self._tkinstance.place(x=pos.x, y=pos.y, relx=rpos.x, width=size.x, height=size.y, relwidth=rsize.x, relheight=rsize.y)

        def setPosition(self, pos, rpos):
            self._tkinstance.place(x=pos.x, y=pos.y)

        def setSize(self, size, rsize):
            self._tkinstance.config(width=size.x, height=size.y)
            self._tkinstance.place(relwidth=rsize.x, relheight=rsize.y)

        def setBackgroundColor(self, bcolor):
            self._tkinstance.config(bg=bcolor)

        def _drawline(self, pos1, pos2, color):
            if (color == None): self._tkinstance.create_line(pos1.x, pos1.y, pos2.x, pos2.y)
            else: self._tkinstance.create_line(pos1.x, pos1.y, pos2.x, pos2.y, fill=color)

        def _drawpoly(self, color, *points):
            newpoints = []
            for point in points:
                newpoints.append(point.x)
                newpoints.append(point.y)

            if (color == None): self._tkinstance.create_polygon(*newpoints)
            else: self._tkinstance.create_polygon(*newpoints, fill=color)

        def clear(self):
            self._tkinstance.delete('all')

from os import environ as _environ
_environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pygame import mixer as _mixer
_mixer.init()

class Sound:
    def __init__(self, file):
        self._sound = _mixer.Sound(file)

    def play(self):
        self._sound.play()

    def stop(self):
        self._sound.stop()

class Scene:
    def __init__(self, size=Vector2(500, 500), title='Razor3D Simulation', fullscreen=False):
        from tkinter import Tk
        self._tkWindow = Tk()
        self._tkWindow.title(title)
        self._tkWindow.geometry('{}x{}'.format(size.x, size.y))

        self.screenwidth = size.x
        self.screenheight = size.y

        self._models = []
        self.camera = Model()
        self.display = None

        if (fullscreen):
            self._tkWindow.attributes('-fullscreen', True)
            self._tkWindow.geometry('{}x{}'.format(self._tkWindow.winfo_screenwidth(), self._tkWindow.winfo_screenheight()))
            self.screenwidth = self._tkWindow.winfo_screenwidth()
            self.screenheight = self._tkWindow.winfo_screenheight()

    def clear(self):
        self.display._tkinstance.delete('all')

    def _rotationMatrixY(self, vectors):
        from math import cos, sin, radians
        angle = radians(self.camera.rotation.y)

        sinAngle = sin(angle)
        cosAngle = cos(angle)

        rotated = []

        for v in vectors:
            vx = v.x - self.camera.position.x
            vy = v.y - self.camera.position.y
            vz = v.z - self.camera.position.z

            newX = vx * cosAngle - vz * sinAngle
            newZ = vz * cosAngle + vx * sinAngle

            rotated.append(Vector3(
                newX + self.camera.position.x,
                vy + self.camera.position.y,
                newZ + self.camera.position.z
            ))

        return rotated

    def addModel(self, model):
        self._models.append(model)

    def removeModel(self, model):
        if (model in self._models):
            self._models.remove(model)

    def renderModel(self, model):
        mvecs = model._getworldvectors()
        mvecs = self._rotationMatrixY(mvecs)

        condition = True
        for v in mvecs:
            if (v.z - self.camera.position.z > 0):
                condition = False
                break
        if (condition): return

        for face in model.faces:
            faces = [mvecs[index].getplane(self) for index in face]
            self.display._drawpoly(model.color, *faces)

        for (a, b) in model.pairs:
            pos1 = mvecs[a].getplane(self)
            pos2 = mvecs[b].getplane(self)
            self.display._drawline(pos1, pos2, model.outline)

    def render(self):
        for model in self._models:
            self.renderModel(model)

    def setloop(self, func=None, capfps=60):
        if (func): func()
        self._tkWindow.after(int(1000 / capfps), lambda: self.setloop(func, capfps))

    def run(self):
        self._tkWindow.mainloop()