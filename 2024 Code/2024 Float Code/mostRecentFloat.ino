#include "SparkFun_ProDriver_TC78H670FTG_Arduino_Library.h" //Click here to get the library: http://librarymanager/All#SparkFun_ProDriver
#include <Wire.h>
#include "MS5837.h"
#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile

PRODRIVER myProDriver; //Create instance of this object

float pressuredata[48];
float depthdata[48];
int secsdata[48];
int whereArray = 0;
float currentDepth = 0.0;
float currentPressure = 0.0;
long int t1;
long int tnow;
int secs;
int counter = 0;

char timeStamp[36];
char pressureStr[7];
char depthStr[7];

MS5837 sensor;
RH_ASK driver;

void setup() {

  t1 = millis();

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
    myProDriver.step(250, 0);
    delay(500);
    if(i%3 == 0) {
      tnow = millis();
      sensor.read();
      currentDepth = sensor.depth();
      currentPressure = sensor.pressure();
      pressuredata[whereArray] = currentPressure;
      depthdata[whereArray] = currentDepth;
      secsdata[whereArray] = tnow;
      whereArray++;

      // remove this eventually
      dtostrf(currentPressure, 2, 2, pressureStr);
      Serial.println(pressureStr);

      dtostrf(currentDepth, 2, 2, depthStr);
      Serial.println(depthStr);

      secs = (tnow/1000);
      sprintf(timeStamp, "EX01, %02d sec, %7s kpa, %7s m", secs, pressureStr, depthStr);
      Serial.println(timeStamp);

      driver.send((uint8_t *)timeStamp, strlen(timeStamp));
      driver.waitPacketSent(); 
    }
  }
}

void loop() {

  tnow = millis();

  myProDriver.step(125, 0);
  counter++;
  delay(1000);

  if(counter%3 == 0) {
    sensor.read();
    currentDepth = sensor.depth();
    currentPressure = sensor.pressure();
    pressuredata[whereArray] = currentPressure;
    depthdata[whereArray] = currentDepth;
    secsdata[whereArray] = tnow-t1;
    whereArray++;

    // remove this when we're done
      dtostrf(currentPressure, 2, 2, pressureStr);
      Serial.println(pressureStr);

      dtostrf(currentDepth, 2, 2, depthStr);
      Serial.println(depthStr);

      secs = ((tnow-t1)/1000);
      sprintf(timeStamp, "EX01, %02d sec, %7s kpa, %7s m", secs, pressureStr, depthStr);
      Serial.println(timeStamp);

      driver.send((uint8_t *)timeStamp, strlen(timeStamp));
      driver.waitPacketSent(); 
  }


  if(currentDepth <= -2 || millis() > 90000) { //450000
    for(int x = 0; x < 4; x++) {
      delay(5000);
      tnow = millis();
      sensor.read();
      currentDepth = sensor.depth();
      currentPressure = sensor.pressure();
      pressuredata[whereArray] = currentPressure;
      depthdata[whereArray] = currentDepth;
      secsdata[whereArray] = tnow-t1;
      whereArray++;

    }
    tnow = millis();

    for(int j = 0; j < 20; j++) { // slowly let out water
      tnow = millis();
      myProDriver.step(125, 1);
      if(j%3 == 0) {
        sensor.read();
        currentDepth = sensor.depth();
        currentPressure = sensor.pressure();
        pressuredata[whereArray] = currentPressure;
        depthdata[whereArray] = currentDepth;
        secsdata[whereArray] = tnow-t1;
        whereArray++;

        // remove eventually
        dtostrf(currentPressure, 2, 2, pressureStr);
        Serial.println(pressureStr);

        dtostrf(currentDepth, 2, 2, depthStr);
        Serial.println(depthStr);

        int secs = ((tnow-t1)/1000);
        sprintf(timeStamp, "EX01, %02d sec, %7s kpa, %7s m", secs, pressureStr, depthStr);
        Serial.println(timeStamp);

        driver.send((uint8_t *)timeStamp, strlen(timeStamp));
        driver.waitPacketSent(); 
      }
  }

  sensor.read();
  currentDepth = sensor.depth();
  currentPressure = sensor.pressure();
  int i = 0;
  while(currentDepth < 0) {
    myProDriver.step(250, 1);
    i++;
    delay(500);
    if(i%5 == 0) {
      tnow = millis();
      sensor.read();
      currentDepth = sensor.depth();
      currentPressure = sensor.pressure();
      pressuredata[whereArray] = currentPressure;
      depthdata[whereArray] = currentDepth;
      whereArray++;

      // remove this eventually
      dtostrf(currentPressure, 2, 2, pressureStr);
      Serial.println(pressureStr);

      dtostrf(currentDepth, 2, 2, depthStr);
      Serial.println(depthStr);

      secs = (tnow/1000);
      sprintf(timeStamp, "EX01, %02d sec, %7s kpa, %7s m", secs, pressureStr, depthStr);
      Serial.println(timeStamp);

      driver.send((uint8_t *)timeStamp, strlen(timeStamp));
      driver.waitPacketSent(); 
    }

  }

  // code to transmit all to the station
  for (byte i = 0; i < 48; i = i + 1) {
      currentDepth = depthdata[i];
      currentPressure = pressuredata[i];
      secs = secsdata[i];

      // remove this eventually
      dtostrf(currentPressure, 2, 2, pressureStr);
      Serial.println(pressureStr);

      dtostrf(currentDepth, 2, 2, depthStr);
      Serial.println(depthStr);

      sprintf(timeStamp, "EX01, %02d sec, %7s kpa, %7s m", secs, pressureStr, depthStr);
      Serial.println(timeStamp);

      driver.send((uint8_t *)timeStamp, strlen(timeStamp));
      driver.waitPacketSent(); 
      delay(500);
    } 

    for(int i = 0; i < 24; i++) {
      myProDriver.step(250, 0);
      delay(500);
      if(i%5 == 0) {
        tnow = millis();
        sensor.read();
        currentDepth = sensor.depth();
        currentPressure = sensor.pressure();
        pressuredata[whereArray] = currentPressure;
        depthdata[whereArray] = currentDepth;
        secsdata[whereArray] = tnow;
        whereArray++;

        // remove this eventually
        dtostrf(currentPressure, 2, 2, pressureStr);
        Serial.println(pressureStr);

        dtostrf(currentDepth, 2, 2, depthStr);
        Serial.println(depthStr);

        secs = (tnow/1000);
        sprintf(timeStamp, "EX01, %02d sec, %7s kpa, %7s m", secs, pressureStr, depthStr);
        Serial.println(timeStamp);

        driver.send((uint8_t *)timeStamp, strlen(timeStamp));
        driver.waitPacketSent(); 
      }
    }

    t1 = millis();
  }
}

///0 means that the pump is going towards the dry container
///1 means that the pump is going towards the tip of the syringe
