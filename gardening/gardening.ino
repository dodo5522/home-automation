/*
 Example code for my gardening.
 Editor     : Takashi Ando
 Version    : 1.0

 Hardware Connections (Breakoutboard to Arduino Pro Mini):
 -VCC = 3.3V
 -GND = GND
 -SDA = A4
 -SCL = A5
*/
#include <Wire.h>
#include <TSL2561.h>
#include <HTU21D.h>
#include <MOISTURE_SEN0114.h>
#include <XBee.h>
#include "gardening.h"

/****************************
 * Macro definition
 ****************************/
#ifdef DEBUG_GARDENING
#include <SoftwareSerial.h>
#define DEBUG_PRINT(...) debug_serial->print(__VA_ARGS__)
#else
#define DEBUG_PRINT(...)
#endif

/****************************
 * Global variables
 ****************************/
#ifdef DEBUG_GARDENING
static SoftwareSerial *debug_serial= NULL;
#endif

static XBee myXBee = XBee();
static XBeeAddress64 addrContributor = XBeeAddress64(XBEE_ADDRESS_H_COORDINATOR, XBEE_ADDRESS_L_COORDINATOR);

static MOISTURE_SEN0114 *myMoisture = NULL;
static HTU21D *myHumidity = NULL;
static TSL2561 *myLight = NULL;

static unsigned int lightIntegrationTime = 0;
static unsigned int mainLoopInterval = MAIN_INTERVAL_MSEC;

/****************************
 * internal functions
 ****************************/
void flashLed(int times, int wait)
{
    static const int errorLed = 13;

    for (int i = 0; i < times; i++)
    {
        digitalWrite(errorLed, HIGH);
        delay(wait);
        digitalWrite(errorLed, LOW);

        if (i + 1 < times)
            delay(wait);
    }
}

void indicateStatsOnLed(XBee &myXBee)
{
    // if there is no problem on conmunication, LED is not lighten.
    ZBTxStatusResponse txStatus = ZBTxStatusResponse();

    // after sending a tx request, we expect a status response
    // wait up to half second for the status response
    if (myXBee.readPacket(500))
    {
        // should be a znet tx status
        if (myXBee.getResponse().getApiId() != ZB_TX_STATUS_RESPONSE)
        {
            flashLed(5, 500);
            return;
        }

        myXBee.getResponse().getZBTxStatusResponse(txStatus);

        // get the delivery status, the fifth byte
        if (txStatus.getDeliveryStatus() != SUCCESS)
            flashLed(4, 500);
    }
    else if (myXBee.getResponse().isError())
        flashLed(3, 500);
    else
        flashLed(2, 50);
}

/****************************
 * main routine
 ****************************/
void setup()
{
#ifdef DEBUG_GARDENING
    debug_serial = new SoftwareSerial(DEBUG_SERIAL_RX_PIN, DEBUG_SERIAL_TX_PIN);
    debug_serial->begin(DEBUG_SERIAL_BAURATE);
#endif

    Serial.begin(XBEE_SERIAL_BAURATE);
    myXBee.setSerial(Serial);

    myMoisture = new MOISTURE_SEN0114(MOIST1_MAX, MOIST1_READ_PIN);
    myHumidity = new HTU21D();
    myHumidity->begin();
    myLight = new TSL2561();
    myLight->begin();

    // setTiming() will set the third parameter (ms) to the
    // requested integration time in ms (this will be useful later):
    // The sensor will now gather light during the integration time.
    // After the specified time, you can retrieve the result from the sensor.
    myLight->setTiming(LIGHT_GAIN, LIGHT_INTEGRATION_TIME_INDEX , lightIntegrationTime);
    myLight->setPowerUp();

    if(mainLoopInterval < lightIntegrationTime)
        mainLoopInterval = lightIntegrationTime;
}

void loop()
{
    long nowTemp = 0;
    long nowMoist = 0;
    long nowHumid = 0;
    unsigned int lightData0 = 0;
    unsigned int lightData1 = 0;
    double nowLuxDouble = 0.0;
    long nowLux = 0;

    delay(mainLoopInterval);

    if (myLight->getData(lightData0, lightData1))
    {
        // Perform lux calculation:
        myLight->getLux(LIGHT_GAIN, lightIntegrationTime, lightData0, lightData1, nowLuxDouble);
        nowLux = (long)(10 * nowLuxDouble);
    }

    nowTemp  = (long)(10 * myHumidity->readTemperature());
    nowMoist = (long)(10 * myMoisture->getMoisturePercent());
    nowHumid = (long)(10 * myHumidity->readHumidity());

    SENSOR_DATA sensorData[] =
    {
        {{'L', 'U', 'X', '\0'}, nowLux  },
        {{'M', 'O', 'I', '\0'}, nowMoist},
        {{'H', 'U', 'M', '\0'}, nowHumid},
        {{'T', 'M', 'P', '\0'}, nowTemp },
    };

    for(unsigned int i = 0; i < sizeof(sensorData)/sizeof(SENSOR_DATA); i++)
    {
        ZBTxRequest myTxRequest = ZBTxRequest(
                addrContributor,
                (uint8_t*)&sensorData[i],
                sizeof(SENSOR_DATA));

        myXBee.send(myTxRequest);

        // this function takes 500ms as max when timeout error.
        indicateStatsOnLed(myXBee);
    }

    DEBUG_PRINT("Luminosity:");  DEBUG_PRINT(nowLux/10);  DEBUG_PRINT("[lm]\n");
    DEBUG_PRINT("Moisture :");   DEBUG_PRINT(nowMoist/10);DEBUG_PRINT("[%]\n");
    DEBUG_PRINT("Humidity :");   DEBUG_PRINT(nowHumid/10);DEBUG_PRINT("[%]\n");
    DEBUG_PRINT("Temperature :");DEBUG_PRINT(nowTemp/10); DEBUG_PRINT("[C]\n");
}
