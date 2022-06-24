import pygame
from pygame.locals import *




game_objects = []





 
class App:
    def __init__(self):
        self.running = True
        self.display = None
        self.size = self.width, self.height = 640, 400
        
 
    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True
        
 
    def on_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.running = False
            
        elif event.type == KEYDOWN:
            if event.key == pygame.K_RIGHT:
                game_objects[0].turn_right()
            elif event.key == pygame.K_LEFT:
                game_objects[0].turn_left()
                
                

            
    def on_loop(self):
        pass

    
    def on_render(self):
        self.screen.fill((100,100,100))

        for gameobject in game_objects:
            gameobject.draw()
            
        pygame.display.flip()
        

        
    def on_cleanup(self):
        pygame.quit()
        
 
    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        player = Player(theApp.width/2, theApp.height/2, theApp)
        
        game_objects.append(player)

        pygame.display.set_caption("JetskiHater")
 
        while( self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
        


class Game_Object:
    def __init__(self, x, y, texture, gamespace):
        self.x_position = x
        self.y_position = y
        self.texture = texture
        self.gamespace = gamespace

    def draw(self):
        theApp.screen.blit(self.texture, (self.x_position,self.y_position))
        
        
    


class Player(Game_Object):
    def __init__(self, x, y, gamespace):
        playertexture = pygame.image.load("Duck_for_game.png")
        super().__init__(x,y, playertexture, gamespace)
        
        self.rotation = 180
        self.ammo = 10
        

    def turn_right(self):
        self.rotation += 1

    def turn_left(self):
        self.rotation -= 1

    def shoot(self):
        self.ammo -= 1
        






if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
