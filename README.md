# Социальная сеть
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?style=flat&logo=Pydantic&logoColor=ffffff&color=043A6B)](https://docs.pydantic.dev/)

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
