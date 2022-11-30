void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
myServo.attach(servoPin);
myServo2.attach(servoPin2);
myServo3.attach(servoPin3);
myServo4.attach(servoPin4);

Serial.println("test");
}

void loop() {
  // put your main code here, to run repeatedly:
//myServo.write(0);
 if (Serial.available()>0)
  { 
     int speed = Serial.parseInt(); 
     char letter = Serial.read();
     Serial.println(speed);
     Serial.println(letter);
     if (speed != 0){
       if (letter == 'x'){ 
         myServo.write(speed);
       }
        if (letter == 'y'){
          myServo2.write(speed);
        }if (letter == 'a'){ 
         myServo3.write(speed);
       }
        if (letter == 'b'){ 
         myServo4.write(speed);
       }
       if (letter == 'c'){ 
         myServo5.write(speed);
       }
       if (letter == 'd'){ 
         myServo6.write(speed);
       }
      }
  }
 delay(15); 
}
