#include <Servo.h>

#define THRUSTERS 4 // the number of Thrusters
#define STOP 1500

#define SERVOS 4 // the number of Servos

int thrusterPins[THRUSTERS] = {2,3,4,5}; // Thrusters on pins 2 to 5
Servo thrusters[THRUSTERS];

int servoPins[SERVOS] = {10, 11, 6,9}; // Servos on pins 6 to 9 
Servo servos[SERVOS];

int servoPositions[SERVOS] = {10,10, 0, 0}; 





void setup() {
  Serial.begin(19200);
  for(int i=0; i < THRUSTERS; i++)
  { 
    thrusters[i].attach(thrusterPins[i]); 
    thrusters[i].writeMicroseconds(STOP);
  }

    for(int i=0; i < SERVOS; i++)
  { 
    servos[i].attach(servoPins[i], 1000, 2000); 
    servos[i].write(servoPositions[i]);
    
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
   if (ch >= 'w' && ch < 'w' + 2) 
   {
        Serial.print("Servo "); 
        Serial.print(ch - 'w' + 1);
        Serial.print("   add to speed ");
        Serial.println(speed);
       int currentServoPosition = servoPositions[ch - 'w'];

       if (speed >0 && currentServoPosition + speed <= 170) {
        servoPositions[ch - 'w'] = speed + currentServoPosition;
        servos[ch - 'w'].write(servoPositions[ch - 'w'] ); 
        Serial.println(servoPositions[ch - 'w'] );  
       }

       else if(speed<0 && currentServoPosition + speed >= 10) {
         servoPositions[ch - 'w'] = speed + currentServoPosition;
        servos[ch - 'w'].write(servoPositions[ch - 'w'] );  
        Serial.println(servoPositions[ch - 'w'] );
        
       }
   }
   if (ch >= 'y' && ch < 'y' + 2) {
        servoPositions[ch - 'y'] = speed;
        servos[ch - 'y'].write(servoPositions[ch - 'w'] );  
        
   }
      
  }
}
