### Студенчиский проект yandex-praktikum команды №8

### Основые компоненты

##### API фильмов
Коллекция фильмов, жанров и персон, для создания онлайн кинотеатра

##### Админка
Позвляет вносить изменения в содержание того, что отдает API

##### Сервис (ETL)
Выгружает данные из админки в в API

##### Swagger

http://localhost/api/openapi

### Запуск проекта 

1. Включить vpn
2. Из корневой директории выполнить, docker-compose up
3. Дождаться, когда в логах появится таблица с тестами

**Перезапуск проекта**

1. docker-compose down
2. docker image prune --all 
3. Удалить папку etl/local_storage

### Ссылка на репозиторий

https://github.com/efgraph/Async_API_sprint_1




