import pygame
from pygame.locals import *
import math
import random




game_objects = []
bullets = []
jetskis = []

fps = 60
fps_clock = pygame.time.Clock()

bullet_speed = 5
turn_speed = 3
spawn_margin = 10
clip_size = 5
refill_rate = 25
spawn_rate = 100
player_hitbox = 25
bullet_hitbox = 10
jetski_hitbox = 10


score = 0
jetski_speed_base = 60
jetski_speed_modifier = 20
jetski_speed = (jetski_speed_base + score)/jetski_speed_modifier



def loss_screen():

    #Fill screen, optional, depends on if you want to see the last frame or not
    theApp.screen.fill((0,94,184))

    font_large = pygame.font.SysFont("helvetica", 100)
    font_small = pygame.font.SysFont("helvetica", 50)

    loss_text = font_large.render("Du förlorade, din poäng var: " + str(score), False, (0, 0, 0))
    continue_text = font_small.render("Tryck Mellanslag för att börja om eller ESC för att avsluta", False, (0, 0, 0))

    loss_text_rect = loss_text.get_rect()
    continue_text_rect = continue_text.get_rect()

    loss_text_rect.center = ((theApp.width/2), (theApp.height/2.5))
    continue_text_rect.center = ((theApp.width/2), (theApp.height/1.8))
    
    theApp.screen.blit(loss_text,loss_text_rect)
    theApp.screen.blit(continue_text,continue_text_rect)
    
    pygame.display.flip()

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                theApp.on_cleanup()
                return
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                theApp.on_restart()
                return
        



def rotate_texture(texture, texture_name, rotation, x_position, y_position):
    old_texture = texture
    new_texture = pygame.transform.rotate(pygame.image.load(texture_name), rotation)
    new_rect = new_texture.get_rect(center = old_texture.get_rect(center = (x_position, y_position)).center)
    
    return new_rect, new_texture
    

def generate_spawnpoints():
    spawn_points = []

    #TODO
    #Optimise this function
        
    for i in range(-spawn_margin, theApp.width + spawn_margin):
        if i == player.x_position:
            continue
        spawn_points.append((i, -spawn_margin))
            
    for i in range(-spawn_margin, theApp.width + spawn_margin):
        if i == player.x_position:
            continue
        spawn_points.append((i, theApp.height+spawn_margin))

    for i in range(-spawn_margin, theApp.height + spawn_margin):
        if i == player.y_position:
            continue
        spawn_points.append((-spawn_margin, i))

    for i in range(-spawn_margin, theApp.height + spawn_margin):
        if i == player.y_position:
            continue
        spawn_points.append((theApp.width+spawn_margin, i))

    return spawn_points


def spawn_jetski(spawn_points, speed):
    array_place = random.randint(0, len(spawn_points)-1)
    new_jetski = Jetski(spawn_points[array_place][0], spawn_points[array_place][1], theApp, speed)
    
    
    
    
    

 
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
            player.turn_right()
        elif keys[pygame.K_LEFT]:
            player.turn_left()



    def update_items(self):
        for bullet in bullets:
            
            bullet.travel()
            if (bullet.getX() < -spawn_margin or bullet.getX() > theApp.width + spawn_margin or bullet.getY() < -spawn_margin or bullet.getY() > theApp.height + spawn_margin):
                game_objects.remove(bullet)
                bullets.remove(bullet)

            bullet.hit_detection()

        for jetski in jetskis:
            jetski.travel()
            if math.sqrt((abs(jetski.getX() - player.getX())**2 + (abs(jetski.getY() - player.getY())**2))) < player_hitbox:
                loss_screen()
                
                #game_objects.remove(jetski)
                #jetskis.remove(jetski)
                
                
                
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

    def on_restart(self):
        while bullets:
            bullets.pop(0)

        while jetskis:
            jetskis.pop(0)

        while game_objects:
            game_objects.pop(0)
                

        global score
        score = 0

        global player
        player = Player((theApp.width/2), (theApp.height/2), theApp)
        
        
        
                
                
 
    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        global player
        player = Player((theApp.width/2), (theApp.height/2), theApp)

        pygame.display.set_caption("JetskiHater")

        spawn_points = generate_spawnpoints()

        
        game_timer = 0
        
        while( self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.key_check()
            self.update_items()
            
            if game_timer % refill_rate == 0:
                player.add_ammo()

            if game_timer == spawn_rate:
                jetski_speed = (jetski_speed_base + score)/jetski_speed_modifier
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
        self.texture = pygame.image.load(texture)
        self.gamespace = gamespace
        self.rect = None

        game_objects.append(self)

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
        self.player_texture = "Duck_for_game.png"
        super().__init__(x,y, self.player_texture, gamespace)
        
        self.direction = 0
        self.ammo = clip_size
        
        self.rect, self.texture = rotate_texture(self.texture, self.player_texture, self.direction, self.x_position, self.y_position)
        

    def turn_right(self):
        self.direction -= turn_speed
        if self.direction > 360:
            self.direction = self.direction - 360

        elif self.direction < 0:
            self.direction = self.direction + 360

        self.rect, self.texture = rotate_texture(self.texture, self.player_texture, self.direction, self.x_position, self.y_position)
            
        

    def turn_left(self):
        self.direction += turn_speed
        if self.direction > 360:
            self.direction = self.direction - 360

        elif self.direction < 0:
            self.direction = self.direction + 360

        self.rect, self.texture = rotate_texture(self.texture, self.player_texture, self.direction, self.x_position, self.y_position)
            
    
        
    def shoot(self):
        if self.ammo > 0:
            self.ammo -= 1
            new_bullet = Bullet(self.x_position, self.y_position, self.gamespace, self.direction)
            

    def add_ammo(self):
        if self.ammo < clip_size:
            self.ammo += 1

    def get_ammo(self):
        return self.ammo

    def set_direction(self, new_direction):
        self.direction = new_direction
        

class Bullet(Game_Object):
    def __init__(self, x, y, gamespace, direction):
        self.bullet_texture = "Bullet.png"
        self.speed = bullet_speed
        self.direction = direction

        bullets.append(self)
        
        super().__init__(x,y,self.bullet_texture,gamespace)

        self.rect, self.texture = rotate_texture(self.texture, self.bullet_texture, self.direction, self.x_position, self.y_position)
        
    def travel(self):
        super().setX(self.x_position - self.speed*(math.sin(math.radians(self.direction))))
        super().setY(self.y_position - self.speed*(math.cos(math.radians(self.direction))))
        self.rect, self.texture = rotate_texture(self.texture, self.bullet_texture, self.direction, self.x_position, self.y_position)

    def hit_detection(self):
        removed_self = False 
        for jetski in jetskis:
            if bullet_hitbox + jetski_hitbox > math.sqrt((jetski.getX() - self.getX())**2 + (jetski.getY() - self.getY())**2):
                if not removed_self:
                    game_objects.remove(self)
                    bullets.remove(self)
                    removed_self = True
                
                game_objects.remove(jetski)                
                jetskis.remove(jetski)
                global score
                score += 1
        
        
class Jetski(Game_Object):
    def __init__(self, x, y, gamespace, speed):
        self.jetski_texture = "TestEnemy.png"
        self.speed = speed

        jetskis.append(self)
        
        super().__init__(x,y,self.jetski_texture,gamespace)

        
        if self.x_position < theApp.width/2:
            self.direction = (270 - ((math.degrees(math.atan((player.getY()-self.y_position)/(player.getX()-self.x_position))))%360))%360
        else:
            self.direction = (90 - ((math.degrees(math.atan((player.getY()-self.y_position)/(player.getX()-self.x_position))))%360))%360

         
            

    def travel(self):
        super().setX(self.x_position - self.speed*(math.sin(math.radians(self.direction))))
        super().setY(self.y_position - self.speed*(math.cos(math.radians(self.direction))))
        self.rect, self.texture = rotate_texture(self.texture, self.jetski_texture, self.direction, self.x_position, self.y_position)




if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
