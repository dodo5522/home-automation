#ifndef _DATA_TYPE_H_
#define _DATA_TYPE_H_

typedef struct _SENSOR_DATA
{
    uint8_t type[3]; // ex. "MOI" means moisture
    uint8_t number;  // number character like '0'/'1'/... of the same type's multiple sensor
    int32_t value;   // value got from sensor x multiple to indicate decimal part.
    int32_t multiple;// multiple number against value.
}SENSOR_DATA;

#endif

