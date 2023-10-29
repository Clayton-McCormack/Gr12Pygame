from ImageLoad import *
from StartAndWin import *
import pygame, sys, csv

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # initiates pygame
pygame.font.init()

pygame.display.set_caption('Jump King') #Caption

WINDOW_SIZE = (900,600) #Window size

screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window

#Initiating font for timer
game_font = pygame.font.SysFont('comicsans',20)


#Setting variables
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
frame = 0
counter = 0
jump_counter = 0
gametimer = 0
jump = False
bounce = False
start = True
win = False
direction = 'left'

scroll = 1017 #Scrolling

class player():
    def __init__(self,x,y,name):
        #Getting starting position, name of image, and loading image of the character
        self.x = x
        self.y = y
        self.name = name
        self.image = pygame.image.load(name).convert()

    def animation(self):

        #Globalling these variable so they can change easily
        global player_rect, counter, frame, direction, moving_left, moving_right, jump, air_timer, bounce, walkLeft, walkRight, RHit, LHit, fallL, fallR, jumpL, jumpR, myPlayer

        #If you're facing left, on the ground, and not trying to jump, blit the facing left image
        if direction == 'left' and moving_right == False and moving_left == False and jump == False and air_timer <= 6:
            rectangleResizer(player_rect,walkLeft[0])
            display.blit(walkLeft[0],(player_rect.x,player_rect.y-scroll))

        #Same as above just right
        if direction == 'right' and moving_right == False and moving_left == False and jump == False and air_timer <= 6:
            rectangleResizer(player_rect,walkRight[0])
            display.blit(walkRight[0],(player_rect.x,player_rect.y-scroll))

        #If you're moving left, on the ground, and not trying to jump, blit the walking left cycle
        if moving_left == True and moving_right == False and jump == False and air_timer <= 6:
            rectangleResizer(player_rect,walkLeft[frame])
            display.blit(walkLeft[frame],(player_rect.x,player_rect.y-scroll))

        #Same as above just right
        if moving_right == True and moving_left == False and jump == False and air_timer <= 6:
            rectangleResizer(player_rect,walkRight[frame])
            display.blit(walkRight[frame],(player_rect.x,player_rect.y-scroll))

        #If you're in the air, facing right, and falling blit the right facing fall image
        if air_timer > 6 and direction == 'right' and vertical_momentum > 0:
            display.blit(fallR,(player_rect.x,player_rect.y-scroll))

        #Same as above just left
        if air_timer > 6 and direction == 'left' and vertical_momentum > 0:
            display.blit(fallL,(player_rect.x,player_rect.y-scroll))

        #If you're facing left and bounced, blit the character being hit on the right
        if direction == 'left' and bounce == True:
            display.blit(RHit,(player_rect.x,player_rect.y-scroll))

        #Same as above just opposite direction
        if direction == 'right' and bounce == True:
            display.blit(LHit,(player_rect.x,player_rect.y-scroll))

        #If you're facing left, jumping, and not bouncing
        if direction == 'left'  and jump == True and bounce == False:
            
            #If gravity is negative i.e. in a jump blit the jumping left image
            if vertical_momentum <= 0:
                display.blit(jumpL,(player_rect.x,player_rect.y-scroll))
            
            #Otherwise you're falling so blit the falling image
            else:
                display.blit(fallL,(player_rect.x,player_rect.y-scroll))

        #Same as above just opposite direction
        if direction == 'right' and jump == True and bounce == False:
            if vertical_momentum <= 0:
                display.blit(jumpR,(player_rect.x,player_rect.y-scroll))
            else:
                display.blit(fallR,(player_rect.x,player_rect.y-scroll))

    def move(self,rect,tiles,win_tiles):
        #Globalling these variable so they can change easily
        global moving_left, moving_right, vertical_momentum, bounce, air_timer, direction

        collision_types = {'top':False,'bottom':False,'right':False,'left':False} #Making collision types dictionary

        rect.x += movement[0] #Movement of rectangle in the x direction

        hit_list = collision_test(rect,tiles,win_tiles) #Get the hit list

        for tile in hit_list: #For every tile/rectangle in the hit list
            if movement[0] > 0: #If the movement in the x is greater than 0 i.e. Right
                rect.right = tile.left #The right of the rectangle is equal to the left of the tile
                collision_types['right'] = True #Collision type is right
                
                #If you're in the air and not bouncing, but a collision is happening
                if air_timer > 6 and bounce == False:
                    bounce = True #Make bounce true
                    direction = 'left' #Change the direction to left
                    moving_right = False #Change the direction you're going to false
                    moving_left = True #Make the character move in the opposite direction
                    vertical_momentum = -3 #Make the character go upwards a little bit

                    #All of this together makes a reverse jump i.e. bounce
                    #The boolean bounce is used for animation and so that if you have already bounced once you cannot bounce again

            elif movement[0] < 0: #If the movement if the x is less than 0 i.e. Left
                rect.left = tile.right #The left of the rectangle is equal to the right of the tile
                collision_types['left'] = True #Collision type is left
                
                #All the same things from above except the direction is flipped
                if air_timer > 6 and bounce == False:
                    bounce = True
                    direction = 'right'
                    moving_left = False
                    moving_right = True
                    vertical_momentum = -3

        #Same as x direction just in the y direction
        #There is no bouncing by hitting the top or bottom of an object
        rect.y += movement[1]
        hit_list = collision_test(rect,tiles,win_tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        
        #Returning your characters rectange and the collision type
        return rect, collision_types

class maps():
    def __init__(self, tilesize, surface):
        #Getting the tile size for the map, and surface dimensions we blit the map onto
        self.tilesize = tilesize
        self.surface = surface

    def load_map(self, path): #Getting tile map
        #Empty map array
        map = []
        #Reading the csv file and appending it to the map
        with open(path+'.csv') as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map #Returning map

#Seeing if there is a collision
def collision_test(rect,tiles,win_tiles):
    #Globalling win
    global win

    hit_list = [] #List of hits
    for tile in tiles: #For every tile in the list of tiles
        if rect.colliderect(tile): #If there is a collision append it to the hit list
            hit_list.append(tile)

    for tile in win_tiles: #For every tile in the list of tiles
        if rect.colliderect(tile): #If there is a collision append it to the hit list
            win = True

    #Return the hit list
    return hit_list

def rectangleResizer(rect,varName):
    rect.width = varName.get_width()

#Using map class to define tile size and the display dimenstions
map = maps(16,[592,392])

#Creating display surface
display = pygame.Surface((map.surface))

#Initiating player starting position and image where we get our initial player dimensions from
myPlayer = player(286,1267,'Animation/Running/L1.png')

#Using colourkey function from ImageLoad file to make all the images transparent
colourkey([start_img,finish_img,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,jumpL,fallL,jumpR,fallR,RHit,LHit,L1,L2,L3,L4,R1,R2,R3,R4])

#Creating player's rectange
player_rect = pygame.Rect(myPlayer.x,myPlayer.y,myPlayer.image.get_width(),myPlayer.image.get_height()) #Player's rectangle for collision & where we blit our image

while True: #Game loop

    event_list = pygame.event.get() #Making event list

    #This is useful because we have multiple uses of event lists happening in other files
    #This makes sure they all use the same queue

    if start == True: #Creating start screen if start is true

        #Resetting all values
        player_rect.x, player_rect.y = [286,1267]
        scroll = 1017
        moving_left = False
        moving_right = False
        win = False
        gametimer = 0

        #Using the start screen function from other file which returns the map we use and if we start or not
        start, map_name = startScreen(event_list,screen,start,background_start)

    elif win == True: #If win is true

        data = []

        file = open('Score1.txt','r')

        for i in range (1,4):
            if map_name == 'Maps/Map' + str(i):
                file = open('Score'+ str(i) + '.txt','r')

        line = file.readline()
        while line != '':
            data.append(line)
            line = file.readline()

        file.close
        record = float(data[0])

        if gametimer < record:
            record = gametimer 
            for i in range (1,4):
                if map_name == 'Maps/Map' + str(i):
                    with open('Score' + str(i) + '.txt', 'w') as file:
                        file.write(str(record))

                    file.close
        
        #Using win screen function from other file which shows your time and returns if we restart the game
        start = winScreen(event_list,screen,start,round(gametimer,2),round(record,2),background_start)

    else:
        
        game_map = maps.load_map('',map_name) #Getting tile map

        gametimer += 1/33 #Making a timer for the game

        timer_message = game_font.render(str(round(gametimer,2)), True, (255,20,147)) #Setting the timer message for main game

        if scroll >= 96: #Scrolling if the character is less than a certain threshold
            scroll += (player_rect.y-scroll-250)/20 #Updating scroll depending on how high the character is
        
        if scroll < 96: #If your character is higher than 96 on the screen the scrolling will stay at that point
            scroll = 96

        display.blit(background,(0,map.tilesize-scroll)) #Clear screen by filling it with blue

        win_rects = []
        tile_rects = [] #Tile rectangles
        ysize = 0
        xsize = 0
        y = 0 #Y starts at 0

        for line in game_map: #For every line in the tile map
            x = -1 #Offset by 1 x value this makes borders for the game easy 
            ysize = y*map.tilesize - scroll
            for tile in line: #For every tile in 
                xsize = x*map.tilesize
                if tile == '1':
                    display.blit(one,(xsize,ysize))
                if tile == '2':
                    display.blit(two,(xsize,ysize))
                if tile == '3':
                    display.blit(three,(xsize,ysize))
                if tile == '4':
                    display.blit(four,(xsize,ysize))
                if tile == '5':
                    display.blit(five,(xsize,ysize))
                if tile == '6':
                    display.blit(six,(xsize,ysize))
                if tile == '7':
                    display.blit(seven,(xsize,ysize))
                if tile == '8':
                    display.blit(eight,(xsize,ysize))
                if tile == '9':
                    display.blit(nine,(xsize,ysize))
                if tile == '10':
                    display.blit(ten,(xsize,ysize))
                if tile == '11':
                    display.blit(eleven,(xsize,ysize))
                if tile == '12':
                    display.blit(twelve,(xsize,ysize))
                if tile == '13':
                    display.blit(thirteen,(xsize,ysize))
                if tile == '14':
                    display.blit(fourteen,(xsize,ysize))
                if tile == '15':
                    display.blit(fifteen,(xsize,ysize))
                if tile == '16':
                    display.blit(sixteen,(xsize,ysize))
                if tile == '-1':
                    display.blit(start_img,(xsize,ysize))
                if tile == '-2':
                    display.blit(finish_img,(xsize,ysize))
                    win_rects.append(pygame.Rect(xsize,y*map.tilesize,map.tilesize,map.tilesize))

                if tile not in ['0','-1','-2']: #If the tile value is not in this list then it can be collided with
                    tile_rects.append(pygame.Rect(xsize,y*map.tilesize,map.tilesize,map.tilesize))
                
            #Resetting these in the appropriate indents
                x += 1
            y += 1

        movement = [0,0] #Movement in the x and y
        if moving_right == True: #If you're moving right you move by 2 pixels at a time
            movement[0] += 2
        if moving_left == True: #Same as above just left
            movement[0] -= 2

        movement[1] += vertical_momentum #Movement in the y is added on by an increasing value to mimic gravity
        vertical_momentum += 0.2 #Momentum increases by 0.2 at a time and after 3 frames the character moves an entire pixel

        if vertical_momentum > 5: #Resetting vertical momentum so you don't accelerate forever
            vertical_momentum = 5

        player_rect,collisions = myPlayer.move(player_rect,tile_rects,win_rects) #Making collisions happen by calling the move function

        if collisions['bottom'] == True: #If you collide on the bottom of your character
            air_timer = 0 #The time in the air is 0
            vertical_momentum = 0 #Vertical momentum is reset
            jump = False #Jump turns false
            
            if bounce == True: #If bounce was true when you collide on the bottom of your character
                
                #Stop moving
                moving_right = False
                moving_left = False

                bounce = False #Make bounce false

        #If you collide on the top of your character set vertical momentum to 0. This prevents the top of your character from sticking to ceilings.
        if collisions['top'] == True:
            vertical_momentum = 0

        #If you're not colliding on the bottom or top make the air timer go up
        else:
            air_timer += 1

        #Counter for animation
        counter += 0.0625

        #This section makes it so the animation isn't too fast

        #If the counter becomes a whole integer
        if counter % 1 == 0:
            frame = int(counter)
            if frame > 3: #Resetting frame if it becomes out of range
                frame = 0
                counter = 0
                
        myPlayer.animation() #Calling animation

        for event in event_list: #Event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN: #Keydown events
    
                if event.key == K_RIGHT or event.key == K_d: #If right arrow/D is pressed
                    direction = 'right' #Character is facing right
                    moving_right = True #Moving right is true
                    moving_left = False #Moving left is false

                #Same just opposite direction
                if event.key == K_LEFT or event.key == K_a: #If left arrow/A is pressed
                    direction = 'left'
                    moving_left = True
                    moving_right = False

                if event.key == K_SPACE or event.key == K_UP or event.key == K_w: #If SPACE/Up arrow/W is pressed
                    jump = True #Jump is true
                    if air_timer <= 6: #If the air timer is less than or equal to 6 you can jump
                        vertical_momentum = -4 #Move up 4 pixels per frame

                        #Air timer allows for you to jump a little bit after falling off a platform. This is a quality of life fix.

                if event.key == K_m: #If M is pressed
                    start = True #Start screen
                    
                if event.key == K_r: #If R is pressed
                    #Resetting all values
                    player_rect.x, player_rect.y = [286,1267]
                    scroll = 1017
                    moving_left = False
                    moving_right = False
                    win = False
                    gametimer = 0

                if event.key == K_q: #If Q is pressed quit
                    pygame.quit()
                    sys.exit()

            if event.type == KEYUP: #If the key is released
                #Sets variables to false
                if event.key == K_RIGHT or event.key == K_d:
                    moving_right = False
                if event.key == K_LEFT or event.key == K_a:
                    moving_left = False

        display.blit(timer_message,(0,0)) #Displaying timer
        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0)) #Scaling surface to screen

    pygame.display.update() #Updating display
    clock.tick(60) #60 fps