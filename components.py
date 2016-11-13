class Drawable:
    def __init__(self, char, color, bgcolor = (0,0,0)):
        self.char = char
        self.color = color
        self.bgcolor = bgcolor

class Character:
    def __init__(self):
        self.ready = True

class Solid:
    def __init__(self, volume):
        self.volume = volume

class MoveRight:
    pass
