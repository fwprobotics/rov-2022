import pygame
import time
import json
import pygame
import serial
import serial.tools.list_ports
servo_b_open = 60
servo_b_close = 180
servo_a_open = 60
servo_a_close = 180

# initialize serial monitor
correctdevice = str()
for port in serial.tools.list_ports.comports():
    # print(port.__dict__)
    if "arduino" in port.manufacturer.lower():
    #if "usb" in port.device.lower():
        correctdevice = port.device
print("Using serial port: ", correctdevice)
ser = serial.Serial(correctdevice, 9600, timeout=0.005)

def writeToSerial(msg):
    print("writing", msg.encode())
    ser.write(msg.encode())

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# controller testing
num = 0
pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
print(joystick_count)
controller = pygame.joystick.Joystick(0)
controller.init()
while True:
    for event in pygame.event.get():
        event_dict = event.dict
        print(event.dict)
        if event_dict.get("axis") == 4:
            degrees = translate (event.dict.get("value"), -1, 1, servo_b_close, servo_b_open)
            print(degrees)
            writeToSerial(str(int(degrees)) + "b")
        if event_dict.get("axis") == 5:
            degrees = translate (event.dict.get("value"), -1, 1,servo_a_close, servo_a_open)
            print(degrees)
            writeToSerial(str(int(degrees)) + "a")
        pygame.time.wait(15)
    out = ser.readline()
    if out:
        print(out.decode(), end = '')
