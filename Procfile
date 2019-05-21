web: gunicorn start:app
worker: celery worker -A celery_worker.celery --beat --loglevel=info
heroku ps:scale web=1
heroku ps:scale worker=1