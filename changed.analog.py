# operation make the controller work
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

axis_right_trigger = 5
axis_left_trigger = 4
axis_joystick_left_left_right = 0
axis_joystick_left_up_down = 1
axis_joystick_right_left_right = 2
axis_joystick_right_up_down = 3
yaw_axis = axis_joystick_left_left_right
foward_axis_backwards = axis_joystick_right_up_down
up_down_axis = [axis_joystick_right_up_down,axis_joystick_left_up_down}

claw_one = "x"
claw_two = "y"
thruster_one = "a"
thruster_two = "b"
thruster_three = "c"
thruster_four = "d"

claw_position_mapping = {
    claw_one: (servo_b_close, servo_b_open),
    claw_two: (servo_a_close, servo_a_open)
}

axis_to_claw{
    axis_left_trigger: claw_two,
    axis_right_trigger: claw_one,
}



# initialize serial monitor
correctdevice = str()
for port in serial.tools.list_ports.comports():
    # print(port.__dict__)
    if "arduino" in port.manufacturer.lower():
    #if "usb" in port.device.lower():
        correctdevice = port.device
print("Using serial port: ", correctdevice)
#ser = serial.Serial(correctdevice, 19200, timeout=0.005)

def writeToSerial(msg):
    print("writing", msg.encode())
    #ser.write(msg.encode())

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    value = round(value, 4)
    if not (leftMin <= value <= leftMax):
        print(value)
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
        axis = event_dict.get('axis')
        val = event.dict.get('value')
        if val is not None:
            if axis in {0, 1, 2, 3, 4}:
                if val is not None and not -0.1 <= val <= 0.1:
                    print(f"axis {axis} :{val}")
                    print(str(axis) * int(translate(val, -1, 1, 1, 41)))
            else:
                print(f"axis: {axis}, {val}")

        if axis == claw_one or axis == claw_two:
            claw_code = axis_to_claw[axis] # change to 'x' or 'y'
            degrees = translate (event.dict.get("value"), -1, 1, *claw_position_mapping[claw_code])  
            print(degrees)
            writeToSerial(f"{degrees}{claw_code}" }
    
        if axis in {axis_joystick_left_left_right,axis_joystick_left_up_down,axis_joystick_right_left_right,axis_joystick_right_up_down}:
            
        if event_dict.get("axis") == 0:
            degrees = translate (event.dict.get("value"), -1, 1,1400, 1600)
            degrees = round(degrees/10)*10
            print(degrees)
            if degrees > 1490 and degrees < 1510:
                writeToSerial(str(int(1500)) + "a")
                writeToSerial(str(int(1500)) + "d")
            else:
                writeToSerial(str(int(degrees)) + "a")
                writeToSerial(str(int(degrees)) + "d")
        if event_dict.get("axis") == 1:
            c_degrees = translate (event.dict.get("value"), -1, 1,1400, 1600)
            c_degrees = round(c_degrees/10)*10
            if c_degrees > 1490 and c_degrees < 1510:
                writeToSerial(str(int(1500)) + "c")
            else:
                writeToSerial(str(int(c_degrees)) + "c")
            b_degrees = translate (event.dict.get("value"), -1, 1,1600, 1400)
            b_degrees = round(b_degrees/10)*10
            if b_degrees > 1490 and b_degrees < 1510:
                writeToSerial(str(int(1500)) + "b")
            else:
                writeToSerial(str(int(b_degrees)) + "b")
        if event_dict.get("axis")== 2 :
            a_degrees = translate (event.dict.get("value"), -1, 1,1600, 1400)
            a_degrees = round(a_degrees/10)*10
            if a_degrees > 1490 and a_degrees < 1510:
                writeToSerial(str(int(1500)) + "a")
            else:
                writeToSerial(str(int(a_degrees)) + "a")
            d_degrees = translate (event.dict.get("value"), -1, 1,1400, 1600)
            d_degrees = round(d_degrees/10)*10
            if d_degrees > 1490 and d_degrees < 1510:
                writeToSerial(str(int(1500)) + "d")
            else:
                writeToSerial(str(int(d_degrees)) + "d")
        if event_dict.get("axis")== 3 :
            b_degrees = translate (event.dict.get("value"), -1, 1,1600, 1400)
            b_degrees = round(b_degrees/10)*10
            if b_degrees > 1490 and b_degrees < 1510:
                writeToSerial(str(int(1500)) + "b")
            else:
                writeToSerial(str(int(b_degrees)) + "b")
            c_degrees = translate (event.dict.get("value"), -1, 1,1400, 1600)
            c_degrees = round(c_degrees/10)*10
            if c_degrees > 1490 and c_degrees < 1510:
                writeToSerial(str(int(1500)) + "c")
            else:
                writeToSerial(str(int(c_degrees)) + "c")
        # """
        

        pygame.time.wait(20)

    out = b'' # ser.readline()
    if out:
        print(out.decode(), end = '')
