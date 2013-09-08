#include <SoftwareSerial.h>

int relay = 12;
int bluetoothTx = 3;  // TX-O pin of bluetooth mate, Arduino D2
int bluetoothRx = 2;  // RX-I pin of bluetooth mate, Arduino D3

SoftwareSerial bluetooth(bluetoothTx, bluetoothRx);

void setup() {
  Serial.begin(9600
  );
  bluetooth.begin(9600);  // Start bluetooth serial at 9600
  pinMode(relay, OUTPUT);
}

void loop() {
  char incomingByte;
  if (bluetooth.available()) {
    incomingByte = (char)bluetooth.read();
    
    Serial.print(incomingByte);
    if (incomingByte == 'n') {
      digitalWrite(relay, HIGH); 
    }
    else if (incomingByte == 'f') {
      digitalWrite(relay, LOW); 
    }
  }
  
  if (Serial.available()) {
    bluetooth.print((char)Serial.read()); 
  }
}
