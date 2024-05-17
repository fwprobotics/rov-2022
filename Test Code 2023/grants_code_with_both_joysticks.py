#joysticks are switched around, left joystick goes up, down, forwards, backwards; right joystick pitches and rolls
import json
import pygame
import serial
import serial.tools.list_ports

import serial

def myround(x, base=10):
    return base * round(x/base)



STOP_INT = 1500
STOP = '1500'
button_0 = STOP


pygame.joystick.init()
print(pygame.joystick.get_count())
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)
pygame.init()

right_x_position = 0
right_y_position = 0
left_x_position = 0
left_y_position = 0
right_trigger_position = 0
left_trigger_position = 0

speed_fb_min = 1300 #forward & backward minimum
speed_fb_max = 1700 #forward & backward maximum
speed_fb_d_max = 1600 #forward & backward & down maximum
speed_fb_u_min = 1400 #forward & backward & up minimum
speed_ud_max = 1700 #up & down maximum
speed_ud_min = 1300 #up & down minimum


speed_up_1 =0
speed_down_1 = 0

def translate(value, leftMin, leftMax, rightMin, rightMax):

    leftSpan = leftMax-leftMin
    valueScaled = float(value-leftMin)/leftSpan
    rightSpan = rightMax - rightMin
    return rightMin + (valueScaled * rightSpan)

def writeToSerial(msg):
    print("writing", msg.encode())
    ser.write(msg.encode())
    #fakeSerial.writeToSerial(msg)

correctdevice = str()
for port in serial.tools.list_ports.comports():
    if "com" in port.device.lower():
        correctdevice = port.device
print("Using serial port: ", correctdevice)
ser = serial.Serial(correctdevice, 19200, timeout=0.005)

servoOpen = 180
servoClosed = 0
counter = 0

#log_file = open("events.txt", 'w')
while True:

    for event in pygame.event.get():
        event_dict = event.dict
        print(event_dict)

#which button is being pressed?
        if event_dict.get("axis") == 2: #right joystick x-axis
            right_x_position = event.dict.get("value")

        if event_dict.get("axis") == 3: #right joystick y-axis
            right_y_position = event.dict.get("value")

        if event_dict.get("axis") == 1: #left joystick y-axis
            left_y_position = event.dict.get("value") # DOUBLE CHECK

        if event_dict.get("axis") == 0: #left joystick x-axis
            left_x_position = event.dict.get("value") # DOUBLE CHECK

        if event_dict.get("axis") == 4: #left trigger position; double check
            left_trigger_position = event.dict.get("value")

        if event_dict.get("axis") ==5: #right trigger position; double check
            right_trigger_position = event.dict.get("value")

# map controller buttons to commanded directions
        forward_speed = right_x_position
        up_speed = -right_y_position
        pitch_speed = -left_y_position * 0.6
        right_speed = left_x_position * 0.6 #scale down turning commands
        servo_1 = left_trigger_position
        servo_2 = right_trigger_position

# map command directions to thruster commands
        a_command = 0 #up (front)
        b_command = 0 #down (back)
        c_command = 0 #forward (right)
        d_command = 0 #backward (left)

        c_command += forward_speed
        d_command += -forward_speed

        a_command += up_speed
        b_command += -up_speed

        a_command += pitch_speed
        b_command += pitch_speed

        c_command += right_speed
        d_command += right_speed

# map the thruster commands to their pwm value
        a_pwm = translate(a_command, -1, 1, 1200, 1800)
        b_pwm = translate(b_command, -1, 1, 1200, 1800)
        c_pwm = translate(c_command, -1, 1, 1200, 1800)
        d_pwm = translate(d_command, -1, 1, 1200, 1800)
        servo_1_pwm = translate(servo_1, -1, 1, 0, 180)
        servo_2_pwm = translate(servo_2, -1, 1, 0, 180)

# send pwm to arduino
        writeToSerial(str(int(a_pwm)) + "a")
        writeToSerial(str(int(b_pwm)) + "b")
        writeToSerial(str(int(c_pwm)) + "c")
        writeToSerial(str(int(d_pwm)) + "d")
        writeToSerial(str(int(servo_1_pwm)) + "y")
        writeToSerial(str(int(servo_2_pwm)) + "z")



        if event_dict.get("joy") == 0:
            if event_dict.get("button") == 0:
                a_recent_speed = 1500
                b_recent_speed = 1500
                c_recent_speed = 1500
                d_recent_speed = 1500
                writeToSerial(str(int(a_recent_speed)) + "a")
                writeToSerial(str(int(b_recent_speed)) + "b")
                writeToSerial(str(int(c_recent_speed)) + "c")
                writeToSerial(str(int(d_recent_speed)) + "d")

log_file.close()

pygame.time.wait(15)
out = ser.readline()
if out:
    print(out.decode(), end = '')

# Write your code here :-)# Write your code here :-)
