ifndef VERBOSE
.SILENT:
endif
.DEFAULT_GOAL := help

ifeq ($(OS),)
OS := $(shell uname)
endif


#
# Cписок доступных команд
#
help:
	@grep -E '^[a-zA-Z0-9_\-\/]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo "(Other less used targets are available, open Makefile for details)"
.PHONY: help


#
# Основные команды для развертывания конфигураций
#
clickhouse/setup/dev: export DOCKER_DIR := devops/clickhouse
clickhouse/setup/dev: export DOCKER_TARGET := dev
clickhouse/setup/dev:
	@make setup/base
.PHONY: clickhouse/setup/dev

clickhouse/setup/prod: export DOCKER_DIR := devops/clickhouse
clickhouse/setup/prod: export DOCKER_TARGET := prod
clickhouse/setup/prod:
	@make setup/base
.PHONY: clickhouse/setup/prod


#
# Настроить базовое окружение для всех конфигураций
#
setup/base: export DOCKER_COMPOSE := docker-compose -f $(DOCKER_DIR)/docker-compose.yml -f $(DOCKER_DIR)/docker-compose.$(DOCKER_TARGET).yml --env-file .env
setup/base:
	@printf "\nSetting up base environment: $(OS)\n"
	@cp $(DOCKER_DIR)/.env.example $(DOCKER_DIR)/.env
	@cp .env.example .env

	# установить HOST_UID = UID текущего пользователя. Это влияет на UID пользователя внутри контейнера.
	# Нужно для совместимости прав доступа к сгенерированным файлам у хостового пользователя
	# На Windows host также необходимо переформатирование команд (кавычки и т.д.)
	@if [[ $(OS) = 'Darwin' ]]; then \
		`id -u | xargs -I '{}' sed -i '' 's/HOST_UID=.*/HOST_UID={}/' .env`; \
		`sed -i '' 's/HOST_GID=.*/HOST_GID=61/' ../.env`; \
	elif [[ $(OS) = 'Windows_NT' ]]; then \
		`id -u | xargs -I '{}' sed -i "s/HOST_UID=.*/HOST_UID={}/" .env`; \
		`id -g | xargs -I '{}' sed -i "s/HOST_GID=.*/HOST_GID={}/" .env`; \
	else \
		`id -u | xargs -I '{}' sed -i '' 's/HOST_UID=.*/HOST_UID={}/' .env`; \
		`id -g | xargs -I '{}' sed -i '' 's/HOST_GID=.*/HOST_GID={}/' .env`; \
	fi
	@cat .env
	@printf "\n\nSetting up compose target: $(DOCKER_TARGET)\n"
	@make docker/destroy
	@make docker/build
	@make docker/start
setup/base:
.PHONY: setup/base


#
# Докер команды для управления контейнерами
#

## построить контейнеры
docker/build:
	$(DOCKER_COMPOSE) build
.PHONY: docker/build

## поднять Докер
docker/start:
	$(DOCKER_COMPOSE) up -d
.PHONY: docker/start

# алиас для docker/start
docker/up: docker/start
.PHONY: docker/up

## остановить все контейнеры Приложения
docker/stop:
	$(DOCKER_COMPOSE) down
.PHONY: docker/stop

## остановить и удалить все контейнеры Приложения
docker/down:
	$(DOCKER_COMPOSE) down --remove-orphans
.PHONY: docker/down

## остановить/удалить контейнеры и очистить данные Приложения
docker/destroy:
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
.PHONY: docker/destroy
