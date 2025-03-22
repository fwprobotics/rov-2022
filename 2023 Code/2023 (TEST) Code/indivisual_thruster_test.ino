#include <Servo.h>
Servo mythruster;
void setup() {
Serial.begin (9600);
mythruster.attach(4);

}
void loop() {
// put your main code here, to run repeatedly:
  mythruster.writeMicroseconds(1500);
  delay(2000);
  mythruster.writeMicroseconds(1300);
  delay(2000);

}
