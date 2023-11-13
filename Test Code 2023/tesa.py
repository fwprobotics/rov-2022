import json
import pygame
import serial
import serial.tools.list_ports

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

    valueScaled = float(value-leftMin)/2
    return rightMin + (valueScaled *180)

    """

    leftSpan = leftMax - leftMin #figuring out that the distance difference between the axis values is 2
    rightSpan = rightMax - rightMin # figuring out that the distance between the servo values is 180
    valueScaled = float(value - leftMin) / float(leftSpan) #setting up a ratio of value (1) and putting that ove the left span so (2/2 =1)

    return rightMin + (valueScaled * rightSpan)# multiplying this ratio above by right span value (180*1 = 180)
    """

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
pygame.time.wait(15)
out = ser.readline()
if out:
    print(out.decode(), end = '')
