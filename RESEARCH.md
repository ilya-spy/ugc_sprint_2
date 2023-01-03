# Результаты исследования производительности кластера MongoDB

Локальные запуски внутри кластера
Симуляция данных реального времени - вставка по одной записи в коллекцию

1. Запускаем кластер:  
`make mongo\dev\setup`  

2. Инициализируем ноды
Внутри соответсвующих контейнеров (cfg1, rs1n1, rs2n1, mongos1) запускаем скрипты инициализации из папки /scripts  
`root@mongocfg1#:  cat /scipts/init_cfg1.js | mongosh`  
`root@mongors1n1#: cat /scipts/init_rs1n1.js | mongosh`  
`root@mongors2n1#: cat /scipts/init_rs2n2.js | mongosh`  
`root@mongos1#:    cat /scipts/init_s1.js | mongosh`  

3. После успешной сборки контейнеров будет доступна ссылка по адресу http://127.0.0.1/, логинимся в контейнер mongos1

3. Запускаем иследование  
`apt update`  
`apt-get install python pip`  
`pip install pymongo`  
`python3 /test/analytics.py`  

## Итоги тестов
### Вставка
Вставка 10 000 строк данных в MongoDB:  
`0:00:51`  

### Поиск
Поиск по массиву данных размером в 10 000 строк (1000 случайных выборок) MongoDB:  
`0:00:32`  
