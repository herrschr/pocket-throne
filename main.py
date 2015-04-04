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

    def img_lndscp
        
        

class TileMap:
    TILES_SIZE = 40
    _id = -1
    tiles = []
    tiles_at = {}
    
    def __init__(self):
        pass

class MapLoader:
    pass

    

