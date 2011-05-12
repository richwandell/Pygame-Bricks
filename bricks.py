import pygame, sys, time, random
from pygame.locals import *
import math

if not pygame.mixer: print 'Warning, sound disabled'

pygame.init()
screen = pygame.display.set_mode((0,0),
                                 pygame.FULLSCREEN
                                 )
pygame.display.set_caption('Rich bricks')
white = [255,255,255]
black = [0,0,0]
clock = pygame.time.Clock()
width = screen.get_width()
height = screen.get_height()
pygame.mixer.init
bgmusic = pygame.mixer.Sound('eye_of_the_tiger.wav')
brickhit = pygame.mixer.Sound('brick_hit.wav')
bgmusic.play()
game_over = False
pygame.mouse.set_visible(False)
score = 0
deg = 0


#forward or backward global used for bricks movement direction
global fb
fb = True

class kinect(pygame.sprite.Sprite):
    def __init__(self, xPosition, yPosition):
        pygame.sprite.Sprite.__init__(self)
        self.old = (0,0,0,0)
        self.image = pygame.image.load('kinect.gif')
        self.rect = self.image.get_rect()
        self.rect.center = xPosition, yPosition
        

    def update(self,xPos):
        self.old = self.rect
        self.rect = self.rect.move([xPos-self.rect.x-160, 0])
        
class brick(pygame.sprite.Sprite):
    def __init__(self, xPosition, yPosition):
        global fb
        pygame.sprite.Sprite.__init__(self)
        self.old = (0,0,0,0)
        self.image = pygame.image.load('brick.gif')
        self.image = pygame.transform.scale(self.image, (width/13, height/15))
        self.rect = self.image.get_rect()
        self.rect.topleft = xPosition, yPosition

    def update(self):
        global fb
        self.old = self.rect
        if fb == True:
            self.rect = self.rect.move([width/720,0])
        elif fb == False:
            self.rect = self.rect.move([-width/720,0])

        if self.rect.x > width-100:
            fb = False
        elif self.rect.x < 2:
            fb = True

class ball(pygame.sprite.Sprite):
    def __init__(self,xPosition,yPosition):
        
        pygame.sprite.Sprite.__init__(self)
        self.old = (0,0,0,0)
        self.img_src = pygame.image.load('golfball.gif')
        self.image = self.img_src
        self.rect = self.image.get_rect()
        self.rect.topleft = width/2, height/2
        self.fb = True
        self.du = False
        self.speed = width/720

    def update(self):
        global game_over, deg
        self.old = self.rect

        if self.fb == True:
            self.image = pygame.transform.rotate(self.img_src, -deg)
        else:
            self.image = pygame.transform.rotate(self.img_src, deg)

        if deg == 360: deg = 1
        deg+=2
        
        if self.fb == True:
            self.rect = self.rect.move([self.speed,0])
        else:
            self.rect = self.rect.move([-self.speed,0])
            
        if self.du == True:
            self.rect = self.rect.move([0,width/144])
        else:
            self.rect = self.rect.move([0,-width/144])

        if self.rect.x > width-10:
            self.fb = False
        elif self.rect.x < 0:
            self.fb = True
        if self.rect.y > height:
            game_over = True
            
        elif self.rect.y < 0:
            self.du = True


        
def eraseSprite(screen, rect):
   screen.blit(blank, rect)

        

def menu():
    global screen, black, white
    screen.fill(black)
    font = pygame.font.Font(None, 32)
    screen.blit(font.render('duhhh... wtf man,... hit return', True, white, black),
                [0,0])
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not event.key == pygame.K_ESCAPE:
                    if event.key == pygame.K_RETURN:
                        newGame()
                
                else:
                    pygame.quit()
                    sys.exit()


def newGame():
    global game_over, score
    score = 0
    x,y = screen.get_width(), screen.get_height()
    
    bg_ = pygame.image.load('bg.gif').convert()
    bg = pygame.transform.scale(bg_, (width,height))
    g_over = pygame.image.load('game_over.gif')
    g_over = pygame.transform.scale(g_over, (width, height))

    bricks = []
    for z in range(7):
        bricks.append(brick((x/13)*(z+3),(y/15)*1))

    for z in range(7):
        bricks.append(brick((x/13)*(z+3),(y/15)*2))

    for z in range(7):
        bricks.append(brick((x/13)*(z+3),(y/15)*3))

    for z in range(7):
        bricks.append(brick((x/13)*(z+3),(y/15)*4))
        
    brickgroup = pygame.sprite.RenderPlain(bricks)
    k1 = kinect(x/2,y-150)
    kgroup = pygame.sprite.RenderPlain(k1)
    b1 = ball(x/2,y/2)
    bgroup = pygame.sprite.RenderPlain(b1)

    for z in range(6,0,-1):
        font = pygame.font.Font(None, 32)
        screen.blit(font.render("%d"%z, True, white, black), [x/2,y/2])
        pygame.display.flip()
        clock.tick(1)
    
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#check if user closes application
                running = False
            elif event.type == pygame.MOUSEMOTION:
                mx,my = pygame.mouse.get_pos()
                kgroup.update(mx)
            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_RETURN:
                    game_over = False
                    menu()
                    score = 0
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
                
            
                
        
        if not game_over: 
            screen.fill(black)#clear the screen
            screen.blit(bg, (0,0))#draw background
            font = pygame.font.Font(None, 32)
            screen.blit(font.render("Score: %d"% score, True, white, black), [x/2,5])

            bgroup.update()
            brickgroup.update()
            
            brickgroup.draw(screen)
            kgroup.draw(screen)
            bgroup.draw(screen)

            pygame.display.flip()
             
            if pygame.sprite.spritecollide(b1,brickgroup, True) != []:
                brickhit.play()
                score+=30
                
                
                for z in bricks:
                    if b1.rect.right <= z.rect.left+2:
                        b1.fb = False
                    elif b1.rect.left >= z.rect.right-2:
                        b1.fb = True

                
                if b1.du == True:
                    b1.du = False
                else:
                    b1.du = True

                    
            elif pygame.sprite.spritecollide(b1, kgroup, False) != []:
                if b1.rect.left <= k1.rect.left+30:
                    b1.speed = x/144
                    b1.fb = False
                elif b1.rect.right >= k1.rect.right-30:
                    b1.speed = x/144
                    b1.fb = True
                else:
                    b1.speed = x/720

                    
                if b1.du == True:
                    b1.du = False
                else:
                    b1.du = True
        else:
            screen.blit(g_over, (0,0))#draw background
            pygame.display.flip()
        

if __name__ == '__main__':
    menu()
