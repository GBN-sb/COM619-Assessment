init_db:
	@echo "Initializing database..."
	@bash scripts/init-couchdb.sh

teardown_db:
	@echo "Tearing down database..."
	@bash scripts/teardown-couchdb.sh

test:
	@pytest --cov

lint:
	@ruff check app/

check:
	@pip-audit
	