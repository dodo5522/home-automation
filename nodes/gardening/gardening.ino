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
#include <datatype.h>
#include "gardening.h"

#if defined(ENABLE_DEBUG_SOFT_SERIAL)
#include <SoftwareSerial.h>
#endif
#include <debug.h>

/****************************
 * Macro definition
 ****************************/

/****************************
 * Global variables
 ****************************/

static XBee myXBee = XBee();
static XBeeAddress64 addrContributor = XBeeAddress64(XBEE_ADDRESS_H_COORDINATOR, XBEE_ADDRESS_L_COORDINATOR);

static MOISTURE_SEN0114 myMoisture0 = MOISTURE_SEN0114(MOIST0_READ_PIN);
static MOISTURE_SEN0114 myMoisture1 = MOISTURE_SEN0114(MOIST1_READ_PIN);
static HTU21D myHumidity = HTU21D();
static TSL2561 myLight = TSL2561();

static unsigned int lightIntegrationTime = 0;
static unsigned long mainLoopInterval = MAIN_INTERVAL_MSEC;

/****************************
 * internal functions
 ****************************/
boolean isTriggerToPost(void)
{
    static unsigned long previous_tick_count = millis();
    unsigned long current_tick_count = millis();

    if(current_tick_count < previous_tick_count)
    {
        previous_tick_count = current_tick_count;
        return false;
    }
    else if(current_tick_count - previous_tick_count < mainLoopInterval)
    {
        return false;
    }

    previous_tick_count = current_tick_count;
    return true;
}

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

void indicateStatusXBee(XBee &myXBee)
{
    uint8_t api_id = 0;
    uint8_t delivery_status = 0;
    bool error = false;

    // if there is no problem on conmunication, LED is not lighten.
    ZBTxStatusResponse txStatus = ZBTxStatusResponse();

    // after sending a tx request, we expect a status response
    // wait up to half second for the status response
    if (myXBee.readPacket(500))
    {
        // should be a znet tx status
        api_id = myXBee.getResponse().getApiId();
        if (api_id != ZB_TX_STATUS_RESPONSE)
        {
            DEBUG_PRINT("Error: API ID is ");DEBUG_PRINT(api_id);DEBUG_PRINT("\n");
            flashLed(5, 500);
            return;
        }

        myXBee.getResponse().getZBTxStatusResponse(txStatus);

        // get the delivery status, the fifth byte
        delivery_status = txStatus.getDeliveryStatus();
        if (delivery_status != SUCCESS)
        {
            DEBUG_PRINT("Error: Delivery status is ");DEBUG_PRINT(delivery_status);DEBUG_PRINT("\n");
            flashLed(4, 500);
        }
    }
    else
    {
        error = myXBee.getResponse().isError();
        if (error)
        {
            DEBUG_PRINT("Error: Response error.");DEBUG_PRINT("\n");
            flashLed(3, 500);
        }
        else
        {
            DEBUG_PRINT("Error: Another.");DEBUG_PRINT("\n");
            flashLed(2, 50);
        }
    }
}

/****************************
 * main routine
 ****************************/
void setup()
{
    setup_debug();

#if !defined(ENABLE_DEBUG_HARD_SERIAL)
    Serial.begin(XBEE_SERIAL_BAURATE);
    myXBee.setSerial(Serial);
#endif

    myHumidity.begin();
    myLight.begin();

    // setTiming() will set the third parameter (ms) to the
    // requested integration time in ms (this will be useful later):
    // The sensor will now gather light during the integration time.
    // After the specified time, you can retrieve the result from the sensor.
    myLight.setTiming(LIGHT_GAIN, LIGHT_INTEGRATION_TIME_INDEX , lightIntegrationTime);
    myLight.setPowerUp();

    if(mainLoopInterval < lightIntegrationTime)
        mainLoopInterval = lightIntegrationTime;
}

void loop()
{
    unsigned int lightData0 = 0;
    unsigned int lightData1 = 0;
    double nowLuxDouble = 0.0;
    SENSOR_DATA sensorData[E_SENSOR_MAX] =
    {
        {{'L', 'U', 'X'}, '0', 10, 0},
        {{'M', 'O', 'I'}, '0', 10, 0}, // for small planter
        {{'M', 'O', 'I'}, '1', 10, 0}, // for large planter
        {{'H', 'U', 'M'}, '0', 10, 0},
        {{'T', 'M', 'P'}, '0', 10, 0},
    };

    if (isTriggerToPost() != true)
        return;

    if (myLight.getData(lightData0, lightData1))
    {
        // Perform lux calculation:
        myLight.getLux(LIGHT_GAIN, lightIntegrationTime, lightData0, lightData1, nowLuxDouble);
        sensorData[E_SENSOR_LUMINOSITY].value =
            (int32_t)(sensorData[E_SENSOR_LUMINOSITY].multiple * nowLuxDouble);
    }

    sensorData[E_SENSOR_TEMPERATURE].value =
        (int32_t)(sensorData[E_SENSOR_TEMPERATURE].multiple * myHumidity.readTemperature());
    sensorData[E_SENSOR_HUMIDITY].value =
        (int32_t)(sensorData[E_SENSOR_HUMIDITY].multiple * myHumidity.readHumidity());
    sensorData[E_SENSOR_MOISTURE0].value =
        (int32_t)(sensorData[E_SENSOR_MOISTURE0].multiple * myMoisture0.getMoisturePercent());
    sensorData[E_SENSOR_MOISTURE1].value =
        (int32_t)(sensorData[E_SENSOR_MOISTURE1].multiple * myMoisture1.getMoisturePercent());

    ZBTxRequest myTxRequest = ZBTxRequest(
            addrContributor,
            (uint8_t*)sensorData,
            sizeof(sensorData));

#if !defined(ENABLE_DEBUG)
    myXBee.send(myTxRequest);

    // this function takes 500ms as max when timeout error.
    indicateStatusXBee(myXBee);
#endif

    DEBUG_PRINT("Luminosity:");  DEBUG_PRINT(sensorData[E_SENSOR_LUMINOSITY].value /(float)sensorData[E_SENSOR_LUMINOSITY].multiple); DEBUG_PRINT("[lm]\n");
    DEBUG_PRINT("Moisture0 :");  DEBUG_PRINT(sensorData[E_SENSOR_MOISTURE0].value  /(float)sensorData[E_SENSOR_MOISTURE0].multiple);  DEBUG_PRINT("[%]\n");
    DEBUG_PRINT("Moisture1 :");  DEBUG_PRINT(sensorData[E_SENSOR_MOISTURE1].value  /(float)sensorData[E_SENSOR_MOISTURE1].multiple);  DEBUG_PRINT("[%]\n");
    DEBUG_PRINT("Humidity :");   DEBUG_PRINT(sensorData[E_SENSOR_HUMIDITY].value   /(float)sensorData[E_SENSOR_HUMIDITY].multiple);   DEBUG_PRINT("[%]\n");
    DEBUG_PRINT("Temperature :");DEBUG_PRINT(sensorData[E_SENSOR_TEMPERATURE].value/(float)sensorData[E_SENSOR_TEMPERATURE].multiple);DEBUG_PRINT("[C]\n");
}
