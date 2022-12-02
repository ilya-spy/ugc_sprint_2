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
# Команды развёртывания UGC стенда (все сервисы вместе, ниже есть команды для запуска компонент по отдельности)
#
ugc/%: export DEVOPS_DIR := devops/etl
ugc/%: export DOCKER_DIR := devops/docker

ugc/setup/dev: export DOCKER_TARGET := dev
ugc/setup/dev:
	@make docker/prepare
	@make docker/setup
.PHONY: ugc/setup/dev

ugc/teardown/dev: export DOCKER_TARGET := dev
ugc/teardown/dev:
	@make docker/prepare
	@make docker/destroy
.PHONY: ugc/teardown/dev

#
# Команды развертывания и доступа в кластер ClickHouse
#
clickhouse/%: export DOCKER_DIR := devops/docker/clickhouse

clickhouse/setup/dev: export DOCKER_TARGET := dev
clickhouse/setup/dev:
	@make docker/prepare
	@make docker/setup
.PHONY: clickhouse/setup/dev

clickhouse/setup/prod: export DOCKER_TARGET := prod
clickhouse/setup/prod:
	@make docker/prepare
	@make docker/setup
.PHONY: clickhouse/setup/prod

clickhouse/teardown/dev: export DOCKER_TARGET := dev
clickhouse/teardown/dev:
	@make docker/prepare
	@make docker/destroy
.PHONY: clickhouse/teardown/dev

clickhouse/teardown/prod: export DOCKER_TARGET := prod
clickhouse/teardown/prod:
	@make docker/prepare
	@make docker/destroy
.PHONY: clickhouse/teardown/prod

clickhouse/docker/admin:
	@docker exec -it clickhouse-admin bash
clickhouse/docker/node1:
	@docker exec -it clickhouse-node1 bash
clickhouse/docker/node2:
	@docker exec -it clickhouse-node2 bash
clickhouse/docker/node3:
	@docker exec -it clickhouse-node3 bash
clickhouse/docker/node4:
	@docker exec -it clickhouse-node4 bash


#
# Команды развертывания и доступа в Kafka
#
kafka/%: export DEVOPS_DIR := devops/kafka
kafka/%: export DOCKER_DIR := devops/docker/kafka

kafka/setup/dev: export DOCKER_TARGET := dev
kafka/setup/dev:
	@make docker/prepare
	@make docker/setup
.PHONY: kafka/setup/dev

kafka/teardown/dev: export DOCKER_TARGET := dev
kafka/teardown/dev:
	@make docker/prepare
	@make docker/destroy


#
#  Базовые команды для сборки и запуска заданных Докер-контейнеров (разные цели сборки выше задают $DOCKER_DIR / $DOCKER_TARGET / $DEVOPS_DIR)
#
docker/%: export DOCKER_COMPOSE := docker-compose -f $(DOCKER_DIR)/docker-compose.yml -f $(DOCKER_DIR)/docker-compose.$(DOCKER_TARGET).yml --env-file devops/docker/.env

docker/prepare:
	@printf "Setting up base environment: $(OS)\n"
	@find devops -iname ".env.example" -exec cp "{}" $(echo "{}" | sed s/.example//) \;

	# установить HOST_UID = UID текущего пользователя. Это влияет на UID пользователя внутри контейнера.
	# Нужно для совместимости прав доступа к сгенерированным файлам у хостового пользователя
	# На Windows host также необходимо переформатирование команд (кавычки и т.д.)
	@if [[ $(OS) = 'Darwin' ]]; then \
		`id -u | xargs -I '{}' sed -i '' 's/HOST_UID=.*/HOST_UID={}/' devops/docker/.env`; \
		`sed -i '' 's/HOST_GID=.*/HOST_GID=61/' ../.env`; \
	elif [[ $(OS) = 'Windows_NT' ]]; then \
		`id -u | xargs -I '{}' sed -i "s/HOST_UID=.*/HOST_UID={}/" devops/docker/.env`; \
		`id -g | xargs -I '{}' sed -i "s/HOST_GID=.*/HOST_GID={}/" devops/docker/.env`; \
	else \
		`id -u | xargs -I '{}' sed -i '' 's/HOST_UID=.*/HOST_UID={}/' devops/docker/.env`; \
		`id -g | xargs -I '{}' sed -i '' 's/HOST_GID=.*/HOST_GID={}/' devops/docker/.env`; \
	fi
	@printf "Set up environment for: $(DOCKER_TARGET)\n"
	@printf "Invoke composer command: $(DOCKER_COMPOSE)\n"
docker/prepare:
.PHONY: docker/prepare

## перестроить и перезапустить контейнеры
docker/setup:
	@make docker/destroy
	@make docker/build
	@make docker/start
docker/setup:
.PHONY: docker/setup

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

## остановить все контейнеры
docker/stop:
	$(DOCKER_COMPOSE) down
.PHONY: docker/stop

## остановить и удалить все контейнеры
docker/down:
	$(DOCKER_COMPOSE) down --remove-orphans
.PHONY: docker/down

## остановить/удалить контейнеры и очистить данные томов
docker/destroy:
	$(DOCKER_COMPOSE) down --volumes --remove-orphans
.PHONY: docker/destroy
