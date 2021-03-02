tests:
	docker-compose up -d
	-docker-compose run web python manage.py migrate
	docker-compose run web python manage.py migrate
	docker-compose run web python manage.py test
