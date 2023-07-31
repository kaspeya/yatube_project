# Социальная сеть
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com/)
[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?style=flat-square&logo=SQLite&logoColor=ffffff&color=043A6B)](https://www.sqlite.org/)
[![pytest](https://img.shields.io/badge/-pytest-464646?style=flat-square&logo=pytest&logoColor=ffffff&color=043A6B)](https://docs.pytest.org/en/6.2.x/)
[![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=flat-square&logo=bootstrap&logoColor=ffffff&color=043A6B)](https://getbootstrap.com/)

## Описание проекта
Веб-приложение на Django, платформа для блогов, сайт разработан по классической MVT архитектуре. Использована пагинация постов и кэширование. Регистрация реализована с верификацией данных, сменой и восстановлением пароля через почту.

## Запуск проекта
- Клонируйте репозиторий и перейдите в папку проекта:
```
git clone git@github.com:kaspeya/yatube_project.git
```
- Установите и активируйте виртуальное окружение:
```bash
python -m venv venv
```
```bash
source venv/Scripts/activate
```
- Установите зависимости из файла requirements.txt:
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

- Запустить проект
```bash
python manage.py runserver
```

Автор: [Елизавета Шалаева](https://github.com/kaspeya)
