"""
Example to outline the split of joystick inputs to a commanded speed and direction for thrusters
Takes advantage of analog values returned by a joystick.
"""
import pygame


pygame.init()
pygame.joystick.init()

print(pygame.joystick.get_count())
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)


while True:
    for event in pygame.event.get():
        # Get our input from the user. (In an ideal world, you could swap this block easily between controllers)
        inputDict = {"axis": '', "speed": 0}  # Make a fresh dictionary
        if event.type == pygame.JOYBUTTONDOWN:
            inputDict["axis"] = 'x'
            inputDict["speed"] = event.AXIS_VALUE  # Update with whatever gets the value
        if False:  # Fill in other buttons here
            pass

        # Map the directions to the thrusters
        if inputDict["axis"] == 'x':
            # NOTE: STOP must be changed to an integer
            # Calculate the new speed of the thruster and send it
            writeToSerial(str(int(STOP + 400 * inputDict["speed"])) + 'b')
            writeToSerial(str(int(STOP + 400 * inputDict["speed"])) + 'c')
        elif False:  # Fill in other directions & thrusters here
            writeToSerial(str(int(STOP + 400 * inputDict["speed"])) + 'b')
            writeToSerial(str(int(STOP + -400 * inputDict["speed"])) + 'c')
            pass

    pygame.time.wait(15)
