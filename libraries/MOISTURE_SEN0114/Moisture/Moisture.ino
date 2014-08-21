/*
  # Example code for the moisture sensor <http://www.dfrobot.com/wiki/index.php?title=Moisture_Sensor_%28SKU%3ASEN0114%29>
  # Editor     : Lauren
  # Date       : 13.01.2012
  # Version    : 1.0
  # Connect the sensor to the A0(Analog 0) pin on the Arduino board
   
  # the sensor value description
  # 0  ~300     dry soil
  # 300~700     humid soil
  # 700~950     in water
*/
#include <MOISTURE_SEN0114.h>

MOISTURE_SEN0114 obj;

void setup()
{
  Serial.begin(9600);
  obj = MOISTURE_SEN0114(700, 7);
}

void loop()
{
  Serial.print("Moisture Sensor Value:");Serial.print(obj.getMoisturePercent());Serial.println("[%]");
  Serial.print("Moisture Sensor Value:");Serial.print(obj.getMoistureRatio());Serial.println("[ratio]");
  Serial.print("Moisture Sensor Value:");Serial.print(obj.getMoistureRaw());Serial.println("[raw]");
  delay(1000);
}
