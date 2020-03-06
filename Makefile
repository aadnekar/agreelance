#---- DOCKER INSTALL COMMANDS ----#

build: ##@ Build docker
	docker-compose build

start:##@ Start the application
	docker-compose up

start-bg:##@Start the application in the background (detached from terminal)
	docker-compose up -d

down:##@Stop the application
	docker-compose down

loaddata: ##@Add Initial data to database
	docker-compose run application python manage.py loaddata seed.json
	@echo "Initial data added to database successfully"

clean-start: ##@Delete docker images and re-apply and start the application
	docker-compose down -v
	docker-compose build
	make makemigrations
	make migrate
	make start

clean-start_bg: ##@Delete docker images and re-apply, start application in the background
	docker-compose down -v
	docker-compose build
	make makemigrations
	make migrate
	make start_bg

clean-install: ##@Delete the current database and install everything again
	docker-compose run application python manage.py flush --no-input
	docker-compose down -v
	docker-compose build
	make makemigrations
	make migrate
	make loaddata
	make start

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
	docker-compose run application pytest

test-mark: ##@Run tests that are marked with mark={mark}
	docker-compose run application pytest -v -m ${mark}
lint: ##@Run linter
	docker-compose run application flake8

test-and-lint: ##@Run Linter and Tests
	make test
	make lint

pytest-coverage: ##@Run pytest and generate test report in xml
	docker-compose run application pytest --junitxml=test-results/junit.xml

test-coverage:##@Run Coverage to optain coverage report
	docker-compose run application coverage run -m pytest
	docker-compose run application coverage html

#----- END TEST ENVIRONMENT COMMANDS ----#

#----- AUTO FORMATTING ENVIRONMENT COMMANDS ----#

auto-format:##@Run black auto formatting on all files in the repository
	docker-compose run application black .

#----- END AUTO FORMATTING ENVIRONMENT COMMANDS ----#


