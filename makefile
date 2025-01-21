APP = restapp-flask

test:
	@flake8 . --ignore=E501 --exclude .venv
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up

heroku:
	@heroku container:login
	@heroku container:push -a $(APP) web
	@heroku container:release -a $(APP) web
	@heroku ps:scale -a $(APP) web=1