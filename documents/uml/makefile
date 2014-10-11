.PHONY:all clean

PLANTUML := plantuml.jar
CONFIG := config.txt
DEPEND_FILES := makefile $(PLANTUML) $(CONFIG)

all:sequence_init_term.png sequence_monitoring.png
	for PNG in $^; do \
		if ! [ -z "`which gnome-open`" ]; then \
			gnome-open $${PNG}; \
		elif ! [ -z "`which open`" ]; then \
			open $${PNG}; \
		fi; \
	done

%.png:%.uml $(DEPEND_FILES)
	java -jar $(PLANTUML) -config $(CONFIG) $<

clean:
	rm -f *.png
