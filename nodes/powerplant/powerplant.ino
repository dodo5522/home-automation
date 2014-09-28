#include <Serial.h>
#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 obj_ina219;

void setup(void)
{
  Serial.begin(9600);

  pinMode(9, OUTPUT);
  digitalWrite(9, LOW);

  obj_ina219.begin();
}

void loop(void)
{
  static boolean led_on = false;
  digitalWrite(9, led_on ? HIGH : LOW);
  led_on = !led_on;

  Serial.print("bus v: "); Serial.println(obj_ina219.getBusVoltage_V());
  Serial.print("shu v: "); Serial.println(obj_ina219.getShuntVoltage_mV());
  Serial.print("cur mA: "); Serial.println(obj_ina219.getCurrent_mA());

  delay(3000);
}

