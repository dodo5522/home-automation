/*
 Example code for my solar plant monitor.
 Editor     : Takashi Ando
 Version    : 1.0
*/
#include <Serial.h>
#include <Wire.h>
#include <INA226.h>
#include <Adafruit_INA219.h>

static INA226 g_ina_solar;
static INA226 g_ina_battery;
static Adafruit_INA219 g_ina_converter(0x45);

void checkConfig(INA226 ina)
{
    Serial.print("Mode:                  ");
    switch (ina.getMode())
    {
        case INA226_MODE_POWER_DOWN:      Serial.println("Power-Down"); break;
        case INA226_MODE_SHUNT_TRIG:      Serial.println("Shunt Voltage, Triggered"); break;
        case INA226_MODE_BUS_TRIG:        Serial.println("Bus Voltage, Triggered"); break;
        case INA226_MODE_SHUNT_BUS_TRIG:  Serial.println("Shunt and Bus, Triggered"); break;
        case INA226_MODE_ADC_OFF:         Serial.println("ADC Off"); break;
        case INA226_MODE_SHUNT_CONT:      Serial.println("Shunt Voltage, Continuous"); break;
        case INA226_MODE_BUS_CONT:        Serial.println("Bus Voltage, Continuous"); break;
        case INA226_MODE_SHUNT_BUS_CONT:  Serial.println("Shunt and Bus, Continuous"); break;
        default: Serial.println("unknown");
    }

    Serial.print("Samples average:       ");
    switch (ina.getAverages())
    {
        case INA226_AVERAGES_1:           Serial.println("1 sample"); break;
        case INA226_AVERAGES_4:           Serial.println("4 samples"); break;
        case INA226_AVERAGES_16:          Serial.println("16 samples"); break;
        case INA226_AVERAGES_64:          Serial.println("64 samples"); break;
        case INA226_AVERAGES_128:         Serial.println("128 samples"); break;
        case INA226_AVERAGES_256:         Serial.println("256 samples"); break;
        case INA226_AVERAGES_512:         Serial.println("512 samples"); break;
        case INA226_AVERAGES_1024:        Serial.println("1024 samples"); break;
        default: Serial.println("unknown");
    }

    Serial.print("Bus conversion time:   ");
    switch (ina.getBusConversionTime())
    {
        case INA226_BUS_CONV_TIME_140US:  Serial.println("140uS"); break;
        case INA226_BUS_CONV_TIME_204US:  Serial.println("204uS"); break;
        case INA226_BUS_CONV_TIME_332US:  Serial.println("332uS"); break;
        case INA226_BUS_CONV_TIME_588US:  Serial.println("558uS"); break;
        case INA226_BUS_CONV_TIME_1100US: Serial.println("1.100ms"); break;
        case INA226_BUS_CONV_TIME_2116US: Serial.println("2.116ms"); break;
        case INA226_BUS_CONV_TIME_4156US: Serial.println("4.156ms"); break;
        case INA226_BUS_CONV_TIME_8244US: Serial.println("8.244ms"); break;
        default: Serial.println("unknown");
    }

    Serial.print("Shunt conversion time: ");
    switch (ina.getShuntConversionTime())
    {
        case INA226_SHUNT_CONV_TIME_140US:  Serial.println("140uS"); break;
        case INA226_SHUNT_CONV_TIME_204US:  Serial.println("204uS"); break;
        case INA226_SHUNT_CONV_TIME_332US:  Serial.println("332uS"); break;
        case INA226_SHUNT_CONV_TIME_588US:  Serial.println("558uS"); break;
        case INA226_SHUNT_CONV_TIME_1100US: Serial.println("1.100ms"); break;
        case INA226_SHUNT_CONV_TIME_2116US: Serial.println("2.116ms"); break;
        case INA226_SHUNT_CONV_TIME_4156US: Serial.println("4.156ms"); break;
        case INA226_SHUNT_CONV_TIME_8244US: Serial.println("8.244ms"); break;
        default: Serial.println("unknown");
    }

    Serial.print("Max possible current:  ");
    Serial.print(ina.getMaxPossibleCurrent());
    Serial.println(" A");

    Serial.print("Max current:           ");
    Serial.print(ina.getMaxCurrent());
    Serial.println(" A");

    Serial.print("Max shunt voltage:     ");
    Serial.print(ina.getMaxShuntVoltage());
    Serial.println(" V");

    Serial.print("Max power:             ");
    Serial.print(ina.getMaxPower());
    Serial.println(" W");
}
void setup(void)
{
    Serial.begin(9600);

    pinMode(9, OUTPUT);
    digitalWrite(9, LOW);

    g_ina_converter.begin();
    g_ina_battery.begin(0x4f);
    g_ina_solar.begin(0x4a);

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

    delay(5000);

    // Display configuration
    checkConfig(g_ina_battery);
    checkConfig(g_ina_solar);
}

void loop(void)
{
    static boolean led_on = false;
    digitalWrite(9, led_on ? HIGH : LOW);
    led_on = !led_on;

    Serial.println("battery:");
    Serial.print("shu A: ");Serial.println(g_ina_battery.readShuntCurrent());
    Serial.print("shu V: "); Serial.println(g_ina_battery.readShuntVoltage());
    Serial.print("bus P: "); Serial.println(g_ina_battery.readBusPower());
    Serial.print("bus V: "); Serial.println(g_ina_battery.readBusVoltage());

    Serial.println("solar:");
    Serial.print("shu A: ");Serial.println(g_ina_solar.readShuntCurrent());
    Serial.print("shu V: "); Serial.println(g_ina_solar.readShuntVoltage());
    Serial.print("bus P: "); Serial.println(g_ina_solar.readBusPower());
    Serial.print("bus V: "); Serial.println(g_ina_solar.readBusVoltage());

    Serial.println("charge converter:");
    Serial.print("bus V: "); Serial.println(g_ina_converter.getBusVoltage_V());
    Serial.print("shu V: "); Serial.println(g_ina_converter.getShuntVoltage_mV());
    Serial.print("cur mA: ");Serial.println(g_ina_converter.getCurrent_mA());

    delay(3000);
}

