#include <Servo.h>

Servo myservo;  // create servo object to control a servo

const int ledPin = 13; // the pin that the LED is attached to
int incomingByte;      // a variable to read incoming serial data into

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object

  // initialize serial communication:
  Serial.begin(9600);
  //myservo.write(90);
  myservo.writeMicroseconds(1500);
  delay(7000);
  // initialize the LED pin as an output:
  // pinMode(ledPin, OUTPUT);
}

void loop() {
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    Serial.write(incomingByte);
    // if it's a capital H (ASCII 72), turn on the LED:
    if (incomingByte == 'N') {
       //myservo.write(90); // sets the servo position according to the scaled value
      //Serial.write('9');
      myservo.writeMicroseconds(1500);
    }
     if (incomingByte == 'F') {
       //myservo.write(115);
       myservo.writeMicroseconds(1620);
     }
     if (incomingByte == 'B') {
       //myservo.write(65); 
       myservo.writeMicroseconds(1380);
     }
  }
  delay(15);
}

