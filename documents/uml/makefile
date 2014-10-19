PLANTUML := plantuml.jar
CONFIG := config.txt
DEPEND_FILES := makefile $(PLANTUML) $(CONFIG)

define SHOW_IMAGE
$(shell \
	if [ -z "$(BUILD_ENV)" ]; then \
		OS=`uname`; \
		if [ "$${OS}" = 'Darwin' ]; then \
			open $1; \
		elif [ "$${OS}" = 'Linux' ]; then \
			gnome-open $1; \
		fi; \
	fi)
endef

.PHONY:all

all:seq class

.PHONY:seq seq_init seq_monitor seq_alive

seq:seq_init seq_monitor seq_alive
	@echo $@ done.

seq_init:sequence_init_term.png
	$(call SHOW_IMAGE,$<)

seq_monitor:sequence_monitoring.png
	$(call SHOW_IMAGE,$<)

seq_alive:sequence_check_alive.png
	$(call SHOW_IMAGE,$<)

%.png:%.uml $(DEPEND_FILES)
	java -jar $(PLANTUML) -config $(CONFIG) $<

.PHONY:class class_process class_xbee class_monitor

class:class_process class_xbee class_monitor
	@echo $@ done.

class_process:
class_xbee:
class_monitor:

.PHONY:clean

clean:
	rm -f *.png

