# Продуктовый помощник Foodgram


### Описание: 
  Это сайт, на котором пользователи будут публиковать свои рецепты, добавлять чужие в избранное и подписываться на публикации других авторов.


### Технологии в проекте:
  Python 3.9, Django 2.2.16, Django REST Framework (DRF), Docker 20.20.18,  
  docker-compose 3.8, nginx:1.21.3-alpine
  

### Последовательность команд при запуске:


#### Подготовка к работе и настройка окуружения проекта
git clone git@github:bluesprogrammer-Python/foodgram-project-react.git  
cd foodgram-project-react/  
python -m venv venv  
source venv/Scripts/./activate  
pip install -r requirements.txt  
cd backend/foodgram/  
python manage.py runserver

#### База данных
База данных с тестовыми данными уже загружена в проект, можно проверить работу проекта на этих данных
или удалить и наполнить своими.  
Сайт - http://158.160.36.165/signin  
Админка - Почта: serg2012@yandex.ru, пароль: 12396  
python manage.py import_csv (запуск скрипта для импорта ингридиетов)

### Автор:
 	Семёнов Сергей (Github - bluesprogrammer-Python)
