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

void setup()
{
    Serial.begin(9600);

    myMoisture = new MOISTURE_SEN0114(700, 7);
    myHumidity = new HTU21D();
    myHumidity->begin();

#ifdef XBEE_MODE_API
    myXBee.setSerial(Serial);
#endif
}

void loop()
{
    unsigned char nowMoisture = myMoisture->getMoisturePercent();
    unsigned char nowHumidity = (unsigned char)myHumidity->readHumidity();
    char nowTemperature = (char)myHumidity->readTemperature();

#ifdef XBEE_MODE_API
    unsigned char sensorData[][5] =
    {
        /* signed prefix         value */
        {  0,     'M', 'O', 'I', nowMoisture},
        {  0,     'H', 'U', 'M', nowHumidity},
        {  1,     'T', 'M', 'P', (unsigned char)nowTemperature},
    };

    for(int i = 0; i < sizeof(sensorData)/sizeof(sensorData[0]); i++)
    {
        ZBTxRequest myTxRequest = ZBTxRequest(
                addrContributor,
                (uint8_t*)sensorData[i],
                sizeof(sensorData[i]));

        myXBee.send(myTxRequest);

        // this function takes 500ms as max when timeout error.
        indicateStatsOnLed(myXBee);
    }
#else
    Serial.print("Moisture :");Serial.print(moist);Serial.println("[%]");
    Serial.print("Humidity :");Serial.print(humd);Serial.println("[%]");
    Serial.print("Temperature :");Serial.print(temp);Serial.println("[C]");
#endif

    delay(1000);
}
