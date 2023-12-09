import json
import pygame
import serial
import serial.tools.list_ports
def myround(x, base=10):
    return base * round(x/base)



STOP_INT = 1500
STOP = '1500'


pygame.joystick.init()
print(pygame.joystick.get_count())
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)
pygame.init()

x_last_speed = 0
y_last_speed = 0
x_position = 0
y_position = 0

a_recent_speed = 0
b_recent_speed = 0
c_recent_speed = 0
d_recent_speed = 0

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
        
        if counter % 50 ==0:
            if event.dict.get("axis") ==3 or event.dict.get("axis") == 2:
                #if abs(event.dict.get("value")) > 0.1:
                #    print(event.dict)
                pass
        counter = counter +1
        
        
        if event_dict.get("axis") == 4:
            degrees=translate(event.dict.get("value"), -1,1,0,180)
            print(degrees)
            writeToSerial(str(int(degrees)) + "y")
        if event_dict.get("axis") ==5:
            degrees = translate(event.dict.get("value"), -1,1,0,180)
            print(degrees)
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
        
        
        if abs(x_position)>abs(y_position) :

            speed_forward = myround(translate(x_position,-1,1,1400,1600)) #forward
            if int(speed_forward) != c_recent_speed:
                writeToSerial(str(int(speed_forward)) + "c")
                c_recent_speed = speed_forward
  
            # was previously [1400, 1500]
            speed_backward = myround(translate(x_position, -1,1,1600,1400)) #backward
            if int(speed_backward) != d_recent_speed:
                writeToSerial(str(int(speed_backward)) + "d")
                d_recent_speed = speed_backward
            speed_down = myround(translate(abs(x_position), 0,1,1500,1550))
            if int(speed_down) != b_recent_speed:
                writeToSerial(str(int(speed_down)) + "b")
                b_recent_speed = speed_down
            speed_up = myround(translate(abs(x_position), 0,1,1500,1450))
            if int(speed_up) != a_recent_speed:
                writeToSerial(str(int(speed_up)) + "a")
                a_recent_speed = speed_up
            print(str(speed_backward) + "d    " + str(speed_forward) + "c   " + str(speed_down) + "b  " + str(speed_up) + "a  ")
            
        else :
            
            speed_up_1 = myround(translate(y_position, -1,1,1600,1400)) #up
            if int(speed_up_1) != a_recent_speed:
                writeToSerial(str(int(speed_up_1)) + "a")
                a_recent_speed = speed_up_1

            speed_down_1 = myround(translate(y_position,-1,1,1400,1600)) #down
            if int(speed_down_1) != b_recent_speed:
                writeToSerial(str(int(speed_down_1)) + "b")
                b_recent_speed = speed_down_1
                
            # Zero out the forward/backward directions
            if c_recent_speed != STOP_INT:
                writeToSerial(STOP + "c")
                c_recent_speed = STOP_INT
            if d_recent_speed != STOP_INT:
                writeToSerial(STOP + "d")
                d_recent_speed = STOP_INT
            print(str(speed_up_1) + "a  " + str(speed_down_1) + "b   " + "1500c   " +   "1500d   " )
            
log_file.close()

pygame.time.wait(15)
out = ser.readline()
if out:
    print(out.decode(), end = '')
