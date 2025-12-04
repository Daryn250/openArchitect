# grid class: handles physical coordinates to screen coordinates


class Floor:
    def __init__(self, floor_number = 0):
        self.coordinates = [0,0]
        # init rest of stuff
        self.floor_number = floor_number # do not modify until more floors are needed
        
        self.objects = [] # list of all objects on floor. Walls and windows.
        self.decorations = [] # things like furnature.
        self.measurements = [] # eventually for measuring everything with constraints. hideable.

        self.measurements_shown = False # turn off for now. No need to worry about it.


        

    def draw(self):



        for object in self.objects:
            # draw the object
            object.draw()

        for decoration in self.decorations:
            decoration.draw()
        
        for measurement in self.measurements:
            measurement.draw()

    def add_object(self, object):
        self.objects.append(object)
    
        

        