#include <Servo.h>
#include <Wire.h>
#include "TSYS01.h"
int servoPin = 9;
int servoPosition = 0;
Servo myservo_1;
Servo myservo_2;
Servo mythruster_forward;
Servo mythruster_backward;
Servo mythruster_up;
Servo mythruster_down;

TSYS01 sensor;


void setup() { // put your setup code here, to run once:
  Serial.begin(19200);
  myservo_1.attach(9);
  myservo_2.attach(10);

  mythruster_up.attach(2);
  mythruster_down.attach(3);
  mythruster_forward.attach(4);
  mythruster_backward.attach(5);

  delay(7000);
  Serial.println("Start!");

Wire.begin();
while (!sensor.init()) {
  Serial.println("TSYS01 device failed to initialize!");
  delay(2000);
 }

}

void loop() {
  // put your main code here, to run repeatedly:
  sensor.read();
  Serial.print("Temperature: ");
  Serial.print(sensor.temperature()); 
  Serial.println(" deg C");

  if(Serial.available()){

    int speed = Serial.parseInt();
    char ch = Serial.read();
    if(ch=='y'){
      myservo_1.write(speed);
    } if(ch =='z'){
      myservo_2.write(speed);
    } if(ch=='a'){
      mythruster_up.writeMicroseconds(speed);
    } if(ch=='b'){
      mythruster_down.writeMicroseconds(speed);
    } if (ch=='c'){
      mythruster_forward.writeMicroseconds(speed);
    } if (ch=='d'){
      mythruster_backward.writeMicroseconds(speed);
    }
  }
}
