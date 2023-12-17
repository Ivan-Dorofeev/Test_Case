# Сайт недвижимости

Тестовый сайт на Flask с фильтрацией

<img width="75%" alt="image" src="https://github.com/Ivan-Dorofeev/Test_Case/assets/58893102/06cb4cec-328d-4684-bd6c-ecc1ee6f8233">

### Как запустить

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Затем установите зависимости:

```sh
pip install -r requirements.txt
```

В корне каталога создайте файл `.env` и добавьте в него ссылку на базу данных Postgres:


```sh
DATABASE_URL=<ваша ссылка на базу данных>
```

Запустите сайт:

```sh
python3 site.py
```

### Дополнительно

Файл css расположен тут, если нужны правки стилей:
`/static/css/style.css`

Ссылка на тестовую БД с добавленными объектами недвижимости: 
`postgres://brneimtr:yHY3ao1BLzBOyvkOZ3GfSQi9Z7-WJkGK@ella.db.elephantsql.com/brneimtr`