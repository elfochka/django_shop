Подключение Postgresql:

1. Устанавливаем СУБД 'sudo apt install postgresql'
2. Подключаемся к СУБД коммандой 'sudo -i -u postgres'
3. Вводим команду 'psql'
4. Создаем пользователя "CREATE USER username WITH PASSWORD 'postgres'"
5. Наделяем пользователя правами суперпользователя командой 'ALTER USER username WITH SUPERUSER'
6. Создаем базу данных для проекта командой 'createdb store_data'
7. Переходим в папку проекта и подключаем зависимости файла requirements.txt командой 'pip install -r requirements'
8. В файле store/settings.py находим подключение к базе данных 
```python
DATABASES={
   'default':{
      'ENGINE':'django.db.backends.sqlite3',
      'NAME':os.path.join(BASE_DIR,'db.sqlite3'),
   }
}
```
и меняем его на 
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'store_data',
        'USER': 'username',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
    }
}
```
9. Выполняем миграции командой 'python manage.py migrate'