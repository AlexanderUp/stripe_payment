Запуск приложения в режиме отладки:

1. Создаем директорию 'payment':

    mkdir payment

2. Клонируем репозиторий:

    git clone git@github.com:AlexanderUp/stripe_payment.git

3. Настраиваем виртуальное окружение:

    python3 -m pip venv venv

6. Активируем виртуальное окружение:

    source venv/bin/activate

5. Устанавливаем зависимости:

    python3 -m pip install -r requirements.txt

6. Переходим в папку проекта:

    cd dj_payment

7. Создаем и применяем миграции БД:

    python3 manage.py makemigrations

    python3 manage.py migrate

8. Создаем суперпользователя, следуем инструкциям из терминала:

    python3 manage.py createsuperuser

9. Запускаем отладочный сервер:

    python3 manage.py runserver
