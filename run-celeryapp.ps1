$pipenvPath=(pipenv --venv) -join "";
& "$pipenvPath\Scripts\activate";
celery -A wsgi:celery worker -l INFO -P threads;