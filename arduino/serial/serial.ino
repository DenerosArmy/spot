#include <Servo.h> 

String incomingString;
Servo pan, tilt;

int theta = 0, phi = 0;
int panPin = 10, tiltPin = 11, buttonPin = 12; 

void setup(){
  Serial.begin(9600);
  Serial.flush();
  pan.attach(panPin);
  tilt.attach(tiltPin);
  pinMode(buttonPin, OUTPUT);
}

void loop() {
  // delay(10);
  
  // Check if there's incoming serial data.
  while (Serial.available() > 0) {
    // Read a byte from the serial buffer.
    char incomingByte = (char)Serial.read();
    // stop reading for now if we reach a break character
    if (incomingByte == '/') {
      break; 
    }
    incomingString += incomingByte;
  }

  Serial.println(incomingString);
    
  if (incomingString == "on") {
      press();
  }
  else if (incomingString == "off") {
      release();
  }
  else if (incomingString == "aim") {
      aim();
  }
  else if (incomingString == "line") {
      line();
  }
    
  incomingString = "";
}

void press() {
  digitalWrite(buttonPin, HIGH);
}

void release() {
  digitalWrite(buttonPin, LOW);
}

void aim() {
  
}

void line() {
  
}
