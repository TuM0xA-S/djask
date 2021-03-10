if [ ! -z "$DEV" ]
then
	echo "development server"
	export DJANGO_SETTINGS_MODULE=djask.settings.dev
	./manage.py makemigrations
	./manage.py migrate
	python3 manage.py runserver 0.0.0.0:8000
else
	echo "production server"
	export DJANGO_SETTINGS_MODULE=djask.settings.prod
	./manage.py makemigrations
	./manage.py migrate
	gunicorn -w 2 -b :8000 djask.wsgi
fi
