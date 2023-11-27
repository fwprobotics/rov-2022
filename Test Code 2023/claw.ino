#include <Servo.h>
int servoPin = 9;
int servoPosition = 0;
Servo myservo_1;
Servo myservo_2;

void setup() { // put your setup code here, to run once:
  Serial.begin(19200);
  myservo_1.attach(9);
  myservo_2.attach(10);
  delay(1000);
  Serial.println("Start!");


}

void loop() {
  // put your main code here, to run repeatedly:
if(Serial.available()){

  int speed = Serial.parseInt();
  char ch = Serial.read();
  if(ch=='y'){
    myservo_1.write(speed);
  } if(ch =='z'){
    myservo_2.write(speed);
  }
}
}




