const int yellowButton = 1; // the yellow button is in pin 1
const int pump1Relay = 2; // the relay for pump 1 is connected to pin 2
const int greenButton = 3; // the green button is in pin 3
const int pump2Relay = 4; // the relay for pump 2 is connected to pin 4
int yellowButtonState;
int greenButtonState;
void setup()
{
pinMode(yellowButton, INPUT);
pinMode(pump1Relay, OUTPUT);
pinMode(greenButton, INPUT);
pinMode(pump2Relay, OUTPUT);
}
 
void loop()
{
yellowButtonState = digitalRead(yellowButton);
if (yellowButtonState == 0) // We press yellow the button
{
digitalWrite(pump1Relay, HIGH); // the 1st water pump fills the bottle
}
else // we release the button
{
digitalWrite(pump1Relay, LOW); // the 1st water pump stops
}
greenButtonState = digitalRead(greenButton); // we press the green button
if (greenButtonState == 0)
}
digitalWrite(pump2Relay, HIGH); // the 2nd water pump fills the bottle 
else //
{
digitalWrite(pump1Relay, LOW); // the water pump stops
}
}