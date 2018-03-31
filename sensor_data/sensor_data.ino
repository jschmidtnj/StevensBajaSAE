#include <max6675.h>

bool mode_1_rpm = false;
bool mode_2_rpm = not mode_1_rpm;
bool mode_1_speed = false;
bool mode_2_speed = not mode_1_speed;

double current_time_rpm = 0;
double previous_time_rpm = 0;
bool print_now_rpm = false;
double current_time_speed = 0;
double previous_time_speed = 0;
bool print_now_speed = false;

unsigned int diameter = 1; //in feet
unsigned int num_decimal = 2;
unsigned int rpm_pin = 2;
unsigned int speed_pin = 3;
unsigned int delay_time = 10; //ms
double rpm_data = 0;
double speed_data = 0;

unsigned int thermoDO_1 = 4;
unsigned int thermoCS_1 = 5;
unsigned int thermoCLK_1 = 6;
MAX6675 thermocouple_1(thermoCLK_1, thermoCS_1, thermoDO_1);
String thermocouple_1_data = "0";

unsigned int thermoDO_2 = 7;
unsigned int thermoCS_2 = 8;
unsigned int thermoCLK_2 = 9;
MAX6675 thermocouple_2(thermoCLK_2, thermoCS_2, thermoDO_2);
String thermocouple_2_data = "0";

void setup() {
  // put your setup code here, to run once:
  pinMode(rpm_pin, INPUT);
  pinMode(speed_pin, INPUT);
  Serial.begin(115200);
  previous_time_rpm = micros();
}

void loop() {
  // put your main code here, to run repeatedly:
  //RPM data input
  mode_1_rpm = digitalRead(rpm_pin);
  if (mode_1_rpm == mode_2_rpm) {
    mode_2_rpm = not mode_1_rpm;
    current_time_rpm = micros();
    if(print_now_rpm == true){
      rpm_data = (1000000 * 60 / (current_time_rpm - previous_time_rpm)); //print the rpm
      print_now_rpm = not print_now_rpm;
    }
    else{
      print_now_rpm = not print_now_rpm;
    }
    previous_time_rpm = current_time_rpm;
  }

  //speed data input
  mode_1_speed = digitalRead(speed_pin);
  if (mode_1_speed == mode_2_speed) {
    mode_2_speed = not mode_1_speed;
    current_time_speed = micros();
    if(print_now_speed == true){
      //mph = rpm * 60min/hr * pi * diameter_of_wheel (feet) / 5280 ft/mile
      speed_data = (1000000 * 60 / (current_time_speed - previous_time_speed)) * (60 * PI * diameter / 5280); //print the rpm
      print_now_speed = not print_now_speed;
    }
    else{
      print_now_speed = not print_now_speed;
    }
    previous_time_speed = current_time_speed;
  }

  String thermocouple_1_reading = String(thermocouple_1.readFahrenheit());
  if (thermocouple_1_reading != " NAN"){
    thermocouple_1_data = thermocouple_1_reading;
  }
  /*
  String thermocouple_2_reading = String(thermocouple_2.readFahrenheit());
  if (thermocouple_2_reading != " NAN"){
    thermocouple_2_data = thermocouple_2_reading;
  }
  */
  rpm_data = 700;
  speed_data = 60.55;
  thermocouple_2_data = 47.55;
  Serial.println(String(rpm_data, num_decimal) + "," + String(speed_data, num_decimal) + "," + thermocouple_1_data + "," + thermocouple_2_data + ",");
  //+ "," + String(thermocouple_2.readFahrenheit())
  delay(delay_time);
}
