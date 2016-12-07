class Drawable:
    def __init__(self, char, color, bgcolor = (0,0,0), depth = 0):
        self.char = char
        self.color = color
        self.bgcolor = bgcolor
        self.depth = depth

class Character:
    def __init__(self):
        self.ready = True

# Component for objects that are physical (Pretty much every non-gas object)
# Volume is measured in m3
# Weight is measured in kg
class Physical:
    def __init__(self, volume, weight):
        self.volume = volume
        self.weight = weight

class MoveRight:
    pass
