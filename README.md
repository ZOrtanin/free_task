# My Django React App

This project consists of a Django backend and a React frontend, all containerized using Docker.

## Requirements

- Docker
- Docker Compose

## Установка

1. Клонируем репазиторий:
```bash
git clone https://github.com/ZOrtanin/free_task.git
cd free_task
```

2. Собираем и запускаем проект в докере:
```bash
docker-compose up --build
```

3. Заходим в консоль free_task_api 
```bash
docker exec -it free_task_api bash
```

4. Делаем миграции
```bash
python manage.py makemigrations
```

5. Запускаем миграции
```bash
python manage.py migrate
```

6. Бэкенд http://localhost:8000
7. Фронтенд http://localhost:80
