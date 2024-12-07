#include <SoftwareSerial.h> // Include the SoftwareSerial library

// Define pins for SoftwareSerial
SoftwareSerial mySerial(2, 3); // RX pin connected to pin 2, TX pin connected to pin 3

void setup() {
  Serial.begin(57600); // Initialize the default serial communication
  mySerial.begin(57600); // Initialize the SoftwareSerial port at 9600 baud
}

void loop() {
  // Read data from SoftwareSerial if available
  if (mySerial.available()) {
    char data = mySerial.read(); // Read one byte
    Serial.print(data); // Print received data to the serial monitor
  }
  
  // Read data from the default serial port and send it to SoftwareSerial
  if (Serial.available()) {
    char data = Serial.read(); // Read one byte
    mySerial.write(data); // Send data to SoftwareSerial
  }
}
