unsigned int rpm_pin = 2;
unsigned int speed_pin = 3;
unsigned int rate = 115200;
unsigned int delay_time = 10; //ms
float rpm_data = 0;
float speed_data = 0;

void setup(){
  pinMode(rpm_pin, INPUT);
  pinMode(speed_pin, INPUT);
  Serial.begin(rate);
}

void loop(){
  String rpm_data_string = String(rpm_data)[:3];
  String speed_data_string = String(rpm_data)[:3];
  Serial.println(rpm_data_string + "," + speed_data_string);
  delay(delay_time);
}

