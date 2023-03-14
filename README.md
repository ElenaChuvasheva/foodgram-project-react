# Проект Foodgram

## Описание  
Пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.  
Проект постоянно дополняется.

## Дополнения
### backend
* В админке настроены различные уровни доступа для суперюзера и админа.  
### frontend
* Исправлена ссылка в футере, ведущая на главную страницу

## Технологии
Python, Django Rest Framework, Djoser, Docker, PostgreSQL

## Локальный запуск проекта  
Для запуска подойдёт Docker 20.10.21, Docker Compose 2.12.2.  
Клонируйте репозиторий:  
```
git clone git@github.com:ElenaChuvasheva/foodgram-project-react.git
```
Перейдите в папку foodgram-project-react/infra/:
```
cd foodgram-project-react/infra/
```
Создайте в этой папке файл .env с переменными окружения для работы с базой данных, значения даны для примера:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=m$&m+5lb%q@ehwkq6tz#0)u8&xkm&3^u!+o9u5zqr-iic^pol7
```
В папке foodgram-project-react/infra/ запустите команду:
```
docker-compose up
```
Образы для контейнеров frontend и backend будут загружены c Docker Hub. Если необходимо собрать их именно по коду на локальном компьютере, измените текст файла docker-compose.yml в части, описывающей frontend и backend:
```
  frontend:    
    build:
      context: ../frontend
      dockerfile: Dockerfile
    volumes:
      - ../frontend/:/app/result_build/

  backend:    
    build:
      context: ../backend
      dockerfile: Dockerfile
    volumes:
      - media_backend_value:/app/media/
      - static_backend_value:/app/static/
    env_file:
      - ./.env
    depends_on:
      - db

```
Внутри контейнера выполните команды сборки статики и применения миграций:
```
docker-compose exec backend python manage.py collectstatic
docker-compose exec backend python manage.py migrate
```
Зайдите в shell:
```
docker-compose exec backend python manage.py shell
```
Выполните скрипт:
```
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
```
При необходимости выполните загрузку фикстур:
```
docker-compose exec backend python manage.py loaddata fixtures.json
```
В тестовой базе данных суперпользователь admin, email a@a.ru, пароль admin.  
Сайт откроется по адресу localhost.

## Примеры запросов
/recipes - главная страница с рецептами  
/signin - вход на сайт  
/api/docs - документация API  
/for_staff_only - админка  

![foodgram_deploy CI](https://github.com/ElenaChuvasheva/foodgram-project-react/actions/workflows/foodgram_deploy.yml/badge.svg)

Адрес сайта foodgram.gotdns.ch  
Адрес админки foodgram.gotdns.ch/for_staff_only/  
Суперпользователь admin, a@a.ru, пароль admin  

## Планы развития
* Комментарии к рецептам
* Личные сообщения
* Регистрация и восстановление пароля с проверкой по емейл

## Авторы проекта
- [Елена Чувашева](https://github.com/ElenaChuvasheva) - бэкенд
- Яндекс.Практикум - фронтенд
