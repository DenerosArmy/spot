#include <Servo.h> 

String incomingString = String("");
Servo pan, tilt;

int theta = 0, phi = 0;
int panPin = 3, tiltPin = 2, buttonPin = 13; 

void setup(){
  Serial.begin(9600);
  Serial.flush();
  pan.attach(panPin);
  tilt.attach(tiltPin);
  pinMode(buttonPin, OUTPUT);
  digitalWrite(buttonPin, HIGH);
  aim('Z', '(');
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
    while (Serial.available() < 2) {
       Serial.println(Serial.peek());
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
  
  
  int theta = theta1;
  int phi = phi1;
  int t = 0;
  while (theta != theta2 || phi != phi2) {
    t += dt;
    if (t > time) {
      pan.write(theta2);
      tilt.write(phi2);
      break;
    }
    theta = theta1 + (theta2 - theta1) * t / time;
    phi = phi1 + (phi2 - phi1) * t / time;
    delay(dt);
    pan.write(theta);
    tilt.write(phi);
  }
}
