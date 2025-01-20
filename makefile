APP = restapi

test:
	@flake8 . --exclude .venv
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up

heroku:
	@heroku container:login
	@heroku container:push -a <project> web
	@heroku container:release -a <project> web
	@heroku ps:scale -a <project> web=1