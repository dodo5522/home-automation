.PHONY:all clean

PLANTUML := plantuml.jar
CONFIG := config.txt
DEPEND_FILES := $(PLANTUML) $(CONFIG)

all:sample.png

sample.png:sample.txt $(DEPEND_FILES)
	java -jar $(PLANTUML) -config $(CONFIG) $<
	open $@

clean:
	rm -f sample.png
