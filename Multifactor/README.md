# NTLMv2 - проверка логина и пароля

Задача: 
Реализовать проверку логина и пароля пользователя с использованием протокола NTLMv2. 
 

## Требования: 
- использовать две функции, одна клиентская - передает логин и пароль, вторая - серверная - принимает и проверяет. 
- межсетевой обмен, и пр. не требуется, достаточно проверить алгоритм. 
- функции должны быть должным образом оформлены и документированы. 
- язык Python

## Запуск

- Сначала необходимо зайти на сайт [Stripe](https://dashboard.stripe.com/products/) и создать свой аккаунт.

    ```sh
    pip install -r requirements.txt
    ```

 - Создайте базу данных SQLite

    ```sh
    python3 manage.py makemigrations
    ```
    ```sh
    python3 manage.py migrate
    ```
 - Запустите разработческий сервер

