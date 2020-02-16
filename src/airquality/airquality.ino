#include <Wire.h>
#include "Adafruit_SGP30.h"

Adafruit_SGP30 sgp;

long avgTvoc = 0;
long avgECo2 = 0;
long avgRawH2 = 0;
long avgRawEthanol = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("#SGP30 test");

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
  
  //take cumulative measurements every second
  avgTvoc += sgp.TVOC;
  avgECo2 += sgp.eCO2;
  avgRawH2 += sgp.rawH2;
  avgRawEthanol += sgp.rawEthanol; 
  delay(1000);

  counter++;
  if (counter == 30) {
    counter = 0;

    //log average measurement every 30s 
    Serial.print(String((float) avgTvoc / (float) 30) + " "); 
    Serial.print(String((float) avgECo2 / (float) 30) + " "); 
    Serial.print(String((float) avgRawH2 / (float) 30) + " "); 
    Serial.println(String((float) avgRawEthanol / (float) 30)); 

    avgTvoc = 0;
    avgECo2 = 0;
    avgRawH2 = 0;
    avgRawEthanol = 0;

    uint16_t TVOC_base, eCO2_base;
    if (! sgp.getIAQBaseline(&eCO2_base, &TVOC_base)) {
      Serial.println("#Failed to get baseline readings");
      return;
    }
  }
}
