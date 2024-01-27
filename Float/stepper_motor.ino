#include "SparkFun_ProDriver_TC78H670FTG_Arduino_Library.h" //Click here to get the library: http://librarymanager/All#SparkFun_ProDriver
PRODRIVER myProDriver; //Create instance of this object

void setup() {
  Serial.begin(115200);
  Serial.println("SparkFun ProDriver TC78H670FTG Example 1");
  myProDriver.begin(); // default settings
}

void loop() {
  myProDriver.step(145000, 0); // 0 goes up/away from the tip
  delay(1000);
  myProDriver.step(145000, 1); // 1 goes down/towards the tip
  delay(1000);
}
