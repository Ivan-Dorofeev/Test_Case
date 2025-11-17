# Audio Service API

## Описание
Сервис для загрузки и управления аудиофайлами с авторизацией через Яндекс

## Установка
1. Заполните `.env`
2. Запустите сервисы: `docker-compose up -d`
3. Примените миграции: `docker-compose exec app alembic upgrade head`

## API Endpoints
- `POST /auth/yandex` - Авторизация через Яндекс
- `POST /audio` - Загрузка аудиофайла
- `GET /audio` - Получение списка файлов