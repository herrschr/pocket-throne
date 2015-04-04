import pygame

class MapManager:
    _tilesize = 40
    _map = None
    
    def __init__(self, tilemap):
        if tilemap == None:
            return None
        self._map = tilemap

    def pos_to_gui(self,(x,y)):
        gui_x = x * self._tilesize
        gui_y = y * self._tilesize
        return (gui_x, gui_y)
    
    def spawn_unit(self,x,y):
        pass

    def move_unit(self):
        pass

    def spawn_building(self, building,x,y):
        if building == None:
            pass
        else:
            image = pygame.image.load(building.image)
            screen.blit(image, pos_to_gui(x,y))

    def spawn_landscape(self):
        if self.lndscp == "NULL":
            pass
        elif self.lndscp == "M":
            image = pygame.image.load("")
        elif self.lndscp == "F":
            image = pygame.image.load("")
        elif self.lndscp == "G":
            image = pygame.image.load("")
        elif self.lndscp == "D":
            image = pygame.image.load("")
        elif self.lndscp == "W":
            image = pygame.image.load("")
        else:
            print "Fehler. G: Wiese, D: Erde, T: Baum"
        screen.blit(image, (self.gui_x,self.gui_y))
