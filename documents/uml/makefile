.PHONY:all clean

PLANTUML := plantuml.jar
CONFIG := config.txt
DEPEND_FILES := makefile $(PLANTUML) $(CONFIG)

all:sequence_processes.png

%.png:%.uml $(DEPEND_FILES)
	#java -jar $(PLANTUML) -config $(CONFIG) $<
	java -jar $(PLANTUML) $<

clean:
	rm -f *.png
