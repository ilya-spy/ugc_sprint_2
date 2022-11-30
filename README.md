# Проектная работа 8 спринта

Проектные работы в этом модуле выполняются в командах по 3 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.  
Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Slack в канале #group_projects.  
Задания на спринт вы найдёте внутри тем.  

### Запуск ClickHouse служб
    # запуск dev окружения  
    make clickhouse/setup/dev

    # запуск prod окружения  
    make clickhouse/setup/prod  

### Запуск Гейта

```shell
cd devops/docker
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file ../.env build
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file ../.env up

# подключиться к контейнеру
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec ugc_gate_api bash
```