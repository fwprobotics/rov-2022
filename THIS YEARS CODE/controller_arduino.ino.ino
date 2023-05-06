#include <Servo.h>

#define THRUSTERS 4 // the number of Thrusters
#define STOP 1500

#define SERVOS 4 // the number of Servos

int thrusterPins[THRUSTERS] = {2, 3, 4, 5}; // Thrusters on pins 2 to 5
Servo thrusters[THRUSTERS];

int servoPins[SERVOS] = {8, 9, 11, 10}; // Servos on pins 6 to 9  (w and x are camera; y and z are claws)
Servo servos[SERVOS];

int servoPositions[SERVOS] = {10,10, 0, 0}; 


#define MAX_THRUSTER_STEP 5
int lastThrusterSpeeds[THRUSTERS] = {1500, 1500, 1500, 1500};
int desiredThrusterSpeeds[THRUSTERS] {1500, 1500, 1500, 1500};
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) > (b) ? (a) : (b))

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
  Serial.println("Started!");

}

void loop() {
  serviceSerial();

  // Go through all the thrusters
  for(uint8_t i = 0; i < THRUSTERS; ++i)
  {
    // Get the speed the pilot set
    int speed = desiredThrusterSpeeds[i];
    if(speed > STOP)
    {
      // If it is in a faster forward direction, only ramp up a small step
      if(speed > lastThrusterSpeeds[i]) {
        speed = MIN(lastThrusterSpeeds[i] + MAX_THRUSTER_STEP, speed);
      }
    } else if (speed < STOP) {
      // If it is in a faster reverse direction, only ramp up a small step
      if(speed < lastThrusterSpeeds[i]) {
        speed = MAX(lastThrusterSpeeds[i] - MAX_THRUSTER_STEP, speed);
      }
    }
    // If the speed we're ramping to isn't the speed the thruster is
    //  spinning at, set the thruster to the new speed.
    if(speed != lastThrusterSpeeds[i]) {
      lastThrusterSpeeds[i] = speed;   
      thrusters[i].write(speed);
      Serial.print("Thruster "); 
      Serial.print(i);
      Serial.print("   ramped to ");
      Serial.println(speed);
    }
  }
  
  
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
        char thrusterIndex = ch - 'a';
        Serial.print("Thruster "); 
        Serial.print(thrusterIndex + 1);
        Serial.print("   set to ");
        Serial.println(speed);
        desiredThrusterSpeeds[thrusterIndex] = speed;
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
        servoPositions[ch - 'y' + 2] = speed;
        servos[ch - 'y' + 2].write(servoPositions[ch - 'y' + 2] );  
        
   }
      
  }
}