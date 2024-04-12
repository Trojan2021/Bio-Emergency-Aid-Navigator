//Change the code below by your sketch
//Code for Gps
#include <TinyGPS++.h>
#include "HardwareSerial.h"

static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;

// The TinyGPS++ object
TinyGPSPlus gps;


HardwareSerial gps_serial(2);

#define RXD2 39
#define TXD2 38

void setup() {
  // Note the format for setting a serial port is as follows: Serial2.begin(baud-rate, protocol, RX pin, TX pin);
  Serial.begin(9600);
 
 gps_serial.begin(9600, SERIAL_8N1, RXD2, TXD2);

 Serial.println("Serial Txd is on pin: "+String(TX));
 Serial.println("Serial Rxd is on pin: "+String(RX));
}

void loop() {
  while (gps_serial.available()) {
   Serial.print(char(gps_serial.read()));  // read from gps, write to serial debug port
  }
}