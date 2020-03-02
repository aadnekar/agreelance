#---- DOCKER INSTALL COMMANDS ----#

start:##@ Start the application
	docker-compose up

start_bg:##@Start the application in the background (detached from terminal)
	docker-compose up -d

down:##@Stop the application
	docker-compose down

loaddata: ##@Add Initial data to database
	docker-compose run application python manage.py loaddata seed.json
	@echo "Initial data added to database successfully"

#---- END DOCKER INSTALL COMMANDS ----#

#---- START DJANGO COMMANDS ----#

migrate: ##@Perform a migration to database
	docker-compose run application python manage.py migrate
	@echo "Migrate completed successfully"

makemigrations: ##@Docker Set up migration files
	docker-compose run application python manage.py makemigrations
	@echo "Migrations completed successfully"

force-makemigrations: ##@Docker Forcibly perform makemigrations on the separate apps
	$(foreach app,$(filter-out __pycache__ common, $(APPDIR)),docker-compose run application python manage.py makemigrations ($(app) &))
	@echo "Migrations completed successfully"



#---- END DJANGO COMMANDS ----#

#----- TEST ENVIRONMENT COMMANDS ----#

test: ##@Run test
	docker-compose run application coverage run -m pytest

lint: ##@Run linter
	docker-compose run application flake8

test_and_lint: ##@Run Linter and Tests
	make test
	make lint

coverage_report:
	docker-compose run application coverage html

clean_start: ##@Delete docker images and re-apply and start the application
	docker-compose down -v
	docker-compose build
	make makemigrations
	make migrate
	make start

clean_start_bg: ##@Delete docker images and re-apply, start application in the background
	docker-compose down -v
	docker-compose build
	make makemigrations
	make migrate
	make start_bg

#----- END TEST ENVIRONMENT COMMANDS ----#
