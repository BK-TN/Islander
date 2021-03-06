import components

class Entity:
    def __init__(self, name, components):
        self.name = name
        self.components = components
        self.actions = []

    # Returns a component with the specified type if it is found
    def get(self, comp_type):
        for comp in self.components:
            if type(comp) is comp_type:
                return comp
        return None

    # Checks if the entity has a component type without returning it
    def has(self, comp_type):
        return self.get(comp_type) != None

    # Gives an action to this entity for other systems to read
    def give_action(self, action):
        self.actions.append(action)

    # Gets a list of actions given to this entity of the specified action type
    def get_actions(self, action_type):
        result = []
        for action in self.actions:
            if type(action) is action_type:
                result.append(action)
        return result

    def clear_actions(self):
        self.actions = []

def player():
    return Entity("John McJohn", [
        components.Drawable('@',(255,255,255)),
        components.Character(),
        components.Physical(0.25, 80)
    ])

def rock():
    return Entity("rock", [
        components.Drawable('#', (128,128,128), bgcolor = (96,96,96)),
        components.Physical(1, 2500)
    ])

def dirt():
    return Entity("dirt", [
        components.Drawable('~', (165,42,42), bgcolor = (64,16,16)),
        components.Physical(1, 1500)
    ])

def water():
    return Entity("water", [
        components.Drawable("~", (32,64,255))
    ])

def grass():
    return Entity("grass", [
        components.Drawable('.', (10,150,10), bgcolor = (16,32,16), depth = 1),
    ])

def moveright():
    return Entity("i wanna moveright", [
        components.Drawable('>',(0,255,0)),
        components.MoveRight(),
        components.Physical(0.25, 50)
    ])
