APP = restapp-flask

test:
	@echo "Running tests..."
	@black .
	@bandit -r . -x /tests/,/.venv/
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