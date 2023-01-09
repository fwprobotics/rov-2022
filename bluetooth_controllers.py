# controller testing
import pygame
import time
num = 0
pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
print(joystick_count)
controller = pygame.joystick.Joystick(0)
controller.init()
while num != 10:
    for event in pygame.event.get():
        print(event)
    num = num + 1
    time.sleep(3)
Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy
Se# Write your code here :-)
