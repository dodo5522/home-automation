ARDUINO_DIR      = /Applications/Arduino.app/Contents/Resources/Java
ARDMK_DIR        = ../make_env
AVR_TOOLS_DIR    = $(ARDUINO_DIR)/hardware/tools/avr
MONITOR_PORT     = /dev/cu.usb*
MONITOR_BAUDRATE = 9600
BOARD_TAG        = pro
MCU              = atmega328p
F_CPU            = 8000000L
HEX_MAXIMUM_SIZE = 32768
ARDUINO_LIBS     = SoftwareSerial Wire XBee INA226 Adafruit_INA219 datatype debug
CXXFLAGS_STD     = -std=c++11
CPPFLAGS        += -fno-threadsafe-statics
ifneq ($(DEBUG),)
CPPFLAGS        += -DENABLE_DEBUG_$(DEBUG)_SERIAL
endif

AVRDUDE_ARD_BAUDRATE = 57600
AVRDUDE_CONF = $(ARDUINO_DIR)/hardware/tools/avr/etc/avrdude.conf

include ../make_env/Arduino.mk
