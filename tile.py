import pygame

class Tile:
    _id = -1
    pos_x = -1
    pos_y = -1
    gui_x = -1
    gui_y = -1
    lndscp = "NULL"

    def __init__(self):
        pass

    def initial(self,x,y,lndscp):
        self.gui_x = TILES_SIZE * x
        self.gui_y = TILES_SIZE * y
        self.pos_x = x
        self.pos_y = y
        self.lndscp = lndscp

    def img_lndscp():
        if self.lndscp == "NULL":
            pass
        elif self.lndscp == "G":
            image = pygame.image.load("")
        elif self.lndscp == "D":
            image = pygame.image.load("")
        elif self.lndscp == "T":
            image = pygame.image.load("")
        else:
            print "Fehler. G: Wiese, D: Erde, T: Baum"
        screen.blit(image, (self.gui_x,self.gui_y))
