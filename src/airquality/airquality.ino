#include <Wire.h>
#include "Adafruit_SGP30.h"

Adafruit_SGP30 sgp;

void setup() {
  Serial.begin(9600);
  Serial.println("SGP30 test");

  while (! sgp.begin()){
    Serial.println("#Sensor not found :(");  
  }
}

int counter = 0;
void loop() {
  if (! sgp.IAQmeasure()) {
    Serial.println("#Measurement failed");
    return;
  }
  if (! sgp.IAQmeasureRaw()) {
    Serial.println("#Raw Measurement failed");
    return;
  }
  Serial.print(String(sgp.TVOC) + " ");
  Serial.print(String(sgp.eCO2) + " "); 
  Serial.print(String(sgp.rawH2) + " "); 
  Serial.println(String(sgp.rawEthanol)); 

//take measurements every 1 seconds
  delay(1000);

  counter++;
  if (counter == 30) {
    counter = 0;

    uint16_t TVOC_base, eCO2_base;
    if (! sgp.getIAQBaseline(&eCO2_base, &TVOC_base)) {
      Serial.println("#Failed to get baseline readings");
      return;
    }
  }
}
