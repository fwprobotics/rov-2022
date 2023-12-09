#include <Servo.h>
int servoPin = 9;
int servoPosition = 0;
Servo myservo_1;
Servo myservo_2;
Servo mythruster_forward;
Servo mythruster_backward;
Servo mythruster_up;
Servo mythruster_down;




void setup() { // put your setup code here, to run once:
  Serial.begin(19200);
  myservo_1.attach(9);
  myservo_2.attach(10);

  mythruster_up.attach(1);
  mythruster_down.attach(2);
  mythruster_forward.attach(3);
  mythruster_backward.attach(4);

  delay(1000);
  Serial.println("Start!");


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
    mythruster_up.writeMicroseconds(speed)
  } if(ch=='b'){
    mythruster_down.writeMicroseconds(speed)
  } if (ch=='c'){
    mythruster_forward.writeMicroseconds(speed)
  } if (ch=='d'){
    mythruster_backward.writeMicroseconds(speed)
  }
}
}
