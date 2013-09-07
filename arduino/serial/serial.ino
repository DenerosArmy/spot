String incomingString;

void setup(){
  Serial.begin(9600);
  Serial.flush();
}

void loop() {
  delay(1000);
  // Check if there's incoming serial data.
  while (Serial.available() > 0) {
    // Read a byte from the serial buffer.
    char incomingByte = (char)Serial.read();
    incomingString += incomingByte;
  }

  if (incomingString != "") {
    // Message completely received
    Serial.println(incomingString);
    incomingString = "";
  }
}
