# Тестовое задание Stripe Payment API.

## Описание тестового задания.

Смотри файл ```TASK_DESCRIPTION.md```.

## Запуск приложения в режиме отладки.

1. Клонируем репозиторий:

    ```git clone https://github.com/AlexanderUp/stripe_payment.git```

2. Настраиваем виртуальное окружение:

    ```python3 -m pip venv venv```

3. Активируем виртуальное окружение:

    ```source venv/bin/activate```

4. Устанавливаем зависимости.

- Для запуска приложения на рабочем сервере:

    ```python3 -m pip install -r requirements/requirements_base.txt```

- Для запуска приложения при разработке (установка линтеров, etc.):

    ```python3 -m pip install -r requirements/requirements_dev.txt```

5. Переходим в папку ```dj_payment``` (расположенную внутри одноименной папки).

    ```cd dj_payment/dj_payment```

6. В файле ```.env``` указываем значения необходимых ключей по образцу из файла ```example.env```. Для получения ключей Stripe API обратитесь к документации.

7. Переходим в папку проекта:

    ```cd ..```

8. Создаем и применяем миграции БД:

    ```python3 manage.py makemigrations```

    ```python3 manage.py migrate```

9. Создаем суперпользователя для доступа в административную часть сайта, следуем инструкциям из терминала:

    ```python3 manage.py createsuperuser```

10. Запускаем отладочный сервер:

    ```python3 manage.py runserver```


## Использованные технологии

- Python 3.12
- Django 4.2.7
- Stripe 7.6.0
