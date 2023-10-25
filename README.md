## Добро пожаловать в Фудграм! ##

Это сервис, в котором вы можете: 
- смотреть чужие рецепты
- добавлять свои
- подписываться на любимых пользователей
- добавлять рецепты в избранное, чтобы позже
насладиться приготовлением новых интересных блюд

Так же для зарегистрированных пользователей доступна
возможность скачивать список покупок со списком всех нужных
ингредиентов, чтобы легко и быстро сделать покупки.

Технологии, которые были использованы:
- Python 3.9.6
- Django 3.2.3
- Django Rest Framework 3.12.4
- Djoser 2.2.0

Вы можете насладиться этим сервисом по следующим адресам:
 - https://taskmanagerpro.sytes.net
 - 51.250.96.55:8000

*Данные для захода в админ-панель:*
- *email: admin@ya.ru*
- *password: superuser*

### Чтобы развернуть проект у себя самостоятельно: ###

-Клонировать репозиторий и перейти в него в командной строке:
```git@github.com:Elizabeth-Bell/foodgram-project-react.git ```
-Перейти в директорию с docker-compose
```cd backend```
- Запустить докер
- Выполнить сборку контейнеров
```docker compose up```
- Собрать статику бэкэнда
```docker compose exec backend python manage.py collectstatic```
- Переместить ее в необходимую папку 
```docker compose exec backend cp -r /app/collected_static/. /backend_static/static/  ```
- Выполнить миграции
```docker compose exec backend python manage.py migrate```
