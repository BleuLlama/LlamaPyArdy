
DIRNAME := $(shell basename `pwd`)
DATETIM := $(shell date +%Y%m%d_%H%M%S)
TARNAME := $(DIRNAME).$(DATETIM).tar


all:
	@echo Targets:  backup cleanup

backup: cleanup
	@cd .. ; tar -cvf $(TARNAME) $(DIRNAME) ; gzip $(TARNAME)
	@cd .. ; ls -l $(TARNAME).gz
	@echo ../$(TARNAME).gz
	@echo Done.

cleanup:
	@echo "Removing temp files"
	-find . -name "._*" | xargs rm
	-find . -name .DS_Store | xargs rm
	-find . -name "*.pyc" | xargs rm
	-find . -name "*.swp" | xargs rm

