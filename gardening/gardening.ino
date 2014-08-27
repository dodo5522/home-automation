/*
 Example code for my gardening.
 Editor     : Takashi Ando
 Version    : 1.0

 Hardware Connections (Breakoutboard to Arduino):
 -VCC = 3.3V
 -GND = GND
 -SDA = A4 (use inline 10k resistor if your board is 5V)
 -SCL = A5 (use inline 10k resistor if your board is 5V)
 -Moisture line = A7
*/

#include <Wire.h>
#include <HTU21D.h>
#include <MOISTURE_SEN0114.h>

MOISTURE_SEN0114 myMoisture = MOISTURE_SEN0114(700, 7);
HTU21D myHumidity;

void setup()
{
  Serial.begin(9600);
  myHumidity.begin();
}

void loop()
{
  float humd = myHumidity.readHumidity();
  float temp = myHumidity.readTemperature();
  unsigned char moist = myMoisture.getMoisturePercent();

  Serial.print("Moisture :");Serial.print(moist);Serial.println("[%]");
  Serial.print("Humidity :");Serial.print(humd);Serial.println("[%]");
  Serial.print("Temperature :");Serial.print(temp);Serial.println("[C]");
  delay(1000);
}
