ARDUINO_DIR      = /Applications/Arduino.app/Contents/Java
ARDMK_DIR        = ../make_env
AVR_TOOLS_DIR    = $(ARDUINO_DIR)/hardware/tools/avr
MONITOR_PORT     = /dev/cu.usbserial*
MONITOR_BAUDRATE = 9600
BOARD_TAG        = pro
MCU              = atmega328p
F_CPU            = 8000000L
HEX_MAXIMUM_SIZE = 32768
ARDUINO_LIBS     = SoftwareSerial Wire XBee TSL2561 HTU21D MOISTURE_SEN0114 datatype debug
CXXFLAGS_STD     = -std=c++11
CPPFLAGS        += -fno-threadsafe-statics
ifneq ($(DEBUG),)
CPPFLAGS        += -DENABLE_DEBUG_$(DEBUG)_SERIAL
endif
USER_LIB_PATH   := $(realpath ../libraries)

AVRDUDE_ARD_BAUDRATE = 57600
AVRDUDE_CONF = $(ARDUINO_DIR)/hardware/tools/avr/etc/avrdude.conf

include ../make_env/Arduino.mk
