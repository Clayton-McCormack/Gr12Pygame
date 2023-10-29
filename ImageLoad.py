import pygame, sys

#Making the colourkey functions
def colourkey(images):
    for i in images: #For every image colourkey it
        i.set_colorkey((255,0,0))

#set_colorkey works like a green screen it sets whatever color you want to be transparent
#Therefore since I made all the backgrounds to my pictures red I am cutting out red

#Loading all these images - Yes it's tedious and long
one = pygame.image.load('Blocks/left_corner.png')
two = pygame.image.load('Blocks/middle_grass.png')
three = pygame.image.load('Blocks/right_corner.png')
four = pygame.image.load('Blocks/top_side.png')
five = pygame.image.load('Blocks/left_middle.png')
six = pygame.image.load('Blocks/middle.png')
seven = pygame.image.load('Blocks/right_middle.png')
eight = pygame.image.load('Blocks/middle_side.png')
nine = pygame.image.load('Blocks/bottom_left.png')
ten = pygame.image.load('Blocks/bottom_middle.png')
eleven = pygame.image.load('Blocks/bottom_right.png')
twelve = pygame.image.load('Blocks/bottom_side.png')
thirteen = pygame.image.load('Blocks/floating_left.png')
fourteen = pygame.image.load('Blocks/floating_middle.png')
fifteen = pygame.image.load('Blocks/floating_right.png')
sixteen = pygame.image.load('Blocks/floating_block.png')
start_img = pygame.image.load('Blocks/Start.png')
background = pygame.image.load('Clouds.png')
finish_img = pygame.image.load('Blocks/Finish.png')
L1 = pygame.image.load('Animation/Running/L1.png')
L2 = pygame.image.load('Animation/Running/L2.png')
L3 = pygame.image.load('Animation/Running/L3.png')
L4 = pygame.image.load('Animation/Running/L4.png')
R1 = pygame.image.load('Animation/Running/R1.png')
R2 = pygame.image.load('Animation/Running/R2.png')
R3 = pygame.image.load('Animation/Running/R3.png')
R4 = pygame.image.load('Animation/Running/R4.png')
jumpL = pygame.image.load('Animation/Jumping/LUp.png')
fallL = pygame.image.load('Animation/Jumping/LFall.png')
jumpR = pygame.image.load('Animation/Jumping/RUp.png')
fallR = pygame.image.load('Animation/Jumping/RFall.png')
LHit = pygame.image.load('Animation/Jumping/LHit.png')
RHit = pygame.image.load('Animation/Jumping/RHit.png')
background_start = pygame.image.load('JumpKingBackground.jpg')

#Loading running and jumping into lists
walkLeft = [L1, L2, L3, L4]
walkRight = [R1, R2, R3, R4]