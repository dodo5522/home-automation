#ifndef _DATA_TYPE_H_
#define _DATA_TYPE_H_

typedef struct _SENSOR_DATA
{
    uint8_t type[3]; // ex. MOI means moisture
    uint8_t number;  // number of the same type's multiple sensor
    int32_t value;   // value got from sensor *10 to indicate decimal part.
}SENSOR_DATA;

#endif

