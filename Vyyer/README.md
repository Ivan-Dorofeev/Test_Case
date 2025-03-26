# Решаем reCaptcha и вводим данные на сайте


<img width="50%" alt="image" src="https://github.com/user-attachments/assets/f34bb2d9-8175-4da3-b9e1-e38184b70710">

### Как запустить

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Затем установите зависимости:

```sh
pip install -r req.txt
```
Заполните реальными данными переменные:

    CAPTCHA_API_KEY = ""  # API ключ сервиса reCaptcha
    ZIP_CODE = ""  # Пример почтового индекса
    LICENSE_ID = ""  # Пример номера водительского удостоверения
    DOB = "21/09/1999"  # Пример даты рождения


Запустите скрипт:

```sh
python3 solve_reCaptcha.py
```
