#include "SparkFun_ProDriver_TC78H670FTG_Arduino_Library.h" //Click here to get the library: http://librarymanager/All#SparkFun_ProDriver
PRODRIVER myProDriver; //Create instance of this object
int counter=0;
int direction = 0;
void setup() {
  Serial.begin(115200);
  Serial.println("SparkFun ProDriver TC78H670FTG Example 1");
  myProDriver.begin(); // default settings
}

void loop() {
 if (counter >= 0 && counter <= 60) {
      myProDriver.step(250,direction);
      delay(1000);
      counter = counter+1;
      Serial.println(counter);
 }
 else {
    counter = 0;
    if(direction == 1){
      direction = 0;
    }else{
      direction = 1;
    }
    delay(60000);

 }
}

///1 means that the pump is at the top of the tip
///0 means that the pump is at the bottem of the tip
