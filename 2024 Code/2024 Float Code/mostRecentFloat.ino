#include "SparkFun_ProDriver_TC78H670FTG_Arduino_Library.h" //Click here to get the library: http://librarymanager/All#SparkFun_ProDriver
PRODRIVER myProDriver; //Create instance of this object
int counter = 0;
int d = 0;
int x = 3;

float pressuredata[11];
float depthdata[11];
int whereArray = 0;
float currentDepth = 0.0;
float currentPressure = 0.0;
long int t1;
long int tnow;

#include <Wire.h>
#include "MS5837.h"
#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile
char buff[10];

MS5837 sensor;
RH_ASK driver;


void setup() {

  Serial.println("SparkFun ProDriver TC78H670FTG Example 1");
  myProDriver.begin(); // default settings

  if (!driver.init())
        Serial.println("init failed");
  Serial.begin(9600);
 
  Serial.println("Starting");
 
  Wire.begin();

  // Initialize pressure sensor
  // Returns true if initialization was successful
  // We can't continue with the rest of the program unless we can initialize the sensor
  while (!sensor.init()) {
    Serial.println("Init failed!");
    Serial.println("Are SDA/SCL connected correctly?");
    Serial.println("Blue Robotics Bar30: White=SDA, Green=SCL");
    Serial.println("\n\n\n");
    delay(5000);
  }
 
  sensor.setModel(MS5837::MS5837_30BA);
  sensor.setFluidDensity(997); // kg/m^3 (freshwater, 1029 for seawater)

    for(int i = 0; i < 24; i++) {
      myProDriver.step(250, d);
      delay(500);
    }

  t1 = millis();
}

void loop() {

  tnow = millis();

  myProDriver.step(125,d);
  delay(1000);
  counter = counter+1;
  Serial.println(counter);
  sensor.read();
  // pressuredata[whereArray] = sensor.pressure();

  currentDepth = sensor.depth();
  currentPressure = sensor.pressure();

  Serial.print("Depth: ");
  Serial.print(currentDepth);
  Serial.println(" m");


  Serial.print("Pressure: ");
  Serial.print(currentPressure);
  Serial.println(" mbar");
  // depthdata[whereArray] = sensor.depth();


  char timeStamp[36];
  char pressureStr[7];
  char depthStr[7];
  dtostrf(currentPressure, 2, 2, pressureStr);
  Serial.println(pressureStr);

  dtostrf(currentDepth, 2, 2, depthStr);
  Serial.println(depthStr);

    int secs = ((tnow-t1)/1000);
    sprintf(timeStamp, "EX01, %02d sec, %7s kpa, %7s m", secs, pressureStr, depthStr);
    Serial.println(timeStamp);

    driver.send((uint8_t *)timeStamp, strlen(timeStamp));
    driver.waitPacketSent(); 
    delay(1000);

  if(currentDepth <= -2.5) {
    delay(20000); // wait 20 seconds

      for(int j = 0; j < 20; j++) { // slowly let out water
        sensor.read();
        myProDriver.step(125, 1);

        currentDepth = sensor.depth();
        currentPressure = sensor.pressure();

        char timeStamp[36];
        char pressureStr[7];
        char depthStr[7];
        dtostrf(currentPressure, 2, 2, pressureStr);
        Serial.println(pressureStr);

        dtostrf(currentDepth, 2, 2, depthStr);
        Serial.println(depthStr);

        int secs = ((tnow-t1)/1000);
        sprintf(timeStamp, "EX01, %02d sec, %7s kpa, %7s m", secs, pressureStr, depthStr);
        Serial.println(timeStamp);

        driver.send((uint8_t *)timeStamp, strlen(timeStamp));
        driver.waitPacketSent(); 

        delay(1000);
    }
    
  }
}


///0 means that the pump is going towards the dry container
///1 means that the pump is going towards the tip of the syringe
