./manage.py makemigrations
./manage.py migrate
gunicorn -w 2 -b :8000 djask.wsgi
