.PHONY:all clean

PLANTUML := plantuml.jar
CONFIG := config.txt
DEPEND_FILES := makefile $(PLANTUML) $(CONFIG)

all:sequence_init_term.png sequence_monitoring.png

%.png:%.uml $(DEPEND_FILES)
	#java -jar $(PLANTUML) -config $(CONFIG) $<
	java -jar $(PLANTUML) $<
	gnome-open $@

clean:
	rm -f *.png
