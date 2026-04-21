import pygame 
import time
import math
pygame.init()

screen = pygame.display.set_mode((1400, 1050))
clock = pygame.time.Clock()

pygame.display.set_caption("MICKEY MOUSE CLOCK") 

left = pygame.transform.scale(pygame.image.load("clock/leftarm.png"), (1400,1050))
right = pygame.transform.scale(pygame.image.load("clock/rightarm.png"), (1400,1050))
main = pygame.transform.scale(pygame.image.load("clock/mickeyclock.jpeg"), (1400, 1050))

done = False

while not done: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    current_time = time.localtime()                                                                          
    minute = current_time.tm_min
    second = current_time.tm_sec
    
    minute_angle = minute * 60    + (second / 60) * 6                                                         
    second_angle = second * 6 
    
    screen.blit(main, (0,0))                                                                                 
    rotated_rightarm = pygame.transform.rotate(pygame.transform.scale(right, (1400, 1050)), -minute_angle)    
    rightarmrect = rotated_rightarm.get_rect(center=(1400 // 2 , 1050 // 2 ))
    screen.blit(rotated_rightarm, rightarmrect)

    rotated_leftarm = pygame.transform.rotate(pygame.transform.scale(left, (40.95, 682.5)), -second_angle)  
    leftarmrect = rotated_leftarm.get_rect(center=(1400 // 2 , 1050 // 2 ))
    screen.blit(rotated_leftarm, leftarmrect)
    
    pygame.display.flip() 
    clock.tick(60) 
    
pygame.quit()