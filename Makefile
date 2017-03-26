ifeq (${COMPOSE_FILE},)
CONFIG_FILE = docker-compose.yml
else
CONFIG_FILE = ${COMPOSE_FILE}
endif

COMMAND = docker-compose -f ${CONFIG_FILE}

MANAGE = ${COMMAND} run --rm web python manage.py

django:
	${MANAGE} $(filter-out $@, $(MAKECMDGOALS))

test:
	${MANAGE} test

run:
	${COMMAND} up web

container-shell:
	${COMMAND} run --rm web bash

build:
	${COMMAND} build

default: build run

bash:
	${COMMAND} run --rm web bash

deploy: build
	${COMMAND} run --rm collectstatic
	${MANAGE} run --rm migrate
	${COMMAND} restart
