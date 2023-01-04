# Ссылка на GitHub репозиторий

[ugc_sprint_2](https://github.com/merkushov/ugc_sprint_2)

# Проектная работа 9 спринта

Проектные работы в этом модуле выполняются в командах по 3 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.  

Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Slack в канале #group_projects.  
Задания на спринт вы найдёте внутри тем.  
<br>
# Запуск сервиса
```
make ugc/dev/setup
# после исполнения необходимо создать общую структуру ClickHouse с учетом шардов, реплик и таблиц 
make clickhouse/docker/admin  
olap@clickhouse-admin:/usr/src/ugc$  python cluster/main.py
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
olap@clickhouse-admin:/usr/src/ugc$  python cluster/main.py

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
curl -X 'POST' \
  'http://localhost:8004/api/v1/progress/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'accept: application/json' -H "Authorization: Bearer $AUTH_API_ACCESS_TOKEN" \
  -d '{
  "movie_id": "84906673-b9f2-44a6-a4e6-2e1d278726ea",
  "frames": 123
}'
```

# Использование pre-commit
Для единообразия кода в проекте используется pre-commit, который при каждом коммите проверяет стилистику кода и ряд 
правил работы с git

Среди используемых инструментов:
- black
- isort
- flake8
- autopep8


Установка pre-commit
```shell
pip install pre-commit
pre-commit install
```

Настройка pre-commit осуществляется с помощью файла [конфигурации](.pre-commit-config.yaml)

## Особенности использования
При обнаружении недочетов isort, black, autopep8 их исправят, а flake8 выведет в консоль ссылки на проблемные места. 
<br>В каждом из случаев вы увидите сообщение о безуспешной попытке коммита "Commit failed with error". <br>Не отчаивайтесь, повторите коммит если вы пользуетесь git через GUI.
<br>Если пользуетесь командной строкой или терминалом добавьте __изменения 
в индекс__ и сделайте commit
```shell
git add file-for-commit
git commit -m 'commit message'
```
