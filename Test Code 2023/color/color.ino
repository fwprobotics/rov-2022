#include <Servo.h>
int servoPin = 9;
int servoPosition = 0;
Servo myservo_1;
Servo myservo_2;
Servo mythruster_forward;
Servo mythruster_backward;
Servo mythruster_up;
Servo mythruster_down;

int blue = 2;
int red = 3;
int green = 4;
int white = 5; 
int yellow = 6;



void setup() { // put your setup code here, to run once:
  Serial.begin(19200);
  myservo_1.attach(9);
  myservo_2.attach(10);

  mythruster_up.attach(2);
  mythruster_down.attach(3);
  mythruster_forward.attach(4);
  mythruster_backward.attach(5);

  delay(7000);
  Serial.println("Start!");

  pinMode(blue, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(white, OUTPUT);
  pinMode(yellow, OUTPUT);


}

void loop() {
  // put your main code here, to run repeatedly:
if(Serial.available()){

  int speed = Serial.parseInt();
  char ch = Serial.read();
  if(ch=='y'){
    myservo_1.write(speed);
  } if(ch =='z'){
    myservo_2.write(speed);

  } if(ch=='a'){
    mythruster_up.writeMicroseconds(speed);
    digitalWrite(blue,HIGH);
  } if(ch=='b'){
    mythruster_down.writeMicroseconds(speed);
    digitalWrite(red, HIGH);
  } if (ch=='c'){
    mythruster_forward.writeMicroseconds(speed);
    digitalWrite(green, HIGH);
  } if (ch=='d'){
    mythruster_backward.writeMicroseconds(speed);
    digitalWrite(white, HIGH);
  }
}
}
