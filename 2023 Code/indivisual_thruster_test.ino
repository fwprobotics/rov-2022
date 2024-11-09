#include <Servo.h>
Servo myservo;
Servo mythruster;
int pls = 0;
const int buttonPin1 = 3;
const int buttonPin2 = 13;
int buttonState = 0;
void setup() {
pinMode(buttonPin1, INPUT_PULLUP);
pinMode(buttonPin2, INPUT_PULLUP);
myservo.attach(9);
Serial.begin (9600);
mythruster.attach(10);

}
void loop() {
// put your main code here, to run repeatedly:
buttonState = digitalRead(buttonPin1);
Serial.println(buttonState);
if (buttonState == HIGH) {
  mythruster.writeMicroseconds(1500);
} else  {
    mythruster.writeMicroseconds(1300);
}

buttonState = digitalRead(buttonPin2);
Serial.println(buttonState);
if(buttonState ==HIGH){
  myservo.write(90);
}else{
  myservo.write(0);
}

}
