//integrated with laser
#include <Servo.h>
// #include <Wire.h>
// #include "TSYS01.h"
int servoPin = 9;
int servoPosition = 0;
Servo myservo_1;
Servo myservo_2;
Servo mythruster_forward;
Servo mythruster_backward;
Servo mythruster_up;
Servo mythruster_down;
bool on = false;
unsigned long mytime = millis();

// TSYS01 sensor;


void setup() { // put your setup code here, to run once:
  Serial.begin(19200);
  myservo_1.attach(9);
  myservo_2.attach(10);

  mythruster_up.attach(5);
  mythruster_down.attach(4);
  mythruster_forward.attach(3);
  mythruster_backward.attach(7);

  pinMode(2, OUTPUT);
  pinMode(6, OUTPUT);

  delay(7000);
  Serial.println("Start!");

// Wire.begin();
// while (!sensor.init()) {
//   Serial.println("TSYS01 device failed to initialize!");
//   delay(2000);
//  }

}

void loop() {
  // put your main code here, to run repeatedly:
  // sensor.read();
  // Serial.print("Temperature: ");
  // Serial.print(sensor.temperature()); 
  // Serial.println(" deg C");

  if(Serial.available()){

    int speed = Serial.parseInt();
    char ch = Serial.read();
    if(ch=='y'){
      myservo_1.write(speed);
    } if(ch =='z'){
      myservo_2.write(speed);
    } if (ch=='l' && on==false && millis()-mytime > 500){
      digitalWrite(6, HIGH);
      mytime = millis();
      on = true;
    } if (ch=='l' && on==true && millis()-mytime > 500){
      digitalWrite(6, LOW);
      mytime = millis();
      on = false;
      
    
      // digitalWrite(2, LOW);
    }if(ch=='a'){
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
