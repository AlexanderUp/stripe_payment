# Тестовое задание Stripe Payment API.

Позволяет совершать покупки товаров с платежами через сервис Stripe Payment.

Приложение развернуто и доступно для тестирования по адресу https://alexanderup.pythonanywhere.com

Для тестирования сайта необходима регистрация или вы можете воспользоваться следующими данными для входа:
- Логин: ```leo```
- Пароль: ```qwerty1990```

NB. При использовании логина ```leo``` административная часть сайта будет недоступна, но выможете использовать для покупок учетную запись администратора (смотри примечания).

- Django Модель Item с полями (name, description, price);
- API с двумя методами:
    - ```GET /buy/{id}```;
    - ```GET /item/{id}```.
- Доступен выбор одного или нескольких товаров, их добавление в корзину, проведение оплаты на общую сумму добавленных в корзину товаров;
- Использованы переменные окружения для храниния чувствительной информации;
- Модели доступны в административной части сайта (смотри примечания);
- Реализованы модели Discount, Tax.

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

6. В файле ```.env``` указываем значения необходимых ключей по образцу из файла ```example.env```. Для получения ключей Stripe API обратитесь к документации (https://stripe.com).

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
- python-dotenv 1.0.0

## Примечания

- Для тестирования оплаты товаров используйте следующие номера тестовых банковских карт:
    - Успешная оплата - ```4242 4242 4242 4242```
    - Необходима аутентификация - ```4000 0025 0000 3155```
    - Платеж отклонен - ```4000 0000 0000 9995```

- Модели доступны в административной части сайта. Для демонстрационных целей установлены следующие авторизационные данные:
    - Логин ```admin```
    - Пароль ```qwerty1990```

- В роли БД использована sqlite, потому что pythonanywhere.com не позволяет использовать PostgreSQL на бесплатных аккаунтах.
