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

class IElectricPower
{
public:
    virtual void begin(void);

    virtual boolean hasAvilityCurrent(void);
    virtual boolean hasAvilityVoltage(void);

    virtual float getBusVoltage_V(void);
    virtual float getShuntVoltage_V(void);
    virtual float getShuntCurrent_A(void);

    virtual void showConfig(void);
    virtual void showStatus(void);
};

class MyINA226 : public IElectricPower
{
public:
    MyINA226(char *name,
            uint8_t slave_address,
            float rShuntValueOhm = 0.002,
            float iMaxExceptedCurrent_A = 2.0,
            ina226_averages_t avg = INA226_AVERAGES_1,
            ina226_busConvTime_t busConvTime = INA226_BUS_CONV_TIME_1100US,
            ina226_shuntConvTime_t shuntConvTime = INA226_SHUNT_CONV_TIME_1100US,
            ina226_mode_t mode = INA226_MODE_SHUNT_BUS_CONT);
    virtual ~MyINA226(void){};

    virtual void begin(void) final;

    virtual void showConfig(void) final;
    virtual void showStatus(void) final;

    virtual boolean hasAvilityCurrent(void) final { return true; };
    virtual boolean hasAvilityVoltage(void) final { return true; };

    virtual float getBusVoltage_V(void) final;
    virtual float getShuntVoltage_V(void) final;
    virtual float getShuntCurrent_A(void) final;
    float getBusPower_W(void);

private:
    INA226 ina_;
    char name_[16];
    uint8_t slave_address_;
    ina226_averages_t averages_;
    ina226_busConvTime_t busConvTime_;
    ina226_shuntConvTime_t shuntConvTime_;
    ina226_mode_t mode_;
    float rShuntValueOhm_;
    float iMaxExceptedCurrent_A_;
};

class MyINA219 : public IElectricPower
{
public:
    MyINA219(char *name, uint8_t slave_address);
    virtual ~MyINA219(void){};

    virtual void begin(void) final;

    virtual void showConfig(void) final {};
    virtual void showStatus(void) final;

    virtual boolean hasAvilityCurrent(void) final { return true; };
    virtual boolean hasAvilityVoltage(void) final { return false; };

    virtual float getBusVoltage_V(void) final;
    virtual float getShuntVoltage_V(void);
    virtual float getShuntCurrent_A(void) final;

private:
    Adafruit_INA219 ina_;
    char name_[16];
};

#endif

