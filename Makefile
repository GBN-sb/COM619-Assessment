init_db:
	@echo "Initializing database..."
	@bash scripts/init-couchdb.sh

teardown_db:
	@echo "Tearing down database..."
	@bash scripts/teardown-couchdb.sh