import json
import pygame
import serial
import serial.tools.list_ports
from sigfig import round




stop='1500'

pygame.joystick.init()
print(pygame.joystick.get_count())
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)
pygame.init()

a_recent_speed = 0
b_recent_speed = 0
c_recent_speed = 0
d_recent_speed = 0

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
counter = 0

def translate(value, leftMin, leftMax, rightMin, rightMax):

    leftSpan = leftMax-leftMin
    valueScaled = float(value-leftMin)/leftSpan
    rightSpan = rightMax - rightMin
    return rightMin + (valueScaled * rightSpan)

while True:


    for event in pygame.event.get():
        event_dict = event.dict
        if counter % 60 ==0:
            if event.dict.get("axis") ==3 or event.dict.get("axis") == 2 :
                print(event.dict)
        counter = counter +1

    
        if event_dict.get("axis") == 4:
            degrees=translate(event.dict.get("value"), -1,1,0,180)
            print(degrees)
            writeToSerial(str(int(degrees)) + "y")
        if event_dict.get("axis") ==5:
            degrees = translate(event.dict.get("value"), -1,1,0,180)
            print(degrees)
            writeToSerial(str(int(degrees)) + "z")

        if event_dict.get("axis") == 2: # thruster's going up to down

            speed_up = round(translate(event.dict.get("value"), -1,1,1400,1600),sigfigs =2) #up
            print (speed_up)
            if int(speed_up) != b_recent_speed:
                writeToSerial(str(int(speed_up)) + " b")
                b_recent_speed = speed_up


            speed_down = round(translate(event.dict.get("value"),-1,1,1600,1400),sigfigs =2) #down
            print (speed_down)
            if int(speed_down) != a_recent_speed:
                writeToSerial(str(int(speed_down)) + " a")
                a_recent_speed = speed_down

            stop_1 = 1500
           
            if int(stop_1) != c_recent_speed:
                writeToSerial(str(int(stop_1)) + " c") 
                c_recent_speed = stop_1
                
            if int(stop_1) != d_recent_speed:
                writeToSerial(str(int(stop)) + " d") 
                d_recent_speed = stop_1

        if event_dict.get("axis") == 3: # thruster's going forward to backward
            print(event.dict)

            speed_forward = translate(event.dict.get("value"),-1,1,1600,1400) #forward
            print (speed_forward)
            if int(speed_forward) != c_recent_speed:
                writeToSerial(str(int(speed_forward)) + " c")
                c_recent_speed = speed_forward

            speed_backward = translate(event.dict.get("value"), -1,1,1400,1500) #backward
            print (speed_backward)
            writeToSerial(str(int(speed_backward)) + " d")
            if int(speed_backward) != d_recent_speed:
                writeToSerial(str(int(speed_backward)) + " d")
                d_recent_speed = speed_backward

            if 0<event.value<=-1:

                speed_up_2 = translate(event.dict.get("value"),-1,0,1400,1500)
                print (speed_up_2)
                if int(speed_up_2) != a_recent_speed:
                    writeToSerial(str(int(speed_up_2)) + " a")
                    a_recent_speed = speed_up_2

                speed_down_2 = translate(event.dict.get("value"),-1,0,1600,1500)
                print (speed_down_2)
                if int(speed_down_2) != b_recent_speed:
                    writeToSerial(str(int(speed_down_2)) + " b")
                    b_recent_speed = speed_down_2
            else:
                speed_up_3 = translate(event.dict.get("value"),0,1,1500,1400)
                print (speed_up_3)
                if int(speed_up_3) != a_recent_speed:
                    writeToSerial(str(int(speed_up_3)) + " a")
                    a_recent_speed = speed_up_3

                speed_down_3 = translate(event.dict.get("value"),0,-1,1500,1600)
                print (speed_down_3)
                if int(speed_down_3) != b_recent_speed:
                    writeToSerial(str(int(speed_down_3)) + " b")
                    b_recent_speed = speed_down_3



pygame.time.wait(15)
out = ser.readline()
if out:
    print(out.decode(), end = '')
