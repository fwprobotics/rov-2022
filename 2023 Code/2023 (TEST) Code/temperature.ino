#include <Wire.h>
#include "TSYS01.h"

TSYS01 sensor;

void setup() {
    Serial.begin(9600);
    Serial.println("Starting");

    Wire.begin();
  
    while (!sensor.init()) {
        Serial.println("TSYS01 device failed to initialize!");
        delay(2000);
    }
}

void loop() {
    sensor.read();
    Serial.print("Temperature: ");
    Serial.print(sensor.temperature()); 
    Serial.println(" deg C");
    delay(1000);
}
