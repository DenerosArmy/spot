int relay = 12;

void setup() {
  Serial.begin(9600);
  pinMode(relay, OUTPUT);
}

void loop() {
  char incomingByte;
  while (Serial.available() > 0) {
    incomingByte = (char)Serial.read();
    if (incomingByte == 'n') {
      digitalWrite(relay, HIGH); 
    }
    else if (incomingByte == 'f') {
      digitalWrite(relay, LOW); 
    }
  }
}
