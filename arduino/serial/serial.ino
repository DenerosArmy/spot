#include <Servo.h> 

String incomingString = String("");
Servo pan, tilt;

int theta = 0, phi = 0;
int panPin = 10, tiltPin = 11, buttonPin = 12; 

void setup(){
  Serial.begin(9600);
  Serial.flush();
  pan.attach(panPin);
  tilt.attach(tiltPin);
  pinMode(buttonPin, OUTPUT);
  aim('Z', 'Z');
}

void loop() { 
  // delay(10);
  char incomingByte;
  
  // Check if there's incoming serial data.
  //while (Serial.available() > 0) {
    // Read a byte from the serial buffer.
    if (Serial.available() > 0) {
      incomingByte = (char)Serial.read();
    }
    //Serial.print(incomingByte);
    // stop reading for now if we reach a break character
    if (incomingByte == '/') {
      execute(incomingString);
      incomingString = String("");
    }
    
    if (incomingByte != 'ÿ' && incomingByte != '') {
      incomingString += incomingByte;
    }
  //}
}
  

void execute(String command) {

  Serial.print("command: ");
  Serial.println(command);
    
  if (command == "/on") {
    Serial.println("turning on laser");
    press();
  }
  else if (command == "/off") {
    Serial.println("turning off laser");
    release();
  }
  else if (command == "/aim") {
    Serial.println(Serial.peek());
    while (Serial.available() < 2) {
       
    }
    aim((int)Serial.read(), (int)Serial.read());
  }
  else if (command == "/line") {
    Serial.println("drawing line");
    while (Serial.available() < 6) {
       
    }
    line((int)Serial.read(), (int)Serial.read(), (int)Serial.read(), (int)Serial.read(), (int)Serial.read(), (int)Serial.read());
  }
}

void press() {
  digitalWrite(buttonPin, HIGH);
}

void release() {
  digitalWrite(buttonPin, LOW);
}

void aim(int theta, int phi) {
  Serial.print("aiming at ");
  Serial.print(theta);
  Serial.print(", ");
  Serial.println(phi);
  
  pan.write(theta);
  tilt.write(phi);
}

void line(int theta1, int phi1, int theta2, int phi2, int time, int dt) {
  time *= 1000;
  Serial.print("drawing line from ");
  Serial.print(theta1);
  Serial.print(", ");
  Serial.print(phi1);
  Serial.print(" to ");
  Serial.print(theta2);
  Serial.print(", ");
  Serial.print(phi2);
  Serial.print(" over ");
  Serial.print(time);
  Serial.print("ms with timestep ");
  Serial.println(dt);
  
  
  int dth = (theta2 - theta1) / (time / dt);
  int dph = (phi2 - phi1) / (time / dt);
  
  if (dth == 0) dth = 1;
  if (dph == 0) dph = 1;
  
  int theta = theta1, phi = phi1;  
  
  for (int i = 0; i < time; i += dt) {
    pan.write(theta);
    tilt.write(phi);
    theta += dth;
    phi += dph;
    delay(dt);
  }
}
