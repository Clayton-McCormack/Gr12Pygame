import pygame, sys, random
from ImageLoad import *
from pygame.locals import *

pygame.init()

def startScreen(event_list,display,start,background): #My start screen with the parametres of the event list display and start
    map = '' #Map name is empty string

    #Initializing fonts
    game_font = pygame.font.SysFont('arial',13)

    #Initializing colours
    White = (255,255,255)
    Red = (255,0,0)
    Green = (0,255,0)

    #Initializing all the messages
    rulemessage = game_font.render('In order to progress you must regain your crown and declare your might as the JUMP KING! (There is a crown in the corner for you Mac)',True,White)
    rulemessage2 = game_font.render('You can bounce off of platforms and the borders of the screen, but only once. No bouncing twice in a row. So be careful.',True,White)
    rulemessage3 = game_font.render('When you fall from a bounce all movement stops.', True, White)
    rulemessage4 = game_font.render('You will be timed. Try to beat the record.',True,White)
    message5 = game_font.render('Click your choice of map or the exit button:',True,White)
    tipmessage = game_font.render('You can cancel a bounce midway to change directions. Similar to a double jump.',True,White)
     
    controls = game_font.render('Controls- Space/Up Arrow/W: Jump, Left Arrow/A: Left, and Right Arrow/D: Right, Go to Menu: M, Restart Map: R (if not beaten), Quit Game: Q',True,White)
    
    #Making buttons and their other colours
    map1_button = game_font.render('Easy',True,White)
    map1_button_collide = game_font.render('Easy',True,Green)
    
    map2_button = game_font.render('Medium',True,White)
    map2_button_collide = game_font.render('Medium',True,Green)

    map3_button = game_font.render('Hard',True,White)
    map3_button_collide = game_font.render('Hard',True,Green)

    exit_button = game_font.render('Quit',True,White)
    exit_button_collide = game_font.render('Quit',True,Red)

    mouse_x, mouse_y = pygame.mouse.get_pos() #Getting mouse positions
    display.blit(background,(0,0)) #Blitting background

    #Making and drawing the buttons
    map1_rect = pygame.Rect(50,540,100,50)
    map2_rect = pygame.Rect(275,540,100,50)
    map3_rect = pygame.Rect(515,540,100,50)
    quit_rect = pygame.Rect(750,540,100,50)

    #Blitting the messages
    display.blit(rulemessage,(25,200))
    display.blit(controls,(5,250))
    display.blit(rulemessage2,(80,300))
    display.blit(rulemessage3,(280,400))
    display.blit(rulemessage4,(310,450))
    display.blit(tipmessage,(180,350))
    display.blit(message5,(300,500))
    display.blit(map1_button,(80,550))
    display.blit(map2_button,(305,550))
    display.blit(map3_button,(545,550))
    display.blit(exit_button,(780,550))

    mouse_rect = pygame.Rect(mouse_x,mouse_y,1,1) #Making mouse rectange

    if mouse_rect.colliderect(map1_rect): #If your mouse collides with any of the  buttons it will become green/red and display the message on top of it
        display.blit(map1_button_collide,(80,550))

    if mouse_rect.colliderect(map2_rect): #Same as first
        display.blit(map2_button_collide,(305,550))

    if mouse_rect.colliderect(map3_rect): #Same as first
        display.blit(map3_button_collide,(545,550))

    if mouse_rect.colliderect(quit_rect): #Same as first
        display.blit(exit_button_collide,(780,550))

    #Button clicks to start game or quit out of game   
    for event in event_list:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: #Keydown events
                
                if event.key == K_q: #Pressing q quits
                    pygame.quit()
                    sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN: #Clicking events
            
            #If you click on any of the map buttons it will start the game and make the map that map
            if mouse_rect.colliderect(map1_rect):
                start = False
                map = 'Maps/Map1'
            
            if mouse_rect.colliderect(map2_rect):
                start = False
                map = 'Maps/Map2'

            if mouse_rect.colliderect(map3_rect):
                start = False
                map = 'Maps/Map3'

            #The quit button makes you quit
            if mouse_rect.colliderect(quit_rect):
                pygame.quit()
                sys.exit()

    return start, map

def winScreen(event_list,display,start,timer,highscore,background):

    #Mostly the same stuff from the start screen 
    game_font = pygame.font.SysFont('arial',13)

    #Initializing colours
    White = (255,255,255)
    Red = (255,0,0)
    Green = (0,255,0)

    #Making messages
    win_message = game_font.render('Congratulations! You got the crown. You are now officialy the JUMP KING!',True,White)
    timer_message = game_font.render('You won in '+str(timer)+' seconds.',True,White)
    record = game_font.render('Your record is ' + str(highscore) + ' seconds.',True,White)
    message = game_font.render('Return to the Menu or Quit:',True,White)

    #Gettting white and green versions of message
    menu_button = game_font.render('Return to Menu',True,White)
    menu_button_collide = game_font.render('Return to Menu',True,Green)

    #Gettting white and red versions of message
    exit_button = game_font.render('Quit',True,White)
    exit_button_collide = game_font.render('Quit',True,Red)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()#Mouse position
    display.blit(background,(0,0)) #Blittin image

    menu_rect = pygame.Rect(180,450,150,50) #Making return to menu rect
    quit_rect = pygame.Rect(550,450,100,50) #Making quit rect

    #Blitting message
    display.blit(win_message,(220,350))
    display.blit(timer_message,(360,250))
    display.blit(record,(350,300))
    display.blit(message,(350,400))
    display.blit(menu_button,(230,460))
    display.blit(exit_button,(580,460))

    mouse_rect = pygame.Rect(mouse_x,mouse_y,1,1) #Making rectange for where mouse is

    #If the mouse hovers over either rectange it will display the other colour
    if mouse_rect.colliderect(menu_rect):
        display.blit(menu_button_collide,(230,460))

    if mouse_rect.colliderect(quit_rect):
        display.blit(exit_button_collide,(580,460))

    #Button clicks to start game or quit out of game   
    for event in event_list:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN: #Keydown events
            if event.key == K_m: #Pressing r returns to menu
                start = True
            
            if event.key == K_q: #Pressing q quits
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN: #Clicking events
            if mouse_rect.colliderect(menu_rect): #Clicking on the return to menu button makes start true
                start = True

            if mouse_rect.colliderect(quit_rect): #Clicking quit exits window
                pygame.quit()
                sys.exit()

    return start #Returning start