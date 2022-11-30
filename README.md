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

### Запуск Kafka
    # запуск контейнеров kafka и zookeeper

