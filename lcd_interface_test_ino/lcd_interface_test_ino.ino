#include <LiquidCrystal.h>

char m;
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("hello world!");
  delay(1000);
  Serial.begin(9600);
}
void loop() {
  if (Serial.available()) {
    m=Serial.read();
    if(m=='1'){
      //Serial.println(1);
      lcd.print("Message 1 from Raspberry pi");
      delay(1000);
    }
    else if(m=='2'){
      //Serial.println(2);
      lcd.print("Message 2 from Raspberry pi");
      delay(1000);
    }
    else if(m=='3'){
      //Serial.println(3);
      lcd.print("Message 3 from Raspberry pi");
      delay(1000);
    }
    else{
      //Serial.println("Wrong no");
      lcd.print(" No message from Raspberry pi");
      delay(1000);
    }

  }
}

