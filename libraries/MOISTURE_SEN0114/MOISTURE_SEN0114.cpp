/*
 * Moisture sensor library.
 * License: This code is public domain.
 */
#include "MOISTURE_SEN0114.h"

MOISTURE_SEN0114::MOISTURE_SEN0114(void)
{
    max_moisture = 700;
    pin_analog = 7;
}

MOISTURE_SEN0114::MOISTURE_SEN0114(unsigned int max, unsigned char pin)
{
    max_moisture = max;
    pin_analog = pin;
}

MOISTURE_SEN0114::~MOISTURE_SEN0114(void)
{
}

/*
 * Return value from 0 to 100 with unit %.
 * 100% means in the water, and 0% means dry soil.
 */
unsigned char MOISTURE_SEN0114::getMoisturePercent()
{
    return (unsigned char)(getMoistureRatio() * 100);
}

/*
 * Return value from 0.0 to 1.0.
 * 1.0 means in the water, and 0.0 means dry soil.
 */
float MOISTURE_SEN0114::getMoistureRatio()
{
    unsigned int raw_value = getMoistureRaw();
    float ratio = 0.0;

    if(raw_value > max_moisture)
        raw_value = max_moisture;

    ratio = (float)raw_value / (float)max_moisture;
    return ratio;
}

/*
 * Return the raw value read from sensor.
 * 0  ~300     dry soil
 * 300~700     humid soil
 * 700~950     in water
 */
unsigned int MOISTURE_SEN0114::getMoistureRaw()
{
    return analogRead(pin_analog);
}
