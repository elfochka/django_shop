#### Подключение PostgreSQL к проекту

1. Скачать и установить PostgreSQL локально
2. Создать базу данных для проекта командой:
```sql
CREATE DATABASE store_db;
```
3. Создать пользователя и дать ему необходимые права командами:
```sql
CREATE USER store_username WITH PASSWORD '0xA6JtA2cxMdyGxYwc6p';
ALTER USER store_username WITH SUPERUSER;
```
4. Выполняем миграции в django командой:
```bash
python manage.py migrate
```

## Фикстуры

Файлы с фикстурами находятся в директории `products/fixtures/`, и разбиты по моделям: `products.json`,
`categories.json`,  `tags.json`, `product_images.json`.

### Загрузка данных из фикстур в БД

После миграции БД, выполнить следующую команду из директории проекта:

```bash
python -m manage loaddata products/fixtures/*.json
```

### Загрузка значков для категорий из фикстуры

Для корректного отображения на страницах сайта значков категорий, хранящихся в фикстуре, необходимо скачать и 
распаковать в директорию `uploads/` файл
[uploads.zip](https://gitlab.skillbox.ru/kurator_skillbox/python_django_team28/uploads/2837c4a863d29c74996a8ce5e73e37d7/uploads.zip).