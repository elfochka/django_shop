# Интернет-магазин Megano

## Настройка и запуск проекта

### Подключение PostgreSQL

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

### Настройка переменных окружения

Скопировать содержимое файла `env.template` в файл `.env` и указать необходимые значения переменных окружения, например:
```bash
SECRET_KEY=secret_key
DEBUG=True
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### Фикстуры

Файлы с фикстурами находятся в директориях `products/fixtures/`, `orders/fixtures/`, и разбиты по моделям: `products.
json`, `categories.json`,  `tags.json`, `product_images.json`, `product_banners.json`, `seller.json`, 
`product_position.json`, `deliveries.json`.

#### Загрузка данных из фикстур в БД

После миграции БД, выполнить следующую команду из директории проекта:

```bash
python -m manage loaddata products/fixtures/*.json
python -m manage loaddata orders/fixtures/*.json
```

#### Загрузка значков для категорий из фикстуры

Для корректного отображения на страницах сайта значков категорий, хранящихся в фикстуре, необходимо скачать и 
распаковать в директорию `uploads/` файл
[uploads.zip](https://gitlab.skillbox.ru/kurator_skillbox/python_django_team28/uploads/5e1a277c4a99972bffcc2dfffca4c72c/uploads.zip)
### Запуск в режиме разработки и отладки

Для запуска проекта необходимо запустить базу данных PostgreSQL, активировать виртуальное окружение, при необходимости, 
установить недостающие 
библиотеки, и выполнить команду Django `runserver`. Например:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python -m manage runserver
```

## Кастомные команды `manage.py`

### Выбор случайного "Предложения дня" – `random_chosen_product`

Для реализации выбора случайного товара, отмеченного как "Ограниченный тираж" (поле `Product.is_limited == True`),
разработана дополнительная команда `random_chosen_product`. Она выбирает случайный товар с флагом `is_limited = True` 
как "Предложение дня" (`is_chosen = True`) для отображения в блоке "Ограниченное предложение" на главной странице. 
Текущему товару "Предложение дня" (если он имеется) устанавливается `is_chosen = False`.

Пример выполнения команды (в активированном виртуальном окружении и с запущенной в фоне БД):

```bash
python -m manage random_chosen_product
```

Для запуска команды ежесуточно в 23:59:00 (таймер обратного отсчёта на главное странице установлен на это время), при 
деплое приложения на сервере предлагается использовать системный сервис Linux `cron`.

Пример настройки выполнения команды по расписанию:

```bash
# Открыть crontab для редактирования:
crontab -e 
# Задача в crontab будет выглядеть примерно так (сама команда будет зависеть от того, как будем деплоить):
59 23 * * * python -m manage random_chosen_product
# Проверить сохранение задачи:
crontab -l
```

## Используемые библиотеки

- [django-allauth](https://github.com/pennersr/django-allauth) - для регистрации и аутентификации пользователей. 
  Библиотека обладает [большим функционалом](https://github.com/pennersr/django-allauth#features), доступным "из 
  коробки". Для подстановки ссылок на страницы входа, регистрации, выхода в шаблонах, необходимо использовать 
  соответственно `{% url 'account_login' %}`, `{% url 'account_signup' %}`, `{% url 'account_logout' %}`. Шаблоны 
  страниц входа и регистрации находятся в `templates/account/`.

### Подключение celery 

1. Скачать и установить Celery
2. Установить брокер сообщений RabbitMQ
3. [Настроить брокер сообщений](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/rabbitmq.html)


 Команды для linux:
```bash
sudo rabbitmqctl add_user myuser mypassword
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_user_tags myuser mytag
sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
```
Заменить myuser, mypassword и myvhost на свои значения