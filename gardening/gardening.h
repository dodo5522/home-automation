#ifndef _GARDENING_H_
#define _GARDENING_H_

/****************************
 * Macro definition
 ****************************/
#define DEBUG_GARDENING
#define DEBUG_SERIAL_RX_PIN (8)
#define DEBUG_SERIAL_TX_PIN (9)
#define DEBUG_SERIAL_BAURATE (9600)

// If the interval is less than integration time, setup() set the integration time as minimum.
#define MAIN_INTERVAL_MSEC (10000)

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
#define MOIST1_MAX (700)
#define MOIST1_READ_PIN (2)
#define MOIST2_MAX (MOIST1_MAX)
#define MOIST2_READ_PIN (3)

#define XBEE_SERIAL_BAURATE (9600)
#define XBEE_ADDRESS_H_COORDINATOR (0x0013A200)
#define XBEE_ADDRESS_L_COORDINATOR (0x40B4500A)

/****************************
 * Structures
 ****************************/
typedef struct _SENSOR_DATA
{
    unsigned char type[4]; // ex. MOI means moisture
    long value;            // value got from sensor *10 to indicate decimal part.
}SENSOR_DATA;

#endif

