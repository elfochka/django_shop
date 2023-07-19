Подключение Postgresql:

1. Скачать и установить PostgreSQL локально
2. Создать базу данных для проекта командой: `createdb store_db`
3. Создать пользователя и дать ему необходимые права командами:  
`CREATE USER store_username WITH PASSWORD '0xA6JtA2cxMdyGxYwc6p'`  
`ALTER USER store_username WITH SUPERUSER`
4. Выполняем миграции в django командой: `python manage.py migrate`