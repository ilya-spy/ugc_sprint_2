# Проектная работа 8 спринта

Проектные работы в этом модуле выполняются в командах по 3 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.  

Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Slack в канале #group_projects.  
Задания на спринт вы найдёте внутри тем.  
<br>
### Запуск ClickHouse служб
    # запуск/остановка dev окружения  
    make clickhouse/setup/dev  
    make clickhouse/teardown/dev

    # запуск/остановка prod окружения  
    make clickhouse/setup/prod  
    make clickhouse/teardown/prod  

### Работа с OLAP-кластером
    # Инициализация кластера  
    make clickhouse/docker/admin  
    clickhouse_admin@clickhouse-admin:/usr/src/clickhouse_admin$  python main.py

    # Доступ в ноды кластера и работа с SQL напрямую  
    make clickhouse/docker/node2  
    root@clickhouse-node2:/# clickhouse-client  

    clickhouse-node2 :) SHOW TABLES
    clickhouse-node2 :) SELECT * FROM olap_views