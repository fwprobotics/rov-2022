
const int RELAY_PIN =  A5; // arduino pin conecting to the relay
const int RELAY_PIN_2 =A4;
const int buttonPin = 11;
bool pumpsOn = false;
int buttonState = 0;

void setup(){
  pinMode(RELAY_PIN, OUTPUT);//stating this is an output
  pinMode(RELAY_PIN_2,OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin (9600); 
}
void loop(){
  buttonState = digitalRead(buttonPin);
  if(buttonState == LOW){
    if (pumpsOn == false){
      Serial.println ("Turning pump's on");
      digitalWrite(RELAY_PIN,HIGH);// here the pump will turn on
      digitalWrite(RELAY_PIN_2,HIGH);// here the pump will turn on
      pumpsOn = true;
      delay(1000);
    }else{
      Serial.println("Turning Pumps off");
      digitalWrite(RELAY_PIN,LOW);
      digitalWrite(RELAY_PIN_2,LOW);
      pumpsOn = false;
      delay(1000);
    }
 }

}
