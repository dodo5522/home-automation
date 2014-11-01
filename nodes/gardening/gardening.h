#ifndef _GARDENING_H_
#define _GARDENING_H_

/****************************
 * Macro definition
 ****************************/
//#define ENABLE_DEBUG_SOFT_SERIAL
//#define ENABLE_DEBUG

// If the interval is less than integration time, setup() set the integration time as minimum.
#if (defined(ENABLE_DEBUG) || defined(ENABLE_DEBUG_SOFT_SERIAL))
#define MAIN_INTERVAL_MSEC (10000)
#else
#define MAIN_INTERVAL_MSEC (300000)
#endif

// If gain = false (0), device is set to low gain (1X)
// If gain = high (1), device is set to high gain (16X)
#define LIGHT_GAIN (false)
// If time = 0, integration will be 13.7ms
// If time = 1, integration will be 101ms
// If time = 2, integration will be 402ms
// If time = 3, use manual start / stop to perform your own integration
#define LIGHT_INTEGRATION_TIME_INDEX (2)

// 0  ~300 : dry soil
// 300~700 : humid soil
// 700~950 : in water
#define MOIST0_READ_PIN (0)
#define MOIST1_READ_PIN (1)

#define XBEE_SERIAL_BAURATE (9600)
#define XBEE_ADDRESS_H_COORDINATOR (0x0013A200)
#define XBEE_ADDRESS_L_COORDINATOR (0x40B4500A)

/****************************
 * Structures
 ****************************/
typedef enum _SENSOR_ARRAY_NUM
{
    E_SENSOR_LUMINOSITY = 0,
    E_SENSOR_MOISTURE0,
    E_SENSOR_MOISTURE1,
    E_SENSOR_HUMIDITY,
    E_SENSOR_TEMPERATURE,
    E_SENSOR_MAX,
}SENSOR_ARRAY_NUM;

#endif

