import pygame
from pygame.locals import *
import math
import random




game_objects = []
bullets = []
jetskis = []

fps = 60
fps_clock = pygame.time.Clock()

bullet_speed = 4
turn_speed = 2
spawn_margin = 10
clip_size = 5
refill_rate = 100
spawn_rate = 200
player_hitbox = 10


score = 0
jetski_speed = (100 + score)/10


def generate_spawnpoints():
    spawn_points = []
        
    for i in range(-spawn_margin, theApp.width + spawn_margin):
        spawn_points.append((i, -spawn_margin))
            
    for i in range(-spawn_margin, theApp.width + spawn_margin):
        spawn_points.append((i, theApp.height+spawn_margin))

    for i in range(-spawn_margin, theApp.height + spawn_margin):
        spawn_points.append((-spawn_margin, i))

    for i in range(-spawn_margin, theApp.height + spawn_margin):
        spawn_points.append((theApp.width+spawn_margin, i))

    return spawn_points


def spawn_jetski(spawn_points, speed):
    array_place = random.randint(0, len(spawn_points)-1)
    new_jetski = Jetski(spawn_points[array_place][0], spawn_points[array_place][1], theApp, speed)
    jetskis.append(new_jetski)
    game_objects.append(new_jetski)
    
    

 
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



    def move_items(self):
        for bullet in bullets:
            bullet.travel()
            if (bullet.getX() < -spawn_margin or bullet.getX() > theApp.width + spawn_margin or bullet.getY() < -spawn_margin or bullet.getY() > theApp.height + spawn_margin):
                game_objects.remove(bullet)
                bullets.remove(bullet)

        for jetski in jetskis:
            jetski.travel()
            if math.sqrt((abs(jetski.getX() - player.getX())**2 + (abs(jetski.getY() - player.getY())**2))) < player_hitbox:
                game_objects.remove(jetski)
                jetskis.remove(jetski)
                
                
                
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
        ammo_text = font.render("Raketer: " + str(player.get_ammo()), False, (0, 0, 0))
        score_text = font.render("Poäng: " + str(score), False, (0, 0, 0))
        theApp.screen.blit(ammo_text,(0,0))
        theApp.screen.blit(score_text,(0,50))
        
            
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

        spawn_points = generate_spawnpoints()

        
        game_timer = 0
        
        while( self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.key_check()
            self.move_items()
            
            if game_timer % refill_rate == 0:
                player.add_ammo()

            if game_timer == spawn_rate:
                spawn_jetski(spawn_points, jetski_speed)
                game_timer = 0
                
            self.on_loop()
            self.on_render()
            fps_clock.tick(fps)
            
            game_timer += 1
            
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
        self.rotation -= turn_speed
        if self.rotation > 360:
            self.rotation = self.rotation - 360

        elif self.rotation < 0:
            self.rotation = self.rotation + 360
            
        old_texture = self.texture
        self.texture = pygame.transform.rotate(pygame.image.load("Duck_for_game.png"), self.rotation)
        new_rect = self.texture.get_rect(center = old_texture.get_rect(center = (self.x_position, self.y_position)).center)
        self.rect = new_rect

    def turn_left(self):
        self.rotation += turn_speed
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
        
        super().__init__(x,y,texture,gamespace)
        
    def travel(self):
        super().setX(self.x_position - self.speed*(math.sin(math.radians(self.direction))))
        super().setY(self.y_position - self.speed*(math.cos(math.radians(self.direction))))
        
        
class Jetski(Game_Object):
    def __init__(self, x, y, gamespace, speed):
        texture = pygame.image.load("TestEnemy.png")
        self.speed = speed
        
        super().__init__(x,y,texture,gamespace)

        self.direction = math.degrees(math.atan((player.getX()-self.x_position)/(player.getY()-self.y_position)))

        print(self.direction)
        print(self.x_position)
        print(self.y_position)
        print("______")
        print(abs(player.getX()-self.x_position))
        print(abs(player.getY()-self.y_position))

    def travel(self):
        super().setX(self.x_position + self.speed*(math.sin(math.radians(self.direction))))
        super().setY(self.y_position + self.speed*(math.cos(math.radians(self.direction))))




if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
