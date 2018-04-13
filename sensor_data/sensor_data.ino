// Test code for Ultimate GPS Using Hardware Serial (e.g. GPS Flora or FeatherWing)
//
// This code shows how to listen to the GPS module via polling. Best used with
// Feathers or Flora where you have hardware Serial and no interrupt
//
// Tested and works great with the Adafruit GPS FeatherWing
// ------> https://www.adafruit.com/products/3133
// or Flora GPS
// ------> https://www.adafruit.com/products/1059
// but also works with the shield, breakout
// ------> https://www.adafruit.com/products/1272
// ------> https://www.adafruit.com/products/746
// 
// Pick one up today at the Adafruit electronics shop
// and help support open source hardware & software! -ada
     
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>
//#include <max6675.h>

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
double rpm_data = 0;
double speed_data = 0;


unsigned int thermoDO_1 = 4;
unsigned int thermoCS_1 = 5;
unsigned int thermoCLK_1 = 6;
//MAX6675 thermocouple_1(thermoCLK_1, thermoCS_1, thermoDO_1);
String thermocouple_1_data = "0";

unsigned int thermoDO_2 = 7;
unsigned int thermoCS_2 = 8;
unsigned int thermoCLK_2 = 9;
//MAX6675 thermocouple_2(thermoCLK_2, thermoCS_2, thermoDO_2);
String thermocouple_2_data = "0";


//GPS::::

SoftwareSerial mySerial(10, 11); // RX, TX

// what's the name of the hardware serial port?
#define GPSSerial mySerial

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);
     
// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t timer = millis();


String latitude = "0";
String longitude = "0";
String speed_gps = "0";
String altitude_gps = "0";

void setup()
{
  // put your setup code here, to run once:
  pinMode(rpm_pin, INPUT);
  //pinMode(speed_pin, INPUT);
  Serial.begin(115200);
  previous_time_rpm = micros();

  //GPS:
  //while (!Serial);  // uncomment to have the sketch wait until Serial is ready
  
  // connect at 115200 so we can read the GPS fast enough and echo without dropping chars
  // also spit it out
  Serial.begin(115200);
  //Serial.println("Adafruit GPS library basic test!");
     
  // 9600 NMEA is the default baud rate for Adafruit MTK GPS's- some use 4800
  GPS.begin(9600);
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // uncomment this line to turn on only the "minimum recommended" data
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
  // the parser doesn't care about other sentences at this time
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate
  // For the parsing code to work nicely and have time to sort thru the data, and
  // print it out we don't suggest using anything higher than 1 Hz
     
  // Request updates on antenna status, comment out to keep quiet
  GPS.sendCommand(PGCMD_ANTENNA);

  delay(1000);
  
  // Ask for firmware version
  GPSSerial.println(PMTK_Q_RELEASE);
}

void loop() // run over and over again
{
  // put your main code here, to run repeatedly:
  //RPM data input
  mode_1_rpm = digitalRead(rpm_pin);
  if (mode_1_rpm == mode_2_rpm) {
    mode_2_rpm = not mode_1_rpm;
    current_time_rpm = micros();
    if (print_now_rpm == true) {
      rpm_data = (1000000 * 60 / (current_time_rpm - previous_time_rpm)); //print the rpm
      print_now_rpm = not print_now_rpm;
    }
    else {
      print_now_rpm = not print_now_rpm;
    }
    previous_time_rpm = current_time_rpm;
  }
  // read data from the GPS in the 'main loop'
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  if (GPSECHO)
    if (c) Serial.print(c);
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences!
    // so be very wary if using OUTPUT_ALLDATA and trytng to print out data
    //Serial.println(GPS.lastNMEA()); // this also sets the newNMEAreceived() flag to false
    if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
      return; // we can fail to parse a sentence in which case we should just wait for another
  }
  // if millis() or timer wraps around, we'll just reset it
  if (timer > millis()) timer = millis();
     
  // approximately every 50 milliseconds or so, print out the current stats - can't really do lower or it doesn't work
  if (millis() - timer > 50) {
    timer = millis(); // reset the timer
    /*
    Serial.print("\nTime: ");
    Serial.print(GPS.hour, DEC); Serial.print(':');
    Serial.print(GPS.minute, DEC); Serial.print(':');
    Serial.print(GPS.seconds, DEC); Serial.print('.');
    Serial.println(GPS.milliseconds);
    Serial.print("Date: ");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
    Serial.print("Fix: "); Serial.print((int)GPS.fix);
    Serial.print(" quality: "); Serial.println((int)GPS.fixquality);
    */
    if (GPS.fix) {
      /*
      Serial.print("Location: ");
      Serial.print(GPS.latitude, 4); Serial.print(GPS.lat);
      Serial.print(", ");
      Serial.print(GPS.longitude, 4); //Serial.println(GPS.lon);
      Serial.print("Speed (knots): "); Serial.println(GPS.speed);
      Serial.print("Angle: "); Serial.println(GPS.angle);
      Serial.print("Altitude: "); Serial.println(GPS.altitude);
      Serial.print("Satellites: "); Serial.println((int)GPS.satellites);
      */
      latitude = String((GPS.latitude), 4) + String(GPS.lat);
      longitude = String((GPS.longitude), 4) + String(GPS.lon);
      speed_gps = String(GPS.speed, 4);
      altitude_gps = String(GPS.altitude);
    }
  }
  Serial.println(String("asdf") + "," + String(rpm_data, num_decimal) + "," + speed_gps + "," + thermocouple_1_data + "," + thermocouple_2_data + "," + latitude + "," + longitude + "," + altitude_gps + "," );
}
