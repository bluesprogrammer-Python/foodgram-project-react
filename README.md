# Продуктовый помощник Foodgram


### Описание
Это сайт, на котором пользователи будут публиковать свои рецепты, добавлять чужие в избранное и подписываться на публикации других авторов.

### Технологии в проекте:
  Python 3.9, Django 2.2.16, Django REST Framework (DRF), Docker 20.20.18,
  docker-compose 3.8, nginx:1.21.3-alpine

### Инструкция по запуску
1. Установите и активируйте виртуальное окружение.
```bash
python -m venv venv
source venv/Scripts/./activate
```
2. Обновите менеджер пакетов pip и установите зависимости.
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
3. Запуск проекта.
```bash
python manage.py runserver
```

### База данных
База данных с тестовыми данными уже загружена в проект, можно проверить работу проекта на этих данных
или удалить и наполнить своими.
Админка http://127.0.0.1:8000/admin/ - Почта: sasha2012@mail.ru, пароль: 12396
python manage.py import_csv (запуск скрипта для импорта ингридиетов)


### Автор:
Семёнов Сергей (Github - bluesprogrammer-Python, telegram - seregabrat9)
