from __future__ import annotations

class display:
    _canvas = None

    class window:
        def __init__(self, size: (int, int)):
            from tkinter import Tk, Canvas
            self._window = Tk()
            self._window.geometry('{}x{}'.format(size[0], size[1]))
            self._window.title('cubegame')
            self._endloop = False

            self._canvas = Canvas(self._window, width=size[0], height=size[1], bg='black')
            self._canvas.pack()

            display._canvas = self._canvas

        def render(self, instance: objects.rect | objects.text):
            if (type(instance) == objects.rect):
                x, y = instance.pos
                w, h = instance.size
                self._canvas.create_rectangle(x, y, x+w, y+h, fill=instance.color, outline='')
            elif (type(instance) == objects.text):
                x, y = instance.pos
                self._canvas.create_text(x, y, text=instance.text, fill=instance.font[2], font=instance.font[0])

        def setloop(self, func: callable = None, capfps: int | float = 60):
            if (self._endloop):
                self._endloop = False
                return

            if (func): func()
            self._window.after(int(1000 / capfps), lambda: self.setloop(func, capfps))

        def endloop(self):
            self._endloop = True

        def title(self, title: str):
            self._window.title(title)

        def fill(self, color: (int, int, int)):
            hexcolor = '#{:02x}{:02x}{:02x}'.format(*color)
            self._canvas.delete('all')
            self._canvas.configure(bg=hexcolor)

        def run(self):
            self._window.mainloop()

    def convertRGBtoHex(color: (int, int, int)) -> str:
        return '#{:02x}{:02x}{:02x}'.format(*color)

    def getDimension(object: objects.rect | objects.text) -> (int, int):
        if (type(object) == objects.rect):
            return object.size
        elif (type(object) == objects.text):
            from tkinter import font
            tkfont = font.Font(family=object.font[0], size=object.font[1])
            return (tkfont.measure(object.text), tkfont.metrics("linespace"))

class objects:
    class rect:
        def __init__(self, pos: (int, int), size: (int, int), color: (int, int, int)):
            self.pos = pos
            self.size = size
            self.color = '#{:02x}{:02x}{:02x}'.format(*color)

        def setpos(self, pos: (int, int)):
            self.pos = pos

        def setaxis(self, axis: chr, value: int):
            if (axis == 'x'): self.pos = (value, self.pos[1])
            elif (axis == 'y'): self.pos = (self.pos[0], value)

        def setsize(self, size: (int, int)):
            self.size = size

        def setcolor(self, color: (int, int, int)):
            self.color = '#{:02x}{:02x}{:02x}'.format(*color)

        def haspoint(self, point: (int, int)) -> bool:
            sleft = self.pos[0]
            sright = self.pos[0] + self.size[0]
            stop = self.pos[1]
            sbottom = self.pos[1] + self.size[1]
            return (point[0] >= sleft and point[0] <= sright and point[1] >= stop and point[1] <= sbottom)

        def collision(self, other: display.frame) -> bool:
            sleft = self.pos[0]
            sright = self.pos[0] + self.size[0]
            stop = self.pos[1]
            sbottom = self.pos[1] + self.size[1]

            oleft = other.pos[0]
            oright = other.pos[0] + other.size[0]
            otop = other.pos[1]
            obottom = other.pos[1] + other.size[1]

            xbools = (sleft < oright and sright > oleft)
            ybools = (stop < obottom and sbottom > otop)
            xboolo = (oleft < sright and oright > sleft)
            yboolo = (otop < sbottom and obottom > stop)

            sxsy = (xbools and ybools)
            sxoy = (xbools and yboolo)
            oxoy = (xboolo and ybools)
            oxsy = (xboolo and yboolo)
            return (sxsy or sxoy or oxoy or oxsy)

    class text:
        def __init__(self, pos: (int, int), text: str, fontstyle: str = 'Arial', fontsize: int = 16, fontcolor: (int, int, int) = (0, 0, 0)):
            self.pos = pos
            self.text = text
            self.font = (fontstyle, fontsize, '#{:02x}{:02x}{:02x}'.format(*fontcolor))

        def setpos(self, pos: (int, int)):
            self.pos = pos

        def setaxis(self, axis: chr, value: int):
            if axis == 'x':
                self.pos = (value, self.pos[1])
            elif axis == 'y':
                self.pos = (self.pos[0], value)

        def settext(self, text: str):
            self.text = text

        def setfontstyle(self, fontstyle: str):
            self.font = (fontstyle, self.font[1], self.font[2])

        def setfontsize(self, fontsize: int):
            self.font = (self.font[0], fontsize, self.font[2])

        def setfontcolor(self, color: (int, int, int)):
            hexcolor = '#{:02x}{:02x}{:02x}'.format(*color)
            self.font = (self.font[0], self.font[1], hexcolor)

    class ui:
        class button:
            def __init__(self, pos: (int, int), size: (int, int), text: str, fontstyle: str = 'Arial', fontsize: int = 16, fontcolor: (int, int, int) = (255, 255, 255), color: (int, int, int) = (0, 122, 204), onclick: callable = None):
                from tkinter import Button
                self._button = Button(display._canvas, text=text, font=(fontstyle, fontsize), fg='#{:02x}{:02x}{:02x}'.format(*fontcolor), bg='#{:02x}{:02x}{:02x}'.format(*color), command=onclick)
                self._button.place(x=pos[0], y=pos[1], width=size[0], height=size[1])

            def setpos(self, pos: (int, int)):
                self._button.place(x=pos[0], y=pos[1])

            def setaxis(self, axis: chr, value: int):
                if axis == 'x':
                    self._button.place(x=value)
                elif axis == 'y':
                    self._button.place(y=value)

            def setsize(self, size: (int, int)):
                self._button.place(width=size[0], height=size[1])

            def settext(self, text: str):
                self._button.config(text=text)

            def setfontstyle(self, fontstyle: str):
                self._button.config(font=(fontstyle, self._button.cget('font')[1]))

            def setfontsize(self, fontsize: int):
                self._button.config(font=(self._button.cget('font')[0], fontsize))

            def setfontcolor(self, color: (int, int, int)):
                hexcolor = '#{:02x}{:02x}{:02x}'.format(*color)
                self._button.config(fg=hexcolor)

            def setcolor(self, color: (int, int, int)):
                hexcolor = '#{:02x}{:02x}{:02x}'.format(*color)
                self._button.config(bg=hexcolor)

            def setonclick(self, onclick: callable):
                self._button.config(command=onclick)

            def destroy(self):
                self._button.destroy()

        class inputbox:
            def __init__(self, pos: (int, int), size: (int, int), fontstyle: str = 'Arial', fontsize: int = 16, fontcolor: (int, int, int) = (255, 255, 255), color: (int, int, int) = (0, 122, 204)):
                from tkinter import Entry
                self._entry = Entry(display._canvas, font=(fontstyle, fontsize), fg='#{:02x}{:02x}{:02x}'.format(*fontcolor), bg='#{:02x}{:02x}{:02x}'.format(*color))
                self._entry.place(x=pos[0], y=pos[1], width=size[0], height=size[1])

            def setpos(self, pos: (int, int)):
                self._entry.place(x=pos[0], y=pos[1])

            def setaxis(self, axis: chr, value: int):
                if axis == 'x':
                    self._entry.place(x=value)
                elif axis == 'y':
                    self._entry.place(y=value)

            def setsize(self, size: (int, int)):
                self._entry.place(width=size[0], height=size[1])

            def setfontstyle(self, fontstyle: str):
                self._entry.config(font=(fontstyle, self._entry.cget('font')[1]))

            def setfontsize(self, fontsize: int):
                self._entry.config(font=(self._entry.cget('font')[0], fontsize))

            def setfontcolor(self, color: (int, int, int)):
                hexcolor = '#{:02x}{:02x}{:02x}'.format(*color)
                self._entry.config(fg=hexcolor)

            def setcolor(self, color: (int, int, int)):
                hexcolor = '#{:02x}{:02x}{:02x}'.format(*color)
                self._entry.config(bg=hexcolor)

            def gettext(self) -> str:
                return self._entry.get()

            def settext(self, text: str):
                self._entry.delete(0, 'end')
                self._entry.insert(0, text)

            def destroy(self):
                self._entry.destroy()

        def clearui():
            for widget in display._canvas.winfo_children():
                widget.destroy()

class draw:
    def line(start: (int, int), end: (int, int), color: (int, int, int) = (255, 255, 255)):
        display._canvas.create_line(start[0], start[1], end[0], end[1], fill=display.convertRGBtoHex(color))

    def rect(pos: (int, int), size: (int, int), color: (int, int, int) = (255, 255, 255)):
        try: color = display.convertRGBtoHex(color)
        except Exception as e: pass
        display._canvas.create_rectangle(pos[0], pos[1], pos[0]+size[0], pos[1]+size[1], fill=color, outline='')

    def polygon(points: [(int, int)], color: (int, int, int) = (255, 255, 255)):
        flat_points = [coord for point in points for coord in point]
        display._canvas.create_polygon(flat_points, fill=display.convertRGBtoHex(color), outline='')

    def text(pos: (int, int), text: str, fontstyle: str = 'Arial', fontsize: int = 16, fontcolor: (int, int, int) = (255, 255, 255)):
        display._canvas.create_text(pos[0], pos[1], text=text, fill=display.convertRGBtoHex(fontcolor), font=(fontstyle, fontsize))

class controller:
    def __init__(self):
        self._keys = {}
        self._mousepos = (0, 0)
        self._mousedelta = (0, 0)
        self._mousebuttons = {'left': False, 'right': False, 'middle': False}

        from tkinter import _default_root
        _default_root.bind('<KeyPress>', self._onkeypress)
        _default_root.bind('<KeyRelease>', self._onkeyrelease)
        _default_root.bind('<Motion>', self._onmousemove)
        _default_root.bind('<ButtonPress>', self._onmousebuttonpress)
        _default_root.bind('<ButtonRelease>', self._onmousebuttonrelease)

    def getkey(self, key: chr) -> bool:
        return self._keys.get(key, False)

    def getmousepos(self) -> (int, int):
        return self._mousepos

    def getmousedelta(self) -> (int, int):
        return self._mousedelta

    def getmousebutton(self, button: str) -> bool:
        return self._mousebuttons.get(button, False)

    def onkeypress(self, key: char, handler: callable):
        def wrapper(event):
            if (event.keysym == key):
                handler()

        from tkinter import _default_root
        _default_root.bind('<KeyPress>', wrapper)

    def onkeyrelease(self, key: char, handler: callable):
        def wrapper(event):
            if (event.keysym == key):
                handler()

        from tkinter import _default_root
        _default_root.bind('<KeyRelease>', wrapper)

    def onmousemove(self, handler: callable):
        from tkinter import _default_root
        _default_root.bind('<Motion>', lambda event: handler(self._mousepos, self._mousedelta))

    def onmousebuttonpress(self, button: str, handler: callable):
        def wrapper(event):
            if ((button == 'left' and event.num == 1) or (button == 'middle' and event.num == 2) or (button == 'right' and event.num == 3) or button == 'any'):
                handler()

        from tkinter import _default_root
        _default_root.bind('<ButtonPress>', wrapper)

    def _onkeypress(self, event):
        self._keys[event.keysym] = True

    def _onkeyrelease(self, event):
        self._keys[event.keysym] = False

    def _onmousemove(self, event):
        new_mousepos = (event.x, event.y)
        self._mousedelta = (new_mousepos[0] - self._mousepos[0], new_mousepos[1] - self._mousepos[1])
        self._mousepos = new_mousepos

    def _onmousebuttonpress(self, event):
        if (event.num == 1): self._mousebuttons['left'] = True
        elif (event.num == 2): self._mousebuttons['middle'] = True
        elif (event.num == 3): self._mousebuttons['right'] = True

    def _onmousebuttonrelease(self, event):
        if (event.num == 1): self._mousebuttons['left'] = False
        elif (event.num == 2): self._mousebuttons['middle'] = False
        elif (event.num == 3): self._mousebuttons['right'] = False

class time:
    def after(ms: float, handler: callable):
        from tkinter import _default_root
        _default_root.after(int(ms), handler)