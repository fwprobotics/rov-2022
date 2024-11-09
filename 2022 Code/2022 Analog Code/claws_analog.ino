#include <Servo.h>

Servo myServo;
Servo myServo2;
int servoPin = 11; //a
int servoPin2 = 9; //b
void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
myServo.attach(servoPin);
myServo2.attach(servoPin2);
Serial.println("test");
}

void loop() {
  // put your main code here, to run repeatedly:
//myServo.write(0);
 if (Serial.available()>0)
  { 
     int speed = Serial.parseInt(); 
     char letter = Serial.read();
     Serial.println(speed);
     Serial.println(letter);
     if (speed != 0){
       if (letter == 'a'){

         
         myServo.write(speed);
       }
        if (letter == 'b'){
          myServo2.write(speed);
        }
      }
  }
 delay(15); 
}
