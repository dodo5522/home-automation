#ifndef _POWER_PLANT_H_
#define _POWER_PLANT_H_

/****************************
 * Macro definition
 ****************************/
//#define ENABLE_DEBUG_SOFT_SERIAL
#define ENABLE_DEBUG

const int LED_SWITCH_PIN = 2;

// If the interval is less than integration time, setup() set the integration time as minimum.
#if (defined(ENABLE_DEBUG) || defined(ENABLE_DEBUG_SOFT_SERIAL))
#define MAIN_INTERVAL_MSEC (10000)
#else
#define MAIN_INTERVAL_MSEC (300000)
#endif

#define XBEE_SERIAL_BAURATE (9600)
#define XBEE_ADDRESS_H_COORDINATOR (0x0013A200)
#define XBEE_ADDRESS_L_COORDINATOR (0x40AFBCCE)

/****************************
 * Structures
 ****************************/
typedef enum _SENSOR_ARRAY_NUM
{
    E_SENSOR_CURRENT_VOLTAGE0 = 0,
    E_SENSOR_CURRENT_VOLTAGE1,
    E_SENSOR_CURRENT,
    E_SENSOR_MAX,
}SENSOR_ARRAY_NUM;

#endif

