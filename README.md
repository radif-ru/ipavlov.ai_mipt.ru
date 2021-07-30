# Запуск проекта
## (тестировалось на Docker Toolbox под Windows, на Linux возможно понадобится выдать права на исполнение файлов entrypoint.sh!)
## После запуска доступ на локальной машине по адресу и порту: http://127.0.0.1:3333
## При запуске `production`-версии отключается режим дебага, код грузится, только если проходит проверку на flake8, работа в режиме пользователя, а не root

### Запуск dev версии:
#### 1. Создать образ и запустить контейнер в фоне:
> docker-compose  up -d --build 
#### 2. Выполнить миграции, создать суперпользователя, создать группы:
> docker-compose exec web python manage.py add_groups


### Запуск prod версии:
#### 1. Создать образ и запустить контейнер в фоне:
> docker-compose -f docker-compose.prod.yml  up -d --build 
#### 2. Собрать миграции:
> docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations
#### 3. Выполнить миграции
> docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
#### 4. Сборка стандартных и подготовленных статических файлов 
> docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic
#### 5. Создать суперпользователя
> docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
#### 5. Создать группы
> docker-compose -f docker-compose.prod.yml exec web python manage.py add_groups

 При запуске `python manage.py add_groups` создаются группы: пациент, врач, администратор 
 Если суперпользователя предварительно не создать вручную, то выполняются миграции, 
 генерируется суперпользователь `admin`. Пароль у админа `medicalqwerty`.

