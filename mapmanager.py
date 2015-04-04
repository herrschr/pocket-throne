class MapManager:
    pass

    def spawn_unit(self):
        pass

    def move_unit(self):
        pass

    def spawn_building(self):
        pass

    def spawn_landscape(self):
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
