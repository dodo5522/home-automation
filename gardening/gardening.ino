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

#include <stdio.h>
#include <Wire.h>
#include <HTU21D.h>
#include <MOISTURE_SEN0114.h>
#ifdef XBEE_MODE_API
#include <XBee.h>

XBee myXBee = XBee();
XBeeAddress64 addrContributor = XBeeAddress64(0x0013A200, 0x40B4500A);
#endif

MOISTURE_SEN0114 *myMoisture = NULL;
HTU21D *myHumidity = NULL;

int statusLed = 13;
int errorLed = 13;

void flashLed(int pin, int times, int wait)
{
    for (int i = 0; i < times; i++)
    {
        digitalWrite(pin, HIGH);
        delay(wait);
        digitalWrite(pin, LOW);

        if (i + 1 < times)
            delay(wait);
    }
}

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

class SensorValToStr
{
    public:
        SensorValToStr(char *title, double value)
        {
            snprintf(str, sizeof(str), "%s:%.1f", title, value);
        };
        SensorValToStr(char *title, int value)
        {
            snprintf(str, sizeof(str), "%s:%d", title, value);
        };
        virtual ~SensorValToStr(){};
        char* getStr(void)
        {
            return str;
        };
    private:
        char str[32];
};

void loop()
{
  SensorValToStr mySensorValues[] = {
      SensorValToStr("Humidity", (double)myHumidity->readHumidity()),
      SensorValToStr("Temperature", (double)myHumidity->readTemperature()),
      SensorValToStr("Moisture", (int)myMoisture->getMoisturePercent())
  };

#ifdef XBEE_MODE_API
    ZBTxStatusResponse txStatus = ZBTxStatusResponse();

    for(int i = 0; i < sizeof(mySensorValues)/sizeof(SensorValToStr); i++)
    {
        ZBTxRequest myTxRequest = ZBTxRequest(
                addrContributor,
                (uint8_t*)mySensorValues[i].getStr(),
                strlen(mySensorValues[i].getStr()));

        myXBee.send(myTxRequest);

        // after sending a tx request, we expect a status response
        // wait up to half second for the status response
        if (myXBee.readPacket(500))
        {
            // should be a znet tx status
            if (myXBee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE)
            {
                myXBee.getResponse().getZBTxStatusResponse(txStatus);

                // get the delivery status, the fifth byte
                if (txStatus.getDeliveryStatus() == SUCCESS)
                {
                    // success.  time to celebrate
                    //flashLed(statusLed, 5, 50);
                }
                else
                {
                    // the remote XBee did not receive our packet. is it powered on?
                    flashLed(errorLed, 4, 500);
                }
            }
        }
        else if (myXBee.getResponse().isError())
        {
            //nss.print("Error reading packet.  Error code: ");
            //nss.println(myXBee.getResponse().getErrorCode());
            flashLed(errorLed, 3, 500);
        }
        else
        {
            // local XBee did not provide a timely TX Status Response -- should not happen
            flashLed(errorLed, 2, 50);
        }
    }
#else
  Serial.print("Moisture :");Serial.print(moist);Serial.println("[%]");
  Serial.print("Humidity :");Serial.print(humd);Serial.println("[%]");
  Serial.print("Temperature :");Serial.print(temp);Serial.println("[C]");
#endif

  delay(1000);
}
