/*
 * Moisture sensor library.
 * License: This code is public domain.
 */
#include "Arduino.h"

class MOISTURE_SEN0114
{
    public:
        /*
         * Analog read value max threshold is 550 as default.
         * Analog read value min threshold is 50 as default.
         * Analog read pin is 7 as default.
         */
        MOISTURE_SEN0114(unsigned char pin = 7, unsigned int max = 550, unsigned int min = 50);
        virtual ~MOISTURE_SEN0114(void);

        /*
         * Return value from 0 to 100 with unit %.
         * 100% means in the water, and 0% means dry soil.
         */
        unsigned char getMoisturePercent();

        /*
         * Return value from 0.0 to 1.0.
         * 1.0 means in the water, and 0.0 means dry soil.
         */
        float getMoistureRatio();

        /*
         * Return the raw value read from sensor.
         * 0  ~300     dry soil
         * 300~700     humid soil
         * 700~950     in water
         */
        unsigned int getMoistureRaw();

    private:
        unsigned int max_moisture;
        unsigned int min_moisture;
        unsigned char pin_analog;
};

