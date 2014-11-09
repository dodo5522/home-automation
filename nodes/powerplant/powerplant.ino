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
 * IElectricPower class implementation
 ****************************/
IElectricPower::IElectricPower(char *name)
{
    strncpy(name_, name, sizeof(name_) - 1);
}

void IElectricPower::showConfig(void)
{
    DEBUG_PRINT("Name:                  "); DEBUG_PRINT(name_); DEBUG_PRINT("\n");
    DEBUG_PRINT("Measure current        "); DEBUG_PRINT(hasAvilityCurrent()); DEBUG_PRINT("\n");
    DEBUG_PRINT("Measure voltage        "); DEBUG_PRINT(hasAvilityVoltage()); DEBUG_PRINT("\n");
}

/****************************
 * MyINA226 class implementation
 ****************************/
MyINA226::MyINA226(char *name,
        uint8_t slave_address,
        float rShuntValueOhm,
        float iMaxExceptedCurrent_A,
        ina226_averages_t averages,
        ina226_busConvTime_t busConvTime,
        ina226_shuntConvTime_t shuntConvTime,
        ina226_mode_t mode)
    :IElectricPower(name),
    ina_(),
    slave_address_(slave_address),
    averages_(averages),
    busConvTime_(busConvTime),
    mode_(mode),
    rShuntValueOhm_(rShuntValueOhm),
    iMaxExceptedCurrent_A_(iMaxExceptedCurrent_A)
{
}

void MyINA226::begin(void)
{
    ina_.begin(slave_address_);
    ina_.configure(averages_, busConvTime_, shuntConvTime_, mode_);
    ina_.calibrate(rShuntValueOhm_, iMaxExceptedCurrent_A_);
}

void MyINA226::showConfig(void)
{
    IElectricPower::showConfig();
    DEBUG_PRINT("Mode:                  ");
    switch (ina_.getMode())
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
    switch (ina_.getAverages())
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
    switch (ina_.getBusConversionTime())
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
    switch (ina_.getShuntConversionTime())
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

    DEBUG_PRINT("Max possible current:  "); DEBUG_PRINT(ina_.getMaxPossibleCurrent()); DEBUG_PRINT(" A\n");
    DEBUG_PRINT("Max current:           "); DEBUG_PRINT(ina_.getMaxCurrent());         DEBUG_PRINT(" A\n");
    DEBUG_PRINT("Max shunt voltage:     "); DEBUG_PRINT(ina_.getMaxShuntVoltage());    DEBUG_PRINT(" V\n");
    DEBUG_PRINT("Max power:             "); DEBUG_PRINT(ina_.getMaxPower());           DEBUG_PRINT(" W\n");
}

void MyINA226::showStatus(void)
{
    DEBUG_PRINT(name_);DEBUG_PRINT("\n");
    DEBUG_PRINT(" bus V: "); DEBUG_PRINT(getBusVoltage_V());   DEBUG_PRINT("\n");
    DEBUG_PRINT(" shu V: "); DEBUG_PRINT(getShuntVoltage_V()); DEBUG_PRINT("\n");
    DEBUG_PRINT(" shu A: "); DEBUG_PRINT(getShuntCurrent_A()); DEBUG_PRINT("\n");
    DEBUG_PRINT(" pwr W: "); DEBUG_PRINT(getBusPower_W());     DEBUG_PRINT("\n");
}

inline float MyINA226::getBusVoltage_V(void)
{
    return ina_.readBusVoltage();
}

inline float MyINA226::getShuntVoltage_V(void)
{
    return ina_.readShuntVoltage();
}

inline float MyINA226::getShuntCurrent_A(void)
{
    return ina_.readShuntCurrent();
}

inline float MyINA226::getBusPower_W(void)
{
    return ina_.readBusPower();
}

/****************************
 * MyINA219 class implementation
 ****************************/
MyINA219::MyINA219(char *name, uint8_t slave_address)
    :IElectricPower(name),
    ina_(slave_address)
{
}

void MyINA219::begin(void)
{
    ina_.begin();
}

void MyINA219::showStatus(void)
{
    DEBUG_PRINT(name_);DEBUG_PRINT("\n");
    DEBUG_PRINT(" bus V: "); DEBUG_PRINT(getBusVoltage_V());   DEBUG_PRINT("\n");
    DEBUG_PRINT(" shu V: "); DEBUG_PRINT(getShuntVoltage_V()); DEBUG_PRINT("\n");
    DEBUG_PRINT(" cur A: "); DEBUG_PRINT(getShuntCurrent_A()); DEBUG_PRINT("\n");
}

float MyINA219::getBusVoltage_V(void)
{
    return ina_.getBusVoltage_V();
}

float MyINA219::getShuntVoltage_V(void)
{
    return ina_.getShuntVoltage_mV()/1000.0;
}

float MyINA219::getShuntCurrent_A(void)
{
    return ina_.getCurrent_mA()/1000.0;
}

/****************************
 * Macro definition
 ****************************/
//const uint8_t INA226_ADDRESS  = 0x40;
const uint8_t INA226_11_ADDRESS = 0x45;
const uint8_t INA226_DD_ADDRESS = 0x4a;
const uint8_t INA226_CC_ADDRESS = 0x4f;

//const uint8_t INA219_ADDRESS    = 0x40;
const uint8_t INA219_A0_ADDRESS   = 0x41;
const uint8_t INA219_A1_ADDRESS   = 0x44;
const uint8_t INA219_A0A1_ADDRESS = 0x45;

const int LED_SWITCH_PIN = 2;

/****************************
 * global variables
 ****************************/
#if !defined(ENABLE_DEBUG_HARD_SERIAL)
static XBee myXBee = XBee();
static XBeeAddress64 addrContributor = XBeeAddress64(XBEE_ADDRESS_H_COORDINATOR, XBEE_ADDRESS_L_COORDINATOR);
#endif

static MyINA226 battery = MyINA226("battery", INA226_CC_ADDRESS);
static MyINA226 solar = MyINA226("solar panel", INA226_DD_ADDRESS);
//static MyINA219 conv = MyINA219("converter", INA219_A0A1_ADDRESS);

static IElectricPower *powerSensors[] =
{
    static_cast<IElectricPower*>(&battery),
    static_cast<IElectricPower*>(&solar),
//    static_cast<IElectricPower*>(&conv)
};

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

void setup(void)
{
    setup_debug();

#if !defined(ENABLE_DEBUG_HARD_SERIAL)
    Serial.begin(XBEE_SERIAL_BAURATE);
    myXBee.setSerial(Serial);
#endif

    //FIXME: LED power on/off switch control.
    pinMode(LED_SWITCH_PIN, OUTPUT);
    digitalWrite(LED_SWITCH_PIN, LOW);

    for(auto sensor : powerSensors)
    {
        sensor->begin();
    }

#if (defined(ENABLE_DEBUG_HARD_SERIAL) || defined(ENABLE_DEBUG_SOFT_SERIAL))
    delay(5000);

    // Show configuration
    for(auto sensor : powerSensors)
    {
        sensor->showConfig();
    }
#endif
}

void loop(void)
{
    enum class SensorType : uint8_t
    {
        VOLTAGE = 0,
        CURRENT,
        WAT,
        MAX
    };

    //FIXME: LED power on/off switch control.
    static boolean led_on = false;
    SENSOR_DATA sensor_data[sizeof(powerSensors)/sizeof(IElectricPower*)][static_cast<int>(SensorType::MAX)] =
    {
        {
            {{'V', 'O', 'L'}, '0', 100, 0}, // bus voltage
            {{'C', 'U', 'R'}, '0', 100, 0}, // shunt current
            {{'W', 'A', 'T'}, '0', 100, 0}, // power
        },
        {
            {{'V', 'O', 'L'}, '0', 100, 0}, // bus voltage
            {{'C', 'U', 'R'}, '0', 100, 0}, // shunt current
            {{'W', 'A', 'T'}, '0', 100, 0}, // power
        },
    };

    digitalWrite(LED_SWITCH_PIN, led_on ? HIGH : LOW);
    led_on = !led_on;

    if (isTriggerToPost() != true)
    {
        return;
    }

#if (defined(ENABLE_DEBUG_HARD_SERIAL) || defined(ENABLE_DEBUG_SOFT_SERIAL))
    for(auto sensor : powerSensors)
    {
        sensor->showStatus();
    }
#endif

    for(uint8_t i = 0; i < sizeof(powerSensors)/sizeof(IElectricPower*); i++)
    {
        //FIXME: INA219 will crash.
        sensor_data[i][0].value = static_cast<int32_t>(sensor_data[i][0].multiple * static_cast<MyINA226*>(powerSensors[i])->getBusVoltage_V());
        sensor_data[i][1].value = static_cast<int32_t>(sensor_data[i][1].multiple * static_cast<MyINA226*>(powerSensors[i])->getShuntCurrent_A());
        sensor_data[i][2].value = static_cast<int32_t>(sensor_data[i][2].multiple * static_cast<MyINA226*>(powerSensors[i])->getBusPower_W());
    }

#if !defined(ENABLE_DEBUG_HARD_SERIAL)
    ZBTxRequest myTxRequest = ZBTxRequest(
            addrContributor,
            (uint8_t*)sensor_data,
            sizeof(sensor_data));

    myXBee.send(myTxRequest);
#endif
}

