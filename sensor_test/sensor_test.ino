

void setup(){
  pinMode(2, INPUT);
  Serial.begin(9600);
}

void loop(){
  Serial.println("magnet_reading: " + String(digitalRead(2)));
  /*
  if(Serial.available()){
   //do something
   delay(1000);
   }
   */
  delay(10);
}

