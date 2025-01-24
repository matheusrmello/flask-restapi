APP = restapp-flask

test:
	@echo "Running tests..."
	@black .
	@bandit -r . -x /tests/,/.venv/
	@flake8 . --ignore=E501 --exclude .venv
	@pytest -v --disable-warnings

compose:
	@echo "Running docker compose..."
	@docker compose build
	@docker compose up

setup-dev:
	@echo "Setting up development environment..."
	@kind create cluster --config k8s/config/config.yaml
	@kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
	@kubectl wait --namespace ingress-nginx \
  	--for=condition=ready pod \
  	--selector=app.kubernetes.io/component=controller \
  	--timeout=270s
	@helm upgrade \
		--install \
		--set image.tag=5.0.8 \
		--set auth.rootPassword="root" \
		mongodb k8s/charts/mongodb
	@kubectl wait \
  	--for=condition=ready pod \
  	--selector=app.kubernetes.io/component=mongodb \
  	--timeout=270s

teardown-dev:
	@echo "Tearing down development environment..."
	@kind delete clusters kind

