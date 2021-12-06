#include <Servo.h>

#define THRUSTERS 4 // the number of Thrusters
#define STOP 1500

int thrusterPins[THRUSTERS] = {2,3,4,5}; // Thrusters on pins 2 to 5
Servo thrusters[THRUSTERS];


void setup() {
  Serial.begin(19200);
  for(int i=0; i < THRUSTERS; i++)
  { thrusters[i].attach(thrusterPins[i]); 
  thrusters[i].writeMicroseconds(STOP);
  }
  delay(7000);
  // put your setup code here, to run once:

}

void loop() {
  serviceSerial();
  delay(15);
  // put your main code here, to run repeatedly:

}
void serviceSerial()
{
  if (Serial.available())
  { 
    int speed = Serial.parseInt();
    char ch = Serial.read();
    if (ch >= 'a' && ch < 'a' + THRUSTERS)
     { 
        Serial.print("Thruster "); 
        Serial.print(ch - 'a' + 1);
        Serial.print("   set to ");
        Serial.println(speed);
       thrusters[ch - 'a'].write(speed);
      }
  }
}

