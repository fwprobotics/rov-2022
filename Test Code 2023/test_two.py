import json
import pygame
import serial
import serial.tools.list_ports

stop='1500'

pygame.joystick.init()
print(pygame.joystick.get_count())
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)
pygame.init()

def writeToSerial(msg):
    print("writing", msg.encode())
    ser.write(msg.encode())

correctdevice = str()
for port in serial.tools.list_ports.comports():
    if "com" in port.device.lower():
        correctdevice = port.device
print("Using serial port: ", correctdevice)
ser = serial.Serial(correctdevice, 19200, timeout=0.005)

servoOpen = 180
servoClosed = 0

def translate(value, leftMin, leftMax, rightMin, rightMax):

    leftSpan = leftMax-leftMin
    valueScaled = float(value-leftMin)/leftSpan
    rightSpan = rightMax - rightMin
    return rightMin + (valueScaled * rightSpan)

while True:

    for event in pygame.event.get():
        event_dict = event.dict

        if event_dict.get("axis") == 4:
            degrees=translate(event.dict.get("value"), -1,1,0,180)
            print(degrees)
            writeToSerial(str(int(degrees)) + "y")
        if event_dict.get("axis") ==5:
            degrees = translate(event.dict.get("value"), -1,1,0,180)
            print(degrees)
            writeToSerial(str(int(degrees)) + "z")

        if event_dict.get("axis") == 3: # thruster's going up to down

            speed_up = translate(event.dict.get("value"), -1,1,1400,1600) #up
            print (speed_up)
            writeToSerial(str(int(speed_up)) + " b")

            speed_down = translate(event.dict.get("value"),-1,1,1600,1400) #down
            print (speed_down)
            writeToSerial(str(int(speed_down)) + " a") 

            writeToSerial(str(int(stop)) + " c") #foward

            writeToSerial(str(int(stop)) + " d") #backward
        
        if event_dict.get("axis") == 2: # thruster's going forward to backward
            
            speed_forward = translate(event.dict.get("value"),-1,1,1600,1400) #forward
            print (speed_forward)
            writeToSerial(str(int(speed_forward)) + " c")
            
            speed_backward = translate(event.dict.get("value"), -1,1,1400,1500) #backward
            print (speed_backward)
            writeToSerial(str(int(speed_backward)) + " d")
            
            speed_up_2 = translate(event.dict.get("value"),-1,0,1450,1500) 
            print (speed_up_2)
            writeToSerial(str(int(speed_up_2)) + " a")
            
            
            speed_up_3 = translate(event.dict.get("value"),0,1,1500,1450)
            print (speed_up_3)
            writeToSerial(str(int(speed_up_3)) + " a")
            
            speed_down_2 = translate(event.dict.get("value"),-1,0,1550,1500)
            print (speed_down_2)
            writeToSerial(str(int(speed_down_2)) + " b")
            
            speed_down_3 = translate(event.dict.get("value"),0,-1,1500,1550)
            print (speed_down_3)
            writeToSerial(str(int(speed_down_3)) + " b")
        

pygame.time.wait(15)
out = ser.readline()
if out:
    print(out.decode(), end = '')
