import json
import pygame
import serial
import serial.tools.list_ports
def myround(x, base=10):
    return base * round(x/base)
import time


SEND_EVERY = 0.05
last_send_time = 0
STOP_INT = 1500
STOP = '1500'
button_0 = STOP


pygame.joystick.init()
print(pygame.joystick.get_count())
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)
pygame.init()

THRESHOLD = 0.8

x_last_speed = 0
y_last_speed = 0
x_position = 0
y_position = 0
s_last_speed = 0
p_last_speed = 0
s_position = 0
p_position = 0

a_recent_speed = 0
b_recent_speed = 0
c_recent_speed = 0
d_recent_speed = 0

speed_fb_min = 1300 #forward & backward minimum
speed_fb_max = 1700 #forward & backward maximum
speed_fb_d_max = 1600 #forward & backward & down maximum
speed_fb_u_min = 1400 #forward & backward & up minimum
speed_ud_max = 1600 #up & down maximum #changed value to 1600
speed_ud_min = 1400 #up & down minimum #changed value to 1400


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

def readIncomingMessages():
    try:
        return ser.read(500).decode()
    except serial.serialutil.SerialTimeoutException:
        return ''

correctdevice = str()
for port in serial.tools.list_ports.comports():
    if "com" in port.device.lower():
        correctdevice = port.device
print("Using serial port: ", correctdevice)
ser = serial.Serial(correctdevice, 19200, timeout=0.008)

servoOpen = 180
servoClosed = 0
counter = 0

#log_file = open("events.txt", 'w')
while True:

    for event in pygame.event.get():
        event_dict = event.dict
        # print(event_dict)

        if counter % 50 ==0:
            if event.dict.get("axis") ==3 or event.dict.get("axis") == 2:
                #if abs(event.dict.get("value")) > 0.1:
                #    print(event.dict)
                pass
        counter = counter +1

        if event_dict.get("joy") == 0: #full stop button
            SEND_EVERY = 0.05
            last_send_time = 0
            if event_dict.get("button") == 0:
                a_recent_speed = 1500
                b_recent_speed = 1500
                c_recent_speed = 1500
                d_recent_speed = 1500
                writeToSerial(str(int(a_recent_speed)) + "a")
                writeToSerial(str(int(b_recent_speed)) + "b")
                writeToSerial(str(int(c_recent_speed)) + "c")
                writeToSerial(str(int(d_recent_speed)) + "d")

        if event_dict.get("button") == 10: #laser
            writeToSerial(str("10l")) # 10 doesnt matter just needs to be there because code expects it

        if event_dict.get("axis") == 4: #gripper open
            degrees = translate(event.dict.get("value"), -1,1,0,180)
            print(degrees)
            current_time = time.time()
            if current_time > last_send_time + SEND_EVERY:
                last_send_time = current_time
                writeToSerial(str(int(degrees)) + "y")
        if event_dict.get("axis") ==5: #gripper close
            degrees = translate(event.dict.get("value"), -1,1,0,180)
            print(degrees)
            current_time = time.time()
            if current_time > last_send_time + SEND_EVERY:
                last_send_time = current_time
                writeToSerial(str(int(degrees)) + "z")

        if event_dict.get("axis") == 2: # thruster's going forward to backward (right joystick x axis)
            x_position = event.dict.get("value")
            if int(x_position) != x_last_speed:
                x_last_speed = x_position

        if event_dict.get("axis") == 3: # thruster's going up and down (right joystick y axis)
            y_position = event.dict.get("value")
            if int(y_position) != y_last_speed:
                y_last_speed = y_position
        #print(str(x_position) + "x   " + str(y_position) + "y")

        if event_dict.get("axis") == 1: # thruster's pitching up and down (left joystick y axis)
            p_position = event.dict.get("value")
            if int(p_position) != p_last_speed:
                p_last_speed = p_position

        if event_dict.get("axis") == 0: # thruster's yawing left and right (left joystick x axis)
            s_position = event.dict.get("value")
            if int(s_position) != s_last_speed:
                s_last_speed = s_position
                p_last_speed = p_position





        if abs(x_position)>abs(y_position) and abs(x_position)>abs(p_position) and abs(x_position)>abs(s_position): #x should be preferred -forward & backward
            speed_forward = myround(translate(x_position,-1,1,speed_fb_min,speed_fb_max)) #forward
            if int(speed_forward) != c_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_forward)) + "c") # c is forward thruster
                    c_recent_speed = speed_forward

            # was previously [1400, 1500]
            speed_backward = myround(translate(x_position, 1,-1,speed_fb_max,speed_fb_min)) #backward
            if int(speed_backward) != d_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_backward)) + "d") # d is backward thruster
                    d_recent_speed = speed_backward

            speed_down = myround(translate(abs(x_position), 0,1,STOP_INT,speed_fb_d_max)) # between 1500 and 1600
            if int(speed_down) != b_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_down)) + "b")
                    b_recent_speed = speed_down
            speed_up = myround(translate(abs(x_position), 0,1,STOP_INT,speed_fb_u_min)) # between 1500 and 1400
            if int(speed_up) != a_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_up)) + "a")
                    a_recent_speed = speed_up
            print(str(speed_backward) + "d    " + str(speed_forward) + "c   " + str(speed_down) + "b  " + str(speed_up) + "a  ")

        elif abs(y_position)>abs(x_position) and abs(y_position)>abs(p_position) and abs(y_position)>abs(s_position): # if y is greater than x (up and down)

            speed_up_1 = myround(translate(y_position, -1,1,speed_ud_max,speed_ud_min)) #up
            if int(speed_up_1) != a_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_up_1)) + "a")
                    a_recent_speed = speed_up_1

            speed_down_1 = myround(translate(y_position,1,-1,speed_ud_min,speed_ud_max)) #down
            if int(speed_down_1) != b_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_down_1)) + "b")
                    b_recent_speed = speed_down_1

            # Zero out the forward/backward directions
            if c_recent_speed != STOP_INT:
                writeToSerial(STOP + "c")
                c_recent_speed = STOP_INT
            if d_recent_speed != STOP_INT:
                writeToSerial(STOP + "d")
                d_recent_speed = STOP_INT
            #print(str(speed_up_1) + "a  " + str(speed_down_1) + "b   " + "1500c   " +   "1500d   " )

        elif abs(p_position)>abs(s_position) and abs(p_position)>abs(x_position) and abs(p_position)>abs(y_position) and abs(p_position) > .05: # x should be preferred (turn right(yaw))

            speed_up_1 = myround(translate(p_position, -1,1,1700,1500)) #pitch up
            if int(speed_up_1) != a_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_up_1)) + "a")
                    a_recent_speed = speed_up_1

            speed_down_1 = myround(translate(p_position,1,-1,1700,1500)) #pitch down
            if int(speed_down_1) != b_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_down_1)) + "b")
                    b_recent_speed = speed_down_1

            # Zero out the forward/backward directions
            if c_recent_speed != STOP_INT:
                writeToSerial(STOP + "c")
                c_recent_speed = STOP_INT
            if d_recent_speed != STOP_INT:
                writeToSerial(STOP + "d")
                d_recent_speed = STOP_INT
        elif abs(s_position)>abs(p_position) and abs(s_position)>abs(x_position) and abs(s_position)>abs(y_position) and abs(s_position) > .05: # x should be preferred (turn right(yaw))
            print(str(s_position) + " s_position")
            print(str(p_position) + " p_position")
            print(str(x_position) + " x_position") 
            print(str(y_position) + " y_position")
            speed_forward = myround(translate(s_position,-1,1,1300,1700)) #turn right
            if int(speed_forward) != c_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_forward)) + "c") # c is forward thruster
                    c_recent_speed = speed_forward

            # was previously [1400, 1500]
            speed_backward = myround(translate(s_position, 1,-1,1300,1700)) #turn left
            if int(speed_backward) != d_recent_speed:
                current_time = time.time()
                if current_time > last_send_time + SEND_EVERY:
                    last_send_time = current_time
                    writeToSerial(str(int(speed_backward)) + "d") # d is backward thruster
                    d_recent_speed = speed_backward

            if a_recent_speed != STOP_INT:
                writeToSerial(STOP + "a")
                a_recent_speed = STOP_INT
            if b_recent_speed != STOP_INT:
                writeToSerial(STOP + "b")
                b_recent_speed = STOP_INT
                
        else:
            if a_recent_speed != STOP_INT:
                writeToSerial(STOP + "a")
                a_recent_speed = STOP_INT
            if b_recent_speed != STOP_INT:
                writeToSerial(STOP + "b")
                b_recent_speed = STOP_INT
            if c_recent_speed != STOP_INT:
                writeToSerial(STOP + "c")
                c_recent_speed = STOP_INT
            if d_recent_speed != STOP_INT:
                writeToSerial(STOP + "d")
                d_recent_speed = STOP_INT
        









incoming = readIncomingMessages()
if incoming:
    print(incoming)


#log_file.close()

pygame.time.wait(15)
out = ser.readline()
if out:
    print(out.decode(), end = '')
# Write your code here :-)
