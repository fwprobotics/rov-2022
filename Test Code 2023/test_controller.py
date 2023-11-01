import pygame

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(dir(joysticks[0]))
print(joysticks[0].get_numbuttons())
while True:
    print(joysticks[0].get_button(0))
    print(joysticks[0].get_button(1))
    print(joysticks[0].get_button(2))
    print(joysticks[0].get_button(3))
    print(joysticks[0].get_button(4))
    print(joysticks[0].get_button(5))
    print(joysticks[0].get_button(6))
    print(joysticks[0].get_button(7))
    print(joysticks[0].get_button(8))
    print(joysticks[0].get_button(9))
    print(joysticks[0].get_button(10))
    print(joysticks[0].get_button(11))
