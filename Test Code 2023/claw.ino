#include <Servo.h>
int servoPin = 9;
int servoPosition = 0;
Servo myservo;

void setup() { // put your setup code here, to run once:
  Serial.begin(19200);
  myservo.attach(9,1000,2000);
  delay(1000);
  Serial.println("Start!");


}

void loop() {
  // put your main code here, to run repeatedly:
if(Serial.available()){
  char ch = Serial.read();
  if(ch=='w'){
    myservo.write(180);
  }else{
    myservo.write(0);
  }
}


}




