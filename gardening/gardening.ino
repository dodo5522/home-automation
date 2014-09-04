/*
 Example code for my gardening.
 Editor     : Takashi Ando
 Version    : 1.0

 Hardware Connections (Breakoutboard to Arduino):
 -VCC = 3.3V
 -GND = GND
 -SDA = A4 (use inline 10k resistor if your board is 5V)
 -SCL = A5 (use inline 10k resistor if your board is 5V)
 -Moisture line = A7
*/
#define XBEE_MODE_API

#include <Wire.h>
#include <TSL2561.h>
#include <HTU21D.h>
#include <MOISTURE_SEN0114.h>
#ifdef XBEE_MODE_API
#include <XBee.h>
#endif

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
            flashLed(4, 500);
            return;
        }

        myXBee.getResponse().getZBTxStatusResponse(txStatus);

        // get the delivery status, the fifth byte
        if (txStatus.getDeliveryStatus() != SUCCESS)
        {
            // the remote XBee did not receive our packet. is it powered on?
            flashLed(4, 500);
        }
    }
    else if (myXBee.getResponse().isError())
    {
        //nss.print("Error reading packet.  Error code: ");
        //nss.println(myXBee.getResponse().getErrorCode());
        flashLed(3, 500);
    }
    else
    {
        // local XBee did not provide a timely TX Status Response -- should not happen
        flashLed(2, 50);
    }
}

/****************************
 * main routine
 ****************************/
#ifdef XBEE_MODE_API
static XBee myXBee = XBee();
static XBeeAddress64 addrContributor = XBeeAddress64(0x0013A200, 0x40B4500A);
#endif
static MOISTURE_SEN0114 *myMoisture = NULL;
static HTU21D *myHumidity = NULL;
static TSL2561 *myLight = NULL;

// If gain = false (0), device is set to low gain (1X)
// If gain = high (1), device is set to high gain (16X)
static boolean lightGain = false;
// If time = 0, integration will be 13.7ms
// If time = 1, integration will be 101ms
// If time = 2, integration will be 402ms
// If time = 3, use manual start / stop to perform your own integration
static unsigned char lightIntegrationTimeIndex = 2;
// Integration ("shutter") time in milliseconds
static unsigned int lightIntegrationTime = 0;

// If the interval is lower than integration time, setup() set the integration time as minimum.
static unsigned int mainLoopInterval = 1000;

void setup()
{
    Serial.begin(9600);

    myMoisture = new MOISTURE_SEN0114(700, 7);
    myHumidity = new HTU21D();
    myHumidity->begin();
    myLight = new TSL2561();
    myLight->begin();

    // setTiming() will set the third parameter (ms) to the
    // requested integration time in ms (this will be useful later):
    myLight->setTiming(lightGain, lightIntegrationTimeIndex, lightIntegrationTime);
    // To start taking measurements, power up the sensor:
    myLight->setPowerUp();
    // The sensor will now gather light during the integration time.
    // After the specified time, you can retrieve the result from the sensor.
    // Once a measurement occurs, another integration period will start.

    if(mainLoopInterval < lightIntegrationTime)
        mainLoopInterval = lightIntegrationTime;

#ifdef XBEE_MODE_API
    myXBee.setSerial(Serial);
#endif
}

typedef struct _SENSOR_DATA
{
    unsigned char type[3];  // MOI means moisture
    unsigned char sign;     // 0:plus, 1:minus
    unsigned char value[4]; // value got from sensor *10 to indicate decimal part.
}SENSOR_DATA;

void loop()
{
    long nowTemp  = (long)(10 * myHumidity->readTemperature());
    unsigned long nowTempNoSign = (unsigned long)abs(nowTemp);
    unsigned long nowMoist = (unsigned long)(10 * myMoisture->getMoisturePercent());
    unsigned long nowHumid = (unsigned long)(10 * myHumidity->readHumidity());

    unsigned int lightData0, lightData1;
    double lux;    // Resulting lux value
    boolean boolSuccess = false;

    delay(mainLoopInterval);

    if (myLight->getData(lightData0, lightData1))
    {
        // Perform lux calculation:
        boolSuccess = myLight->getLux(lightGain, lightIntegrationTime, lightData0, lightData1, lux);
    }

#ifdef XBEE_MODE_API
    SENSOR_DATA sensorData[] =
    {
        {
            {'M', 'O', 'I'},
            0,
            {
                (nowMoist & 0x000000ff),
                (nowMoist & 0x0000ff00) >> 8,
                (nowMoist & 0x00ff0000) >> 16,
                (nowMoist & 0xff000000) >> 24
            }
        },
        {
            {'H', 'U', 'M'},
            0,
            {
                (nowHumid & 0x000000ff),
                (nowHumid & 0x0000ff00) >> 8,
                (nowHumid & 0x00ff0000) >> 16,
                (nowHumid & 0xff000000) >> 24
            }
        },
        {
            {'T', 'M', 'P'},
            nowTemp < 0 ? 1 : 0,
            {
                (nowTempNoSign & 0x000000ff),
                (nowTempNoSign & 0x0000ff00) >> 8,
                (nowTempNoSign & 0x00ff0000) >> 16,
                (nowTempNoSign & 0xff000000) >> 24
            }
        }
    };

    for(int i = 0; i < sizeof(sensorData)/sizeof(SENSOR_DATA); i++)
    {
        ZBTxRequest myTxRequest = ZBTxRequest(
                addrContributor,
                (uint8_t*)&sensorData[i],
                sizeof(SENSOR_DATA));

        myXBee.send(myTxRequest);

        // this function takes 500ms as max when timeout error.
        indicateStatsOnLed(myXBee);
    }
#else
    Serial.print("Moisture :");Serial.print(moist);Serial.println("[%]");
    Serial.print("Humidity :");Serial.print(humd);Serial.println("[%]");
    Serial.print("Temperature :");Serial.print(temp);Serial.println("[C]");
#endif
}
