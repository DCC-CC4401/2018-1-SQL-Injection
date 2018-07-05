# 2018-1-SQL-Injection-T3

##Dependencies 

`pip install`

##Database configuration

create database from models in `inventario_cei`

```
python manage.py makemigrations inventario_cei
python manage.py migrate

```
Clean database data

`python manage.py sqlflush | python manage.py dbshell`

load data

`python manage.py loaddata db.json`
