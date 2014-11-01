/*
 Example code for my solar plant monitor.
 Editor     : Takashi Ando
 Version    : 1.0
*/
#include <Wire.h>
#include <INA226.h>
#include <Adafruit_INA219.h>
#include <XBee.h>
#include <datatype.h>
#include "powerplant.h"

#if defined(ENABLE_DEBUG_SOFT_SERIAL)
#include <SoftwareSerial.h>
#endif
#include <debug.h>

/****************************
 * Macro definition
 ****************************/
//#define INA226_ADDRESS              (0x40)
#define INA226_11_ADDRESS           (0x45)
#define INA226_DD_ADDRESS           (0x4a)
#define INA226_CC_ADDRESS           (0x4f)

//#define INA219_ADDRESS              (0x40)
#define INA219_A0_ADDRESS           (0x41)
#define INA219_A1_ADDRESS           (0x44)
#define INA219_A0A1_ADDRESS         (0x45)

static XBee myXBee = XBee();
static XBeeAddress64 addrContributor = XBeeAddress64(XBEE_ADDRESS_H_COORDINATOR, XBEE_ADDRESS_L_COORDINATOR);

static INA226 g_ina_solar;
static INA226 g_ina_battery;
static Adafruit_INA219 g_ina_converter(INA219_A0A1_ADDRESS);

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

void checkConfig(INA226 ina)
{
    DEBUG_PRINT("Mode:                  ");
    switch (ina.getMode())
    {
        case INA226_MODE_POWER_DOWN:      DEBUG_PRINT("Power-Down\n"); break;
        case INA226_MODE_SHUNT_TRIG:      DEBUG_PRINT("Shunt Voltage, Triggered\n"); break;
        case INA226_MODE_BUS_TRIG:        DEBUG_PRINT("Bus Voltage, Triggered\n"); break;
        case INA226_MODE_SHUNT_BUS_TRIG:  DEBUG_PRINT("Shunt and Bus, Triggered\n"); break;
        case INA226_MODE_ADC_OFF:         DEBUG_PRINT("ADC Off\n"); break;
        case INA226_MODE_SHUNT_CONT:      DEBUG_PRINT("Shunt Voltage, Continuous\n"); break;
        case INA226_MODE_BUS_CONT:        DEBUG_PRINT("Bus Voltage, Continuous\n"); break;
        case INA226_MODE_SHUNT_BUS_CONT:  DEBUG_PRINT("Shunt and Bus, Continuous\n"); break;
        default: DEBUG_PRINT("unknown\n");
    }

    DEBUG_PRINT("Samples average:       ");
    switch (ina.getAverages())
    {
        case INA226_AVERAGES_1:           DEBUG_PRINT("1 sample\n"); break;
        case INA226_AVERAGES_4:           DEBUG_PRINT("4 samples\n"); break;
        case INA226_AVERAGES_16:          DEBUG_PRINT("16 samples\n"); break;
        case INA226_AVERAGES_64:          DEBUG_PRINT("64 samples\n"); break;
        case INA226_AVERAGES_128:         DEBUG_PRINT("128 samples\n"); break;
        case INA226_AVERAGES_256:         DEBUG_PRINT("256 samples\n"); break;
        case INA226_AVERAGES_512:         DEBUG_PRINT("512 samples\n"); break;
        case INA226_AVERAGES_1024:        DEBUG_PRINT("1024 samples\n"); break;
        default: DEBUG_PRINT("unknown\n");
    }

    DEBUG_PRINT("Bus conversion time:   ");
    switch (ina.getBusConversionTime())
    {
        case INA226_BUS_CONV_TIME_140US:  DEBUG_PRINT("140uS\n"); break;
        case INA226_BUS_CONV_TIME_204US:  DEBUG_PRINT("204uS\n"); break;
        case INA226_BUS_CONV_TIME_332US:  DEBUG_PRINT("332uS\n"); break;
        case INA226_BUS_CONV_TIME_588US:  DEBUG_PRINT("558uS\n"); break;
        case INA226_BUS_CONV_TIME_1100US: DEBUG_PRINT("1.100ms\n"); break;
        case INA226_BUS_CONV_TIME_2116US: DEBUG_PRINT("2.116ms\n"); break;
        case INA226_BUS_CONV_TIME_4156US: DEBUG_PRINT("4.156ms\n"); break;
        case INA226_BUS_CONV_TIME_8244US: DEBUG_PRINT("8.244ms\n"); break;
        default: DEBUG_PRINT("unknown\n");
    }

    DEBUG_PRINT("Shunt conversion time: ");
    switch (ina.getShuntConversionTime())
    {
        case INA226_SHUNT_CONV_TIME_140US:  DEBUG_PRINT("140uS\n"); break;
        case INA226_SHUNT_CONV_TIME_204US:  DEBUG_PRINT("204uS\n"); break;
        case INA226_SHUNT_CONV_TIME_332US:  DEBUG_PRINT("332uS\n"); break;
        case INA226_SHUNT_CONV_TIME_588US:  DEBUG_PRINT("558uS\n"); break;
        case INA226_SHUNT_CONV_TIME_1100US: DEBUG_PRINT("1.100ms\n"); break;
        case INA226_SHUNT_CONV_TIME_2116US: DEBUG_PRINT("2.116ms\n"); break;
        case INA226_SHUNT_CONV_TIME_4156US: DEBUG_PRINT("4.156ms\n"); break;
        case INA226_SHUNT_CONV_TIME_8244US: DEBUG_PRINT("8.244ms\n"); break;
        default: DEBUG_PRINT("unknown\n");
    }

    DEBUG_PRINT("Max possible current:  ");
    DEBUG_PRINT(ina.getMaxPossibleCurrent());
    DEBUG_PRINT(" A\n");

    DEBUG_PRINT("Max current:           ");
    DEBUG_PRINT(ina.getMaxCurrent());
    DEBUG_PRINT(" A\n");

    DEBUG_PRINT("Max shunt voltage:     ");
    DEBUG_PRINT(ina.getMaxShuntVoltage());
    DEBUG_PRINT(" V\n");

    DEBUG_PRINT("Max power:             ");
    DEBUG_PRINT(ina.getMaxPower());
    DEBUG_PRINT(" W\n");
}

void setup(void)
{
    setup_debug();

#if !defined(ENABLE_DEBUG)
    Serial.begin(XBEE_SERIAL_BAURATE);
    myXBee.setSerial(Serial);
#endif

    //FIXME: LED power on/off switch control.
    pinMode(LED_SWITCH_PIN, OUTPUT);
    digitalWrite(LED_SWITCH_PIN, LOW);

    g_ina_converter.begin();
    g_ina_battery.begin(INA226_CC_ADDRESS);
    g_ina_solar.begin(INA226_DD_ADDRESS);

    // Configure INA226
    g_ina_battery.configure(
            INA226_AVERAGES_1,
            INA226_BUS_CONV_TIME_1100US,
            INA226_SHUNT_CONV_TIME_1100US,
            INA226_MODE_SHUNT_BUS_CONT);
    // Calibrate INA226. Rshunt = 0.002 ohm, Max excepted current = 12A
    g_ina_battery.calibrate(0.002, 14);

    // Configure INA226
    g_ina_solar.configure(
            INA226_AVERAGES_1,
            INA226_BUS_CONV_TIME_1100US,
            INA226_SHUNT_CONV_TIME_1100US,
            INA226_MODE_SHUNT_BUS_CONT);
    // Calibrate INA226. Rshunt = 0.002 ohm, Max excepted current = 1.11A
    g_ina_solar.calibrate(0.002, 4);

#if (defined(ENABLE_DEBUG) || defined(ENABLE_DEBUG_SOFT_SERIAL))
    delay(5000);

    // Show configuration
    checkConfig(g_ina_battery);
    checkConfig(g_ina_solar);
#endif
}

void loop(void)
{
    //FIXME: LED power on/off switch control.
    static boolean led_on = false;
    digitalWrite(LED_SWITCH_PIN, led_on ? HIGH : LOW);
    led_on = !led_on;

    if (isTriggerToPost() != true)
        return;

    DEBUG_PRINT("battery:");
    DEBUG_PRINT(" shu A: "); DEBUG_PRINT(g_ina_battery.readShuntCurrent()); DEBUG_PRINT("\n");
    DEBUG_PRINT(" shu V: "); DEBUG_PRINT(g_ina_battery.readShuntVoltage()); DEBUG_PRINT("\n");
    DEBUG_PRINT(" bus P: "); DEBUG_PRINT(g_ina_battery.readBusPower());     DEBUG_PRINT("\n");
    DEBUG_PRINT(" bus V: "); DEBUG_PRINT(g_ina_battery.readBusVoltage());   DEBUG_PRINT("\n");

    DEBUG_PRINT("solar:\n");
    DEBUG_PRINT(" shu A: "); DEBUG_PRINT(g_ina_solar.readShuntCurrent()); DEBUG_PRINT("\n");
    DEBUG_PRINT(" shu V: "); DEBUG_PRINT(g_ina_solar.readShuntVoltage()); DEBUG_PRINT("\n");
    DEBUG_PRINT(" bus P: "); DEBUG_PRINT(g_ina_solar.readBusPower());     DEBUG_PRINT("\n");
    DEBUG_PRINT(" bus V: "); DEBUG_PRINT(g_ina_solar.readBusVoltage());   DEBUG_PRINT("\n");

    DEBUG_PRINT("charge converter:\n");
    DEBUG_PRINT(" bus V: "); DEBUG_PRINT(g_ina_converter.getBusVoltage_V());    DEBUG_PRINT("\n");
    DEBUG_PRINT(" shu V: "); DEBUG_PRINT(g_ina_converter.getShuntVoltage_mV()); DEBUG_PRINT("\n");
    DEBUG_PRINT(" cur mA: ");DEBUG_PRINT(g_ina_converter.getCurrent_mA());      DEBUG_PRINT("\n");
}

