"""
"""

import pygame
import serial

FORWARD = '1620'
BACKWARD = '1380'
STOP = '1500'

pygame.init()
pygame.joystick.init()

print(pygame.joystick.get_count())
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)

# initialize serial monitor
correctdevice = str()    
for port in serial.tools.list_ports.comports():
    print(port.__dict__)
    #if "arduino" in port.manufacturer.lower():
    if "usb" in port.device.lower():
        correctdevice = port.device
print(correctdevice)
ser=serial.Serial(correctdevice , 19200, timeout=1)

def writeToSerial(msg):
    print("writing", msg.encode())
    ser.write(msg.encode())

# -------- Main Program Loop -----------
while True:
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
    
        if event.type == pygame.JOYBUTTONDOWN:  # right joystick is moved out of resting position or select button is pressed
            #print("pygame.JOYBUTTONDOWN event")
            #print(event)
            #print("button:", event.button) 
            if event.button == 9 : #start button pressed
                if event.joy == 0 : 
                    print("this is controller one (thrusters/claws)") 
                if event.joy == 1 : 
                    print("this is controller two (cameras/claws) ") 
        
            if event.joy == 0 : #controller one
                if event.button == 8: # select was pressed
                    writeToSerial(STOP + 'a')
                    writeToSerial(STOP + 'b')
                    writeToSerial(STOP + 'c')
                    writeToSerial(STOP + 'd')


                if event.button == 0: # right joystick up
                    writeToSerial(FORWARD + 'b')
                    writeToSerial(FORWARD + 'c')
                if event.button == 1: # right joystick right
                    writeToSerial(BACKWARD + 'd')
                    writeToSerial(FORWARD + 'a')
                if event.button == 2: # right joystick down
                    writeToSerial(BACKWARD + 'b')
                    writeToSerial(BACKWARD + 'c')
                if event.button == 3: # right joystick left
                    writeToSerial(BACKWARD + 'a')
                    writeToSerial(FORWARD + 'd')
            if event.joy == 1: #controller 2
                if event.button == 0: # 1 button is presed on controller 1, 
                    writeToSerial("10x") 
                if event.button == 1: # 2 button is pressed on controller 1
                    writeToSerial( "10w") 
                if event.button == 2: # 3 button is pressed on controller 1
                    writeToSerial("-10x") 
                if event.button == 3: # 4 button is pressed on controller 1
                    writeToSerial("-10w") 
        if event.type == pygame.JOYBUTTONUP:# right joystick has moved back to resting position
            #print("pygame.JOYBUTTONDOWN event")
            #print(event)
            #print("button:", event.button)
            if event.joy == 0: #controller 1
                if event.button == 8:
                    writeToSerial(STOP + 'a')
                    writeToSerial(STOP + 'b')
                    writeToSerial(STOP + 'c')
                    writeToSerial(STOP + 'd')
                if event.button == 0: # right joystick up
                    writeToSerial(STOP + 'b')
                    writeToSerial(STOP + 'c')
                if event.button == 1: # right joystick right
                    writeToSerial(STOP + 'd')
                    writeToSerial(STOP + 'a')
                if event.button == 2: # right joystick down
                    writeToSerial(STOP + 'b')
                    writeToSerial(STOP + 'c')
                if event.button == 3: # right joystick left
                    writeToSerial(STOP + 'a')
                    writeToSerial(STOP + 'd')
            if event.joy == 1: #controller 2
                if event.button == 4: # left trigger button 1
                    writeToSerial("180z")
                if event.button == 6: #left trigger button 2
                    writeToSerial("0z")
                if event.button == 5: # right trugger button 1
                    writeToSerial("180y")
                if event.button ==7: # right trigger button 2
                    writeToSerial("0y")
         
        elif event.type == pygame.JOYAXISMOTION:
            #print("pygame.JOYAXISMOTION event")
            #print(event)
            if event.joy == 0: 
                axis = event.axis
                value = round(event.value, 2)
                #print(axis, value)
                if axis == 1 and value == 1: #moves back, left joystick down
                    writeToSerial(BACKWARD + 'a')
                    writeToSerial(BACKWARD + 'd')
                if axis == 1 and value == -1: #moves forward, left joystick up
                    writeToSerial(FORWARD + 'a')
                    writeToSerial(FORWARD + 'd')
                if axis == 0 and value == 1: #moves left, left joystick left
                    writeToSerial(FORWARD + 'b')
                    writeToSerial(BACKWARD + 'c')
                if axis == 0 and value == -1:#moves right, left joystick right
                    writeToSerial(BACKWARD + 'b')
                    writeToSerial(FORWARD + 'c')
                if value == 0 : #stops, left joystick neutral
                    writeToSerial(STOP + 'a')
                    writeToSerial(STOP + 'b')
                    writeToSerial(STOP + 'c')
                    writeToSerial(STOP + 'd')
        pygame.time.wait(15)# Write your code here :-)
