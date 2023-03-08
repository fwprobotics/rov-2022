const int RELAY_PIN =  A5; // arduino pin conecting to the relay

void setup(){
  pinMode(RELAY_PIN, OUTPUT);//stating this is an output
}
void loop(){
  digitalWrite(RELAY_PIN,HIGH);// here the pump will turn on
  delay(5000);// delayed for 5000 seconds
  digitalWrite(RELAY_PIN, LOW); // here the pump will  take out water 
  delay(5000); // delayed or stoped 5000 befor going back in the loop
}

