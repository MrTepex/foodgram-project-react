![Foodgram project](https://github.com/MrTepex/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# **Foodgram project**

# Описание

**«Продуктовый помощник»** - это сайт, на котором пользователи могут _публиковать_ рецепты,
добавлять чужие рецепты в _избранное_ и _подписываться_ на публикации других авторов.
Сервис **«Список покупок»** создаёт список продуктов (в формате .txt),
которые нужно купить для приготовления выбранных блюд.

# Админка

```
login: admin
password: admin
```

# Технологии

- [Python 3.7](https://www.python.org/downloads/release/python-370/)
- [Django 2.2.16](https://www.djangoproject.com/download/)
- [Django Rest Framework 3.12.4](https://www.django-rest-framework.org/)
- [PostgreSQL 15.2](https://www.postgresql.org/download/)
- [gunicorn 20.1.0](https://pypi.org/project/gunicorn/)
- [nginx](https://nginx.org/ru/download.html)

# Контейнер

- [Docker 20.10.22](https://www.docker.com/)
- [Docker Compose 2.15.1](https://docs.docker.com/compose/)

# URL's

- http://tepex.myftp.org
- http://tepex.myftp.org/admin
- http://tepex.myftp.org/api


# Документация

Для просмотра документации к API перейдите по адресу:
- на сайте:  http://tepex.myftp.org/api/docs/redoc.html

- локально: http://localhost/api/docs/redoc.html

# Локальная установка

Клонируйте репозиторий и перейдите в него в командной строке:
```sh
git clone https://github.com/MrTepex/foodgram-project-react.git
```
Перейдите в директорию с файлом _Dockerfile_ и запустите сборку образа:
```sh
cd backend && docker build -t <DOCKER_USERNAME>/foodgram:<tag> .
```
Перейдите в директорию с файлом _docker-compose.yaml_:
```sh
cd ../infra
```
Создайте .env файл:
```sh
#.env
SECRET_KEY=<секретный ключ проекта django>
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
```
Запустите контейнеры:
```sh
docker-compose up -d --build
```
После успешного запуска контейнеров выполните миграции в проекте:
```sh
docker-compose exec backend python manage.py makemigrations
```
```sh
docker-compose exec backend python manage.py migrate
```
Создайте суперпользователя:
```sh
docker-compose exec backend python manage.py createsuperuser
```
Соберите статику:
```sh
docker-compose exec backend python manage.py collectstatic --no-input
```
Наполните БД заготовленными данными ингредиентов:
```sh
docker-compose exec backend python manage.py fill_db_with_ingredients
```

Создайте дамп (резервную копию) базы данных:
```sh
docker-compose exec backend python manage.py dumpdata > fixtures.json
```
Для остановки контейнеров и удаления всех зависимостей воспользуйтесь командой:
```sh
docker-compose down -v
```

### Автор
- [Mikhail Terekhov](https://github.com/MrTepex)