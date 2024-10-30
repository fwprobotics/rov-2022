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

while True:

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 3:
                writeToSerial("180z")
            if event.button == 1:
                writeToSerial("0z")

            if event.button == 11:
                writeToSerial("180w")
            if event.button == 13:
                writeToSerial("0w")

pygame.time.wait(15)
out = ser.readline()
if out:
    print(out.decode(), end = '')
