#ifndef _POWER_PLANT_H_
#define _POWER_PLANT_H_

/****************************
 * Macro definition
 ****************************/
#define ENABLE_DEBUG_SOFT_SERIAL
//#define ENABLE_DEBUG_HARD_SERIAL

// If the interval is less than integration time, setup() set the integration time as minimum.
#if (defined(ENABLE_DEBUG_HARD_SERIAL) || defined(ENABLE_DEBUG_SOFT_SERIAL))
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
enum class SENSOR_ARRAY_NUM : uint8_t
{
    E_SENSOR_CURRENT_VOLTAGE0 = 0,
    E_SENSOR_CURRENT_VOLTAGE1,
    E_SENSOR_CURRENT,
    E_SENSOR_MAX,
};

class IElectricPower
{
public:
    IElectricPower(char *name);
    virtual ~IElectricPower(void){};

    virtual void begin(void) = 0;

    virtual void showConfig(void);
    virtual void showStatus(void) = 0;

    virtual inline boolean hasAvilityCurrent(void){ return false; } ;
    virtual inline boolean hasAvilityVoltage(void){ return false; };

    virtual float getBusVoltage_V(void) = 0;
    virtual float getShuntVoltage_V(void) = 0;
    virtual float getShuntCurrent_A(void) = 0;

protected:
    char name_[16];
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

    void begin(void);

    void showConfig(void);
    void showStatus(void);

    inline boolean hasAvilityCurrent(void){ return true; };
    inline boolean hasAvilityVoltage(void){ return true; };

    float getBusVoltage_V(void);
    float getShuntVoltage_V(void);
    float getShuntCurrent_A(void);
    float getBusPower_W(void);

private:
    INA226 ina_;
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

    void begin(void) final;

    void showStatus(void);

    inline boolean hasAvilityCurrent(void){ return true; };

    float getBusVoltage_V(void);
    float getShuntVoltage_V(void);
    float getShuntCurrent_A(void);

private:
    Adafruit_INA219 ina_;
};

#endif

