#include <Servo.h>
int servoPin = 9;

void setup() { // put your setup code here, to run once:
  Serial.begin(19200);
  myservo.attach(9,1000,2000);
  myservo.write(servoPosition(9));
  delay(1000);
  Serial.println("Start!");


}

void loop() {
  // put your main code here, to run repeatedly:

}
