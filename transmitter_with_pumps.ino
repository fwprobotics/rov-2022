
#include "RTClib.h"
#include <RH_ASK.h>
#include <SPI.h> 
#include <Wire.h>
#include <Time.h>

RH_ASK rf_driver;
RTC_DS1307 rtc;

const int RELAY_PIN =  A3; // arduino pin conecting to the relay
const int RELAY_PIN_2 =A2;
const int buttonPin = 11;
bool pumpsOn = false;
int buttonState = 0;

void setup(){
    pinMode(RELAY_PIN, OUTPUT);//stating this is an output
    pinMode(RELAY_PIN_2,OUTPUT);
    pinMode(buttonPin, INPUT_PULLUP);
    rf_driver.init();
    Serial.begin(57600);
    #ifndef ESP8266
      while (!Serial); // wait for serial port to connect. Needed for native USB
    #endif
    if (! rtc.begin()) {
      Serial.println("Couldn't find RTC");
      Serial.flush();
      while (1) delay(10);
    }
    if (! rtc.isrunning()) {
      Serial.println("RTC is NOT running, let's set the time!");
      rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    }
    delay(60000);
}
void loop(){

    Serial.println ("Turning pumps on");
    digitalWrite(RELAY_PIN,HIGH);// here the pump will turn on
    digitalWrite(RELAY_PIN_2,HIGH);// here the pump will turn on
    pumpsOn = true;
    delay(2000);

    Serial.println("Turning Pumps off");
    digitalWrite(RELAY_PIN,LOW);
    digitalWrite(RELAY_PIN_2,LOW);
    pumpsOn = false;
    delay(5000);
    
    DateTime now = rtc.now();
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.print(':');
    Serial.print(now.second(), DEC);
    Serial.println();
    Serial.println();
    delay(1000);
  
      
    const char *msg = "Welcome to the Workshop!";
    char UTC_time [9];
    int num = snprintf(UTC_time, 9, "%02hhu:%02hhu:%02hhu" , now.hour(), now.minute(), now.second());
    rf_driver.send((uint8_t *)UTC_time, strlen(UTC_time));
    rf_driver.waitPacketSent();
    delay(1000);

}
