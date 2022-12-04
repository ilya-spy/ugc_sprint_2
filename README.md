# Проектная работа 8 спринта

Проектные работы в этом модуле выполняются в командах по 3 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.  

Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Slack в канале #group_projects.  
Задания на спринт вы найдёте внутри тем.  
<br>
# Запуск сервиса
```
make ugc/dev/setup
# после исполнения необходимо создать общую структуру ClickHouse с учетом шардов, реплик и таблиц 
make clickhouse/docker/admin  
clickhouse_admin@clickhouse-admin:/usr/src/clickhouse_admin$  python main.py
```

# Запуск отдельных частей сервиса
### Запуск ClickHouse служб  
```
# запуск/остановка dev окружения  
make clickhouse/setup/dev  
make clickhouse/teardown/dev

# запуск/остановка prod окружения  
make clickhouse/setup/prod  
make clickhouse/teardown/prod  
```

### Работа с OLAP-кластером  
```
# Инициализация кластера  
make clickhouse/docker/admin  
clickhouse_admin@clickhouse-admin:/usr/src/clickhouse_admin$  python main.py

# Доступ в ноды кластера и работа с SQL напрямую  
make clickhouse/docker/node2  
root@clickhouse-node2:/# clickhouse-client  

clickhouse-node2 :) SHOW TABLES
clickhouse-node2 :) SELECT * FROM olap_views
```

### Запуск Гейта
```shell
cd devops/docker
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file ../.env build
docker-compose -f docker-compose.yml -f docker-compose.dev.yml --env-file ../.env up

# подключиться к контейнеру
docker-compose -f docker-compose.yml -f docker-compose.dev.yml exec ugc_gate_api bash
```

### Ручное тестирование
```shell
# для неавторизованного пользователя должно вернуть ошибку
curl -X 'POST' 'http://localhost:8004/api/v1/progress/' -H 'accept: application/json' -d ''

# ...к этому моменту должны быть подняты все микросервисы Проекат

# создаём нового пользователя и заолгиниться
curl -XPOST -H "Content-Type: application/json" http://localhost/auth_api/v1/user -d '{"username": "test_user","email": "test@gmail.com","password": "12345"}'
export AUTH_API_ACCESS_TOKEN=$(curl -s -XPOST -H "Content-Type: application/json" http://localhost/auth_api/v1/login -d '{"username": "test_user", "password": "12345"}' | jq '.access' | xargs -L 1)

# отправляем данные от имени авторизованного пользователя
curl -X 'POST' 'http://localhost:8004/api/v1/progress/' -H 'accept: application/json' -H "Authorization: Bearer $AUTH_API_ACCESS_TOKEN" -d ''
```
