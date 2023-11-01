"""
"""

import json
import pygame
import serial
import serial.tools.list_ports

STOP = '1500'

pygame.init()
pygame.joystick.init()

print(pygame.joystick.get_count())
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)

# initialize serial monitor
correctdevice = str()
for port in serial.tools.list_ports.comports():
    # print(port.__dict__)
    if "arduino" in port.manufacturer.lower():
    #if "usb" in port.device.lower():
        correctdevice = port.device
print("Using serial port: ", correctdevice)
ser = serial.Serial(correctdevice, 19200, timeout=0.005)

def writeToSerial(msg):
    print("writing", msg.encode())
    ser.write(msg.encode())


# Opening JSON file
f = open('thruster_config.json')

# returns JSON object as
# a dictionary
data = json.load(f)

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
                    print("this is controller one (thrusters)")
                if event.joy == 1 :
                    print("this is controller two (claws) ")

            if event.joy == 0 : #controller one
                if event.button == 8: # select was pressed
                    writeToSerial(STOP + 'a')
                    writeToSerial(STOP + 'b')
                    writeToSerial(STOP + 'c')
                    writeToSerial(STOP + 'd')

                right_joystick_dict = data.get('rightjoystick', {})
                if event.button == 0: # right joystick up
                    for k, v in right_joystick_dict.get('up', {}).items():
                        writeToSerial(str(v) + k)
                if event.button == 1: # right joystick right
                    for k, v in right_joystick_dict.get('right', {}).items():
                        writeToSerial(str(v) + k)
                if event.button == 2: # right joystick down
                    for k, v in right_joystick_dict.get('down', {}).items():
                        writeToSerial(str(v) + k)
                if event.button == 3: # right joystick left
                    for k, v in right_joystick_dict.get('left', {}).items():
                        writeToSerial(str(v) + k)
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
            right_joystick_dict = data.get('rightjoystick', {})
            if event.joy == 0: #controller 1
                if event.button == 8:
                    writeToSerial(STOP + 'a')
                    writeToSerial(STOP + 'b')
                    writeToSerial(STOP + 'c')
                    writeToSerial(STOP + 'd')
                if event.button == 0: # right joystick up
                    for k, v in right_joystick_dict.get('up', {}).items():
                        writeToSerial(STOP + k)
                if event.button == 1: # right joystick right
                    for k, v in right_joystick_dict.get('right', {}).items():
                        writeToSerial(STOP + k)
                if event.button == 2: # right joystick down
                    for k, v in right_joystick_dict.get('down', {}).items():
                        writeToSerial(STOP + k)
                if event.button == 3: # right joystick left
                    for k, v in right_joystick_dict.get('left', {}).items():
                        writeToSerial(STOP + k)
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
                value = round(event.value,12)
                #print(axis, value)
                left_joystick_dict = data.get('leftjoystick', {})
                if axis == 1 and value == 1: #moves back, left joystick down
                    for k, v in left_joystick_dict.get('down', {}).items():
                        writeToSerial(str(v) + k)
                if axis == 1 and value == -1: #moves forward, left joystick up
                    for k, v in left_joystick_dict.get('up', {}).items():
                        writeToSerial(str(v) + k)
                if axis == 0 and value == 1: #moves left, left joystick left
                    for k, v in left_joystick_dict.get('left', {}).items():
                        writeToSerial(str(v) + k)
                if axis == 0 and value == -1:#moves right, left joystick right
                    for k, v in left_joystick_dict.get('right', {}).items():
                        writeToSerial(str(v) + k)
                if value == 0 : #stops, left joystick neutral
                    writeToSerial(STOP + 'a')
                    writeToSerial(STOP + 'b')
                    writeToSerial(STOP + 'c')
                    writeToSerial(STOP + 'd')
        pygame.time.wait(15)

    # See if the arduino has tried to print anything, and print it here if so.
    out = ser.readline()
    if out:
        print(out.decode(), end = '')
