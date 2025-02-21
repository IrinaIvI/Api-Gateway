### API GATEWAY

API для взаимодействия между клиентом и внутренними сервисами. Проект собран внутри контейнера Docker.

### Оглавление

1. [Описание проекта](#описание-проекта)
2. [Функциональность](#функциональность)
3. [Требования](#требования)
4. [Запуск](#запуск)


### Описание проекта

Данный проект предоставляет к сервисам, служащих для следующих операций:

- Регистрация пользователя
- Авторизация пользователя
- Создание транзакции
- Получение отчета о транзакциях за указанный период времени

### Функциональность

1. **Регистрация пользователя**: Асинхронная функция `api_registration` отправляет запрос для регистрации нового пользователя с использованием логина и пароля.

2. **Авторизация пользователя**: Асинхронная функция `api_authorisation` отправляет запрос для авторизации пользователя с предоставленным логином и паролем.

3. **Создание транзакции**: Асинхронная функция `api_create_transaction` создает новую транзакцию для пользователя, если токен авторизации действителен.

4. **Получение отчета о транзакциях**: Асинхронная функция `api_get_transaction` получает отчет о транзакциях за указанный период, если токен авторизации действителен.

### Требования

- Docker
- Python 3.11+
- Poetry (для управления зависимостями)

### Запуск

Чтобы собрать и запустить Docker образ, выполните следующие команды:

- `docker build -t api_gateway .`
- `docker run -it -p 8000:8000 api_gateway`

Чтобы остановить контейнер, выполните:

`docker stop api_gateway`

Чтобы запустить все сервисы, определенные в `docker-compose.yml`, выполните:

`docker-compose up`

Чтобы остановить все сервисы, выполните:

`docker-compose stop`

