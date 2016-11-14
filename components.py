class Drawable:
    def __init__(self, char, color, bgcolor = (0,0,0), depth = 0):
        self.char = char
        self.color = color
        self.bgcolor = bgcolor
        self.depth = depth

class Character:
    def __init__(self):
        self.ready = True

class Solid:
    def __init__(self, volume):
        self.volume = volume

class MoveRight:
    pass
