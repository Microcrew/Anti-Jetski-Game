import pygame
from pygame.locals import *
import math




game_objects = []
bullets = []

bullet_speed = 0.2
turn_speed = 0.3
spawn_margin = 10
clip_size = 5





 
class App:
    def __init__(self):
        self.running = True
        self.display = None
        self.size = self.width, self.height = 1280, 800
        
 
    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.running = True
        
 
    def on_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.running = False

        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            player.shoot()

            
        #elif event.type == KEYDOWN:
            #if event.key == pygame.K_RIGHT:
                #game_objects[0].turn_right()
            #elif event.key == pygame.K_LEFT:
                #game_objects[0].turn_left()

            

    def key_check(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            game_objects[0].turn_right()
        elif keys[pygame.K_LEFT]:
            game_objects[0].turn_left()



    def move_bullets(self):
        for item in bullets:
            item.travel()
            if (item.getX() < -spawn_margin or item.getX() > theApp.width + spawn_margin or item.getY() < -spawn_margin or item.getY() > theApp.height + spawn_margin):
                game_objects.remove(item)
                bullets.remove(item)
                
                
                
    def on_loop(self):
        pass

    
    def on_render(self):

        #Draw sea
        self.screen.fill((0,94,184))

        
        #Draw all Game Objects
        for gameobject in game_objects:
            gameobject.draw()

        #Draw UI
        font = pygame.font.SysFont("helvetica", 40)
        text2 = font.render("Raketer: " + str(player.get_ammo()), False, (0, 0, 0))
        theApp.screen.blit(text2,(0,0))
        
            
        pygame.display.flip()
        

        
    def on_cleanup(self):
        pygame.quit()
        
 
    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        global player
        player = Player((theApp.width/2), (theApp.height/2), theApp)
        
        game_objects.append(player)

        pygame.display.set_caption("JetskiHater")
        
        ammo_regen = 0
        
        while( self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.key_check()
            self.move_bullets()
            
            if ammo_regen == 1000:
                player.add_ammo()
                ammo_regen = 0
                
            self.on_loop()
            self.on_render()
            
            ammo_regen += 1
            
        self.on_cleanup()
        


class Game_Object:
    def __init__(self, x, y, texture, gamespace):
        self.x_position = x
        self.y_position = y
        self.texture = texture
        self.gamespace = gamespace
        self.rect = None

    def draw(self):
        if self.rect == None:
            theApp.screen.blit(self.texture, (self.x_position,self.y_position))
        else:
            theApp.screen.blit(self.texture, self.rect)

    def setX(self, x):
        self.x_position = x

    def setY(self, y):
        self.y_position = y

    def getX(self):
        return self.x_position

    def getY(self):
        return self.y_position
            
        
        
    


class Player(Game_Object):
    global playertexture
    def __init__(self, x, y, gamespace):
        playertexture = pygame.image.load("Duck_for_game.png")
        super().__init__(x,y, playertexture, gamespace)
        
        self.rotation = 0
        self.ammo = clip_size
        

    def turn_right(self):
        self.rotation += turn_speed
        if self.rotation > 360:
            self.rotation = self.rotation - 360

        elif self.rotation < 0:
            self.rotation = self.rotation + 360
            
        old_texture = self.texture
        self.texture = pygame.transform.rotate(pygame.image.load("Duck_for_game.png"), self.rotation)
        new_rect = self.texture.get_rect(center = old_texture.get_rect(center = (self.x_position, self.y_position)).center)
        self.rect = new_rect

    def turn_left(self):
        self.rotation -= turn_speed
        if self.rotation > 360:
            self.rotation = self.rotation - 360

        elif self.rotation < 0:
            self.rotation = self.rotation + 360
            
        old_texture = self.texture
        self.texture = pygame.transform.rotate(pygame.image.load("Duck_for_game.png"), self.rotation)
        new_rect = self.texture.get_rect(center = old_texture.get_rect(center = (self.x_position, self.y_position)).center)
        self.rect = new_rect
        
    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            new_bullet = Bullet(self.x_position, self.y_position, self.gamespace, self.rotation)
            bullets.append(new_bullet)
            game_objects.append(new_bullet)

    def add_ammo(self):
        if self.ammo < clip_size:
            self.ammo += 1

    def get_ammo(self):
        return self.ammo
        

class Bullet(Game_Object):
    def __init__(self, x, y, gamespace, direction):
        texture = pygame.image.load("Bullet.png")
        self.speed = bullet_speed
        self.direction = direction

        self.bull_array_placement = 0
        self.game_array_placement = 0
        super().__init__(x,y,texture,gamespace)
        
    def travel(self):
        super().setX(self.x_position - self.speed*(math.sin(math.radians(self.direction))))
        super().setY(self.y_position - self.speed*(math.cos(math.radians(self.direction))))
        





if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
