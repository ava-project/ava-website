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
	${MANAGE} test --keep

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
	${MANAGE} collectstatic --noinput
	${MANAGE} migrate
	${COMMAND} restart
