# praktikum_new_diplom


![example workflow](https://github.com/IrinaFinatova/foodgram-project-react/actions/workflows/main.yml/badge.svg?event=push)


Проект Foodgram создает вашу он-лайн кулинарную книгу.
Вы можете создавать свои рецепты, обмениваться рецептами с другими участниками проекта.
Огромная база всевозможных ингредиентов и 
подбор рецептов блюд для завтрака, обеда, ужина.
Вы можете заранее запланировать приготовление блюд и скачать список нужных ингредиентов для покупки.

### Ссылка на развернутый проект

http://51.250.78.9/
вход в админку: логин admin@admin.ru
                пароль admin

### Использованные технологии:

Python 3.7
Django REST Framework 3.12
DRF Simple JWT 4.7
Postgres

### Запуск проекта

Перейдите в папку проекта и выполните команду:

docker-compose up -d --build

### При первом запуске для функционирования проекта выполните команды:

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

docker-compose exec web python manage.py collectstatic --no-input

### Заполните базу ингредиентами блюд

docker-compose exec web python manage.py load_data

### Шаблон файла .env с переменными окружения для работы с БД:

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql

DB_NAME=postgres # имя базы данных

POSTGRES_USER=postgres # логин для подключения к базе данных

POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)

DB_HOST=db # название сервиса (контейнера)

DB_PORT=5432 # порт для подключения к БД

SECRET_KEY = xxxxxxxxxxxxxxxxxxxx
