# Методы API
> Создать пациента или врача с общими данными (ФИО, пол, дата рождения), 
> установить группы пользователя. Входные данные: id пользователя. 
> Необходимые права: администратор. `/api/user/create`

> Изменить данные пациента или врача. Входные данные: id пользователя. 
> Необходимые права: администратор. `/api/user/update/<int:pk>`

> Заблокировать пациента или врача. Входные данные: id пользователя. 
> Необходимые права: администратор. `/api/user/blocking/<int:pk>`

> Получение свободных слотов у врача в будущем. Входные данные: id врача. 
> Выходные данные: id слота, время начали и время окончания слота. 
> Необходимые права: любой авторизованный пользователь. `/api/doctor/slots/get/<int:pk>`

> Возможность записи на приём к врачу (заполнение слота). 
> Входные данные: id слота. ID клиента узнать по токену. 
> Необходимые права: пациент. Обратите внимание, что надо проверять, свободен ли слот. 
> Если да, то выдавать ошибку. `/api/doctor/appointment/<int:pk>`

> Возможность отмены записи на приём. 
> Необходимые права: пациент. `/api/doctor/appointment/undo/1`

> Получение статистических данных: сколько записей на какой день. 
> Пример: {“day”: “2021-07-19”, “count”: 10, “day”: “2021-07-20”: “count”: 5. 
> Крайне желательно использовать группировать данные при запросе к БД. 
> Перебор всех объектов из БД в цикле for – не лучшее решение. `/api/doctor/entries/all`

> Метод авторизации. Входные данные: логин и пароль. 
> Выходные данные: токен (необязательно JWT). `/api/token`

# Запуск Celery
### Автоматическая генерация слотов для всех врачей на неделю вперёд, происходит каждые 66 секунд
#### Чтобы сгенерировались слоты нужно добавить пользователя в группу "врач" и в таблице "Рабочее время врачей" создать хотя бы 1 рабочий день в неделю
> docker-compose exec web celery -A hospital beat

> docker-compose exec web celery -A hospital worker -l INFO --pool=gevent --concurrency=333

# Тестирование проекта
> Выполнить команду `docker-compose exec web pytest` в корне Django проекта

# Запуск проекта
> (Тестировалось на Docker Toolbox под Windows, на Linux возможно понадобится выдать права на исполнение файлов entrypoint.sh!)
>
> После запуска доступ на локальной машине по адресу и порту: http://127.0.0.1:3333
>
> При запуске `production`-версии отключается режим дебага, код грузится, только если проходит проверку на flake8, работа в режиме пользователя, а не root

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
#### 6. Создать группы. `2-5` можно пропустить - сразу запустить этот пункт
> docker-compose -f docker-compose.prod.yml exec web python manage.py add_groups

 При запуске `python manage.py add_groups` создаются группы: пациент, врач, администратор. 
 Если суперпользователя предварительно не создать вручную, то выполняются миграции, 
 генерируется суперпользователь `admin`. Пароль у админа `medicalqwerty`.

# Задание

Разработать приложение для управления потоками людей в
медицинском учреждении. В системе есть три группы пользователей:
пациенты, врачи и администраторы. За основу взять дефолтную таблицу User
и расширить необходимыми полями.

### У любого пользователя есть:
- ФИО
- Пол
- Дата рождения
- Группы, в которых он состоит (пациент, врач, администратор)
<br>У врача дополнительно задаётся:
- Время работы на каждый день недели (пн, вт, ср, чт, пт, сб, вс)
Какие-то дни могут быть пустыми (суббота и воскресение,
например).
- Количество дней, на которое генерируются слоты для записи на
приём (по умолчанию, на 7 дней вперёд).
- Также для врачей должна быть возможность задать отпуск или
перерыв в работе на обед. Формально, это диапазон datetime.
Для этого промежутка времени генерировать слоты не нужно!
- Время обслуживания у конкретного врача = длины слота.
Например, 20 минут.
<br>К примеру, у врача рабочий день начинается в 11:00 и
заканчивается в 13:00. Время обслуживания 20 минут. Тогда
необходимо сгенерировать 6 слотов: 11:00-11:20, 11:20-11:40, 11:40-
12:00, 12:00-12:20, 12:20-12:40, 12:40-13:00. Генерация должна быть
автоматической через celery.

### Для ускорения разработки уточню поля Timetable:
- id
- doctor – врач, внешний ключ на расширенную модель
пользователя
- client – пациент, внешний ключ на расширенную модель
пользователя
- start_time – дата и время начала слота
- stop_time – дата и время окончания слота

### Необходимые методы API:
- Создать пациента или врача с общими данными (ФИО, пол, дата
рождения), установить группы пользователя. Входные данные: id
пользователя. Необходимые права: администратор.
- Изменить данные пациента или врача. Входные данные: id
пользователя. Необходимые права: администратор.
- Заблокировать пациента или врача. Входные данные: id
пользователя. Необходимые права: администратор.
- Получение свободных слотов у врача в будущем. Входные
данные: id врача. Выходные данные: id слота, время начали и
время окончания слота. Необходимые права: любой
авторизованный пользователь.
- Возможность записи на приём к врачу (заполнение слота).
Входные данные: id слота. ID клиента узнать по токену.
Необходимые права: пациент. Обратите внимание, что надо
проверять, свободен ли слот. Если да, то выдавать ошибку.
- Возможность отмены записи на приём. Необходимые права:
пациент.
- Получение статистических данных: сколько записей на какой
день. Пример: {“day”: “2021-07-19”, “count”: 10, “day”: “2021-07-
20”: “count”: 5 Крайне желательно использовать группировать
данные при запросе к БД. Перебор всех объектов из БД в цикле
for – не лучшее решение.
-  Метод авторизации. Входные данные: логин и пароль. Выходные
данные: токен (необязательно JWT).

### Требования к стеку технологий:
- Python 3.6 и выше
- Django 2.1 и выше & DjangoRestFramework
- PostgreSQL
- Celery
- Pytest
- Docker
- Docker-compose

### Итого:
- Расширить таблицу User
- Разработать модель Timetable для слотов
- Разработать автогенерацию слотов
- Разработать 8 методов API. Реализовать можно в несколько строк
кода: задать queryset, serializers. проверку прав.
- Написать несколько юнит-тестов к разработанным функциям
- Обернуть решение в docker-compose