# Проект Foodgram

## Описание  
Пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
В админке настроены различные уровни доступа для суперюзера и админа.

## Локальный запуск проекта  
Для локального запуска подойдёт Docker 20.10.21, Docker Compose 2.12.2.
Клонируйте репозиторий:  
```
git clone git@github.com:ElenaChuvasheva/foodgram-project-react.git
```
Перейдите в папку foodgram-project-react/infra/:
```
cd foodgram-project-react/infra/
```
Создайте в этой папке файл .env с переменными окружения для работы с базой данных:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
В папке foodgram-project-react/infra/ запустите команду:
```
docker-compose up
```


![foodgram_deploy CI](https://github.com/ElenaChuvasheva/foodgram-project-react/actions/workflows/foodgram_deploy.yml/badge.svg)

IP сервера 158.160.5.175  
Адрес админки for_staff_only/  
Суперпользователь admin, a@a.ru, пароль admin  
