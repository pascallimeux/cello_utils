.PHONY: default
default: help ;
RED    := $(shell tput -Txterm setaf 1)
GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)
MYSQL_LOGIN := "root"
MYSQL_PWD   := "123456"
EXPLORER_PRG_NAME := "main.js"
OLS_FOLDER:="/opt/ols"
COMPOSER_FOLDER:=$(OLS_FOLDER)/composer
EXPLORER_FOLDER:=$(OLS_FOLDER)/explorer
BC_EXPLORER_FOLDER=$(EXPLORER_FOLDER)/blockchain-explorer

setup: ##@Explorer Init database and config file.
	@cp $(EXPLORER_FOLDER)/local/config/config.json $(BC_EXPLORER_FOLDER)/config.json
	@sudo service mysql start 2>/dev/null
	@mysql -u$(MYSQL_LOGIN) -p$(MYSQL_PWD) < $(BC_EXPLORER_FOLDER)/db/fabricexplorer.sql 2>/dev/null

start-explorer: ##@Explorer Start blockchain-explorer.
	@pm2 start $(BC_EXPLORER_FOLDER)/$(EXPLORER_PRG_NAME)

stop-explorer:  ##@Explorer Stop blockchain-explorer'. 
	@pm2 stop $(BC_EXPLORER_FOLDER)/$(EXPLORER_PRG_NAME)	

log-explorer: ##@Explorer Display log of blockchain-explorer.
	@pm2 logs

create-cards: ##@Playground Init networks and cards.
	@cd composer && python3 setup_bn.py

stop-playground:  ##@Playground Stop playground. 
	@$(eval PID=`pidof node `)          
	@if [ -n "$(PID)" ]; then \
		echo  "Kill playground, process: "$(PID) && \
		kill -9 $(PID); \
	else \
		echo "Playground is not running"; \
	fi

start-playground: ##@Playground Start playground.
	@$(eval PID=`pidof node `)
	@echo $(PID)    
	@if [ -n "$(PID)" ]; then \
		echo "Playground is already running! process: "$(PID); \
	else \
		nohup composer-playground -p 9000 & > playground.log; \
	fi

log-playground: ##@Playground Display log of playground.
	@$(eval PID=`pidof node`)  
	@if [ -n "$(PID)" ]; then \
		tail -f playground.log; \
	else \
		echo "Playground is not running"; \
	fi

HELP_FUN = \
	%help; \
	while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
	print "usage: make [target]\n\n"; \
	for (sort keys %help) { \
	print "${WHITE}$$_:${RESET}\n"; \
	for (@{$$help{$$_}}) { \
	$$sep = " " x (32 - length $$_->[0]); \
	print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
	}; \
	print "\n"; }

help: ##@other Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)
