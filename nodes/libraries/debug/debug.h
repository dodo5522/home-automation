#ifndef _DEBUG_H_
#define _DEBUG_H_

/****************************
 * constant values definition
 ****************************/
const int DEBUG_SERIAL_RX_PIN = 8;
const int DEBUG_SERIAL_TX_PIN = 9;
const int DEBUG_SERIAL_BAURATE = 9600;

#if defined(ENABLE_DEBUG_SOFT_SERIAL)
SoftwareSerial SoftSerial = SoftwareSerial(DEBUG_SERIAL_RX_PIN, DEBUG_SERIAL_TX_PIN);
#endif

/****************************
 * functions
 ****************************/
inline void setup_debug(void)
{
#if defined(ENABLE_DEBUG_SOFT_SERIAL)
    SoftSerial.begin(DEBUG_SERIAL_BAURATE);
#elif defined(ENABLE_DEBUG_HARD_SERIAL)
    Serial.begin(DEBUG_SERIAL_BAURATE);
#endif
}

#if defined(ENABLE_DEBUG_SOFT_SERIAL)
#define DEBUG_PRINT(...)    SoftSerial.print(__VA_ARGS__);
#elif defined(ENABLE_DEBUG_HARD_SERIAL)
#define DEBUG_PRINT(...)    Serial.print(__VA_ARGS__);
#else
#define DEBUG_PRINT(...)
#endif

#endif

