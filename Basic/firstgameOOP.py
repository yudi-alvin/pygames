
import pygame
pygame.init() #initialized the game

win = pygame.display.set_mode((500, 500))
# This line creates a window of 500 width, 500 height
pygame.display.set_caption("First Game")



walkRight = [pygame.image.load('pic\R1.png'), pygame.image.load('pic\R2.png'), pygame.image.load('pic\R3.png'), pygame.image.load('pic\R4.png'), pygame.image.load('pic\R5.png'), pygame.image.load('pic\R6.png'), pygame.image.load('pic\R7.png'), pygame.image.load('pic\R8.png'), pygame.image.load('pic\R9.png')]
walkLeft = [pygame.image.load('pic\L1.png'), pygame.image.load('pic\L2.png'), pygame.image.load('pic\L3.png'), pygame.image.load('pic\L4.png'), pygame.image.load('pic\L5.png'), pygame.image.load('pic\L6.png'), pygame.image.load('pic\L7.png'), pygame.image.load('pic\L8.png'), pygame.image.load('pic\L9.png')]
bg = pygame.image.load('pic/bg.jpg')
char = pygame.image.load('pic/standing.png')

clock = pygame.time.Clock()

#music & sounds
bulletSound = pygame.mixer.Sound("music/bullet.wav")
hitSound = pygame.mixer.Sound("music/hit.wav")
music = pygame.mixer.music.load("music/music.mp3")
pygame.mixer.music.play(-1)

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.vel = 5
        self.isJump = False
        self.jumpCount=10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28, 60)

    def draw(self, win):
        
        if self.walkCount  +1 >= 27:
            self.walkCount = 0

        if (not self.standing):
            if self.left:  # If we are facing left
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))  # We integer divide walkCounr by 3 to ensure each
                self.walkCount += 1                           # image is shown 3 times every animation
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(walkLeft[0], (self.x,self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y+9, 28, 60)
        # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self, enemy):
        
        
        self.walkCount= 0
        font1 = pygame.font.SysFont("comicsans", 30)
        damage = -enemy.attack
        text = font1.render(str(damage), 1, (255,0,0))
        #win.blit(text, (500/2 - (text.get_width()/2),200))#middle of the screen
        win.blit(text, (self.x+20, self.y ))
        #knockback
        if self.left == True:
            direction = -1
        else:
            direction = 1
        self.x = self.x - 70 *direction
        pygame.display.update()
        #delay
        i =0
        while i < 50:
            pygame.time.delay(10)
            i +=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i=301
                    pygame.quit()
        
        

class goblin(object):
    walkRight = [pygame.image.load('pic/R1E.png'), pygame.image.load('pic/R2E.png'), pygame.image.load('pic/R3E.png'), pygame.image.load('pic/R4E.png'), pygame.image.load('pic/R5E.png'), pygame.image.load('pic/R6E.png'), pygame.image.load('pic/R7E.png'), pygame.image.load('pic/R8E.png'), pygame.image.load('pic/R9E.png'), pygame.image.load('pic/R10E.png'), pygame.image.load('pic/R11E.png')]
    walkLeft = [pygame.image.load('pic/L1E.png'), pygame.image.load('pic/L2E.png'), pygame.image.load('pic/L3E.png'), pygame.image.load('pic/L4E.png'), pygame.image.load('pic/L5E.png'), pygame.image.load('pic/L6E.png'), pygame.image.load('pic/L7E.png'), pygame.image.load('pic/L8E.png'), pygame.image.load('pic/L9E.png'), pygame.image.load('pic/L10E.png'), pygame.image.load('pic/L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 200
        self.healthBar = True
        self.attack=50
        
    
    def draw(self, win):
        if self.healthBar:
            self.move()
            if self.walkCount +1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount +=1
            
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] -20, 50, 10))
            pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] -20, 50 - (0.25 * (200-self.health)), 10))

            self.hitbox = (self.x + 17, self.y, 35, 60)
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2) #hitbox

    
    def move(self):
        if self.vel > 0:
            if self.x  < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel *-1
                self.x += self.vel
                self.walkCount=0
        else:
            if self.x > self.path[0]  - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel *-1
                self.x += self.vel
                self.walkCount=0

    def hit(self, weapon):
        if self.health > 0:
            self.health -= weapon.damage
        if self.health <= 0:
            self.healthBar = False
        # print("hit")
        


class projectile():
    def __init__(self, x, y, colour, direction,radius=6):#add take in weapon class
        self.x = x
        self.y = y
        self.colour = colour
        self.radius = radius
        self.direction = direction
        self.vel = 9 * direction #1 -1
        self.damage = 100 #weapon.damage
    
    def draw(self, win):
        pygame.draw.circle(win, self.colour, (self.x,self.y), self.radius)






def drawGame():

    win.blit(bg, (0,0))
    player1.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    text = font.render("Score" + str(score), 1, (0,0,0))
    win.blit(text, (380,10))
    pygame.display.update() 


font = pygame.font.SysFont("comicsans", 30, True, True) #style, size, B,I
player1 = player(50, 400, 64, 64)
run = True
bullets=[]
goblin = goblin(300, 407, 64, 64, 400)
shoot=0
score =0
###################### MAIN########################
while run:
    clock.tick(27)#frame rate
    for event in pygame.event.get():#track all the events
        #set up the quit button
        if event.type == pygame.QUIT:
            run = False

    if goblin.healthBar==True:
        if player1.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and player1.hitbox[1] + player1.hitbox[3] > goblin.hitbox[1] :
            if player1.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and player1.hitbox[0] + player1.hitbox[2]> goblin.hitbox[0]:
                player1.hit(goblin)
                score -= 50

    #for projectile
    for bullet in bullets:
        if goblin.healthBar==True:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1] :
                if bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius > goblin.hitbox[0]:
                    hitSound.play()
                    goblin.hit(bullet)
                    score += bullet.damage
                    bullets.pop(bullets.index(bullet))
        
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

        #check if the bullet hit
        #check y axis
    #for melee weapon
     

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and shoot %3 == 0:
        bulletSound.play()
        if player1.left:
            direction =-1
        else:
            direction = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(player1.x + player1.width //2), round(player1.y + player1.height//2),(0,0,0),direction))
    shoot+=1

    if keys[pygame.K_LEFT] and player1.x > player1.vel:
        player1.x -= player1.vel
        player1.left = True
        player1.right = False
        player1.standing = False

    elif keys[pygame.K_RIGHT] and player1.x < 500 - player1.width - player1.vel:
        player1.x += player1.vel
        player1.right = True
        player1.left = False
        player1.standing = False
    else: # If the character is not moving we will set both left and right false and reset the animation counter (walkCount)
        player1.standing= True
        player1.walkCount = 0

    if not(player1.isJump):
        if keys[pygame.K_UP]:
            player1.isJump=True
            player1.walkCount = 0
    else:
        if player1.jumpCount >= -10:
            neg = 1
            if player1.jumpCount <0:
                neg = -1
            player1.y -= (player1.jumpCount **2)*0.3 * neg
            player1.jumpCount -=1
        else:
            player1.isJump = False
            player1.jumpCount =10
    drawGame()

pygame.quit()  # If we exit the loop this will execute and close our game