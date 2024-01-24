#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile
#include <TimeLib.h>

RH_ASK driver;
#include <Wire.h>
#include "MS5837.h"

MS5837 sensor;
void setup()
{
    Serial.begin(9600);	  // Debugging only

  Serial.println("Starting");

  Wire.begin();

  // // Initialize pressure sensor
  // // Returns true if initialization was successful
  // // We can't continue with the rest of the program unless we can initialize the sensor
  while (!sensor.init()) {
    Serial.println("Init failed!");
    Serial.println("Are SDA/SCL connected correctly?");
    Serial.println("Blue Robotics Bar30: White=SDA, Green=SCL");
    Serial.println("\n\n\n");
    delay(5000);
  }

  if (!driver.init())
         Serial.println("receiver init failed");

  // .init sets the sensor model for us but we can override it if required.
  // Uncomment the next line to force the sensor model to the MS5837_30BA.
  //sensor.setModel(MS5837::MS5837_30BA);


  sensor.setFluidDensity(997); // kg/m^3 (freshwater, 1029 for seawater)
  sensor.read();
}

void loop()
{
  time_t t = now(); // store the current time in time variable t 
  
  sensor.read();
  double pressure = sensor.pressure()*0.1;
  Serial.println(pressure);
  // double pressure = 8898.88;

  char pressureStr[7];

    char timeStamp[23];
    dtostrf(pressure, 2, 2, pressureStr);
    sprintf(timeStamp, "EX01 %02d:%02d:%02d %7s kpa", hour(t), minute(t), second(t), pressureStr);
    const char *msg =  timeStamp;
    driver.send((uint8_t *)msg, strlen(msg));
    driver.waitPacketSent(); 
    delay(1000);
}

