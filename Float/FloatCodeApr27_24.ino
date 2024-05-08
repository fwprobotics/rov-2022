#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile
#include <TimeLib.h>

RH_ASK driver;
#include <Wire.h>
#include "MS5837.h"

#include "SparkFun_ProDriver_TC78H670FTG_Arduino_Library.h" //Click here to get the library: http://librarymanager/All#SparkFun_ProDriver
PRODRIVER myProDriver; //Create instance of this object
int direction = 0;

typedef enum {
  SURFACE,
  RETRACTING,
  SINKING,
  BOTTOM,
  EXTENDING,
  FLOATING,
  DELAY,
  DONE,
} state_t;

state_t state = DELAY;

int time_in_state_s = 0;

const char* messages[60] = {};
int count = 0;  // the number of messages in the array to send
int times = 0;  // the number of times we've been in the surface state

//int depth = 0
///1 means that the syringe is going towards the tip.
///0 means that the syringe is going away from the tip.

MS5837 sensor;
void setup()
{
  Serial.begin(115200);

  Serial.println("Starting");
  myProDriver.begin(); // default settings

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

void collect_data()
{
  time_t t = now(); // store the current time in time variable t

  sensor.read();
  double pressure = sensor.pressure() * 0.1;
  //Serial.println(pressure);
  //depth = pressure / (997 * 9.80665);
  //   double pressure = 8898.88;
  //Serial.println(depth);

  char pressureStr[7];

  char timeStamp[23];
  dtostrf(pressure, 2, 2, pressureStr);
  sprintf(timeStamp, "EX01 %02d:%02d:%02d %7s kpa", hour(t), minute(t), second(t), pressureStr);
  char *msg =  timeStamp;
  //driver.send((uint8_t *)msg, strlen(msg));

  messages[count] = msg;
  Serial.println(messages[count]);
  count = count + 1;

}

void loop() {
  // put your main code here, to run repeatedly:

  if (state == DELAY) {
    //delay(60000);
    state = RETRACTING;
  }
  else if (state == RETRACTING) {
    collect_data();

    for (int i = 0; i < 3; i++) {
      myProDriver.step(250, direction);
      delay(733);
    }
    time_in_state_s += 5;
    Serial.print("RETRACTING ");
    Serial.println(time_in_state_s);
    if (time_in_state_s >= 87) {
      state = SINKING;
      time_in_state_s = 0;
      direction = 1;
    }
  }
  else if (state == SINKING) {
    collect_data();
    delay (5000);

    time_in_state_s += 5;
    Serial.print("SINKING ");
    Serial.println(time_in_state_s);
    if (time_in_state_s >= 60) {
      state = BOTTOM;
      time_in_state_s = 0;
    }
  }
  else if (state == BOTTOM) {
    collect_data();
    delay (5000);

    time_in_state_s += 5;
    Serial.print("BOTTOM ");
    Serial.println(time_in_state_s);
    if (time_in_state_s >= 5) {
      state = EXTENDING;
      time_in_state_s = 0;
    }
  }
  else if (state == EXTENDING) {
    collect_data();

    for (int i = 0; i < 3; i++) {
      myProDriver.step(250, direction);
      delay(733);
    }
    time_in_state_s += 5;
    Serial.print("EXTENDING ");
    Serial.println(time_in_state_s);
    if (time_in_state_s >= 87) {
      state = FLOATING;
      time_in_state_s = 0;
      direction = 0;
    }
  }
  else if (state == FLOATING) {
    collect_data();
    delay (5000);

    time_in_state_s += 5;
    Serial.print("FLOATING ");
    Serial.println(time_in_state_s);
    if (time_in_state_s >= 60) {
      state = SURFACE;
      time_in_state_s = 0;
    }
  }
  else if (state == SURFACE) {
    for (int i = 0; i < count; i++) {
      const char *msg = messages[i];
      Serial.println(*msg);
      Serial.println(msg);
//      Serial.println((uint8_t *)msg);
      driver.send((uint8_t *)msg, strlen(msg));

      driver.waitPacketSent();
    }
    count = 0;
    Serial.print("SURFACE");
    times = times + 1;
    if (times >= 2) {
      state = DONE;
    } else {
      state == RETRACTING;
    }
  }
}

