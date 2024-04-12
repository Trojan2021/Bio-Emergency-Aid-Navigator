// Adafruit IO Dashboard Setup Example
//
// Adafruit invests time and resources providing this open source code.
// Please support Adafruit and open source hardware by purchasing
// products from Adafruit!
//
// Written by Todd Treece for Adafruit Industries
// Copyright (c) 2016 Adafruit Industries
// Licensed under the MIT license.
//
// All text above must be included in any redistribution.

/************************** Configuration ***********************************/

// edit the config.h tab and enter your Adafruit IO credentials
// and any additional configuration needed for WiFi, cellular,
// or ethernet clients.
#include "config.h"
#include <TinyGPS++.h>
#include "HardwareSerial.h"

/************************ Example Starts Here *******************************/

#define RXD2 39
#define TXD2 38
#define MAX_STRING_LENGTH 100


TinyGPSPlus gps;
HardwareSerial gps_serial(2);
AdafruitIO_Feed *feed = io.feed("GPS");
int flag = 1;

void setup() {

  // start the serial connection
  Serial.begin(115200);
  gps_serial.begin(9600, SERIAL_8N1, RXD2, TXD2);


  // wait for serial monitor to open
  while (!Serial)
    ;

  // connect to io.adafruit.com
  Serial.print("Connecting to Adafruit IO");
  io.connect();

  // wait for a connection
  while (io.status() < AIO_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  // we are connected
  Serial.println();
  Serial.println(io.statusText());

  char c;
}

void loop() {
  static char stringBuilder[MAX_STRING_LENGTH];  // Buffer to store the string
  static int index = 0;                          // Index to keep track of current position in the buffer

  io.run();

  if (gps_serial.available()) {
    while (flag) {
      if (char(gps_serial.read()) == \n) {
        flag = 0;
      }
    }
    c = char(gps_serial.read());
    if (c == '\n') {                // If newline character is encountered
      stringBuilder[index++] = c;   // Append newline character to the string
      stringBuilder[index] = '\0';  // Null-terminate the string
      Serial.println("String received: ");
      Serial.println(stringBuilder);  // Print the string
      feed->save(char(gps_serial.read()));
      index = 0;  // Reset index for next string
      delay(10000);
    } else {
      stringBuilder[index++] = c;
    }
  } else {
    delay(1000);
  }
}
