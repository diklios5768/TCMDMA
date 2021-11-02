. $(pipenv --venv)/bin/activate;
celery -A wsgi:celery worker -l INFO;