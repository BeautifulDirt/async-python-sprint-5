lint:
	docker-compose up files_storage -d
	-docker exec -it files_storage python -m flake8 --max-line-length 120 src
	docker-compose down --remove-orphans

unittest:
	docker-compose up files_storage -d
	-docker exec -it files_storage pytest -ra
	docker-compose down --remove-orphans

prepare:
	make lint
	make test

build:
	docker build . -t files_storage

server_up:
	docker-compose up -d nginx

server_down:
	docker-compose down --remove-orphans
	
msg ?= "01_initial_db"
revision:
	docker-compose up files_storage -d
	docker exec -it files_storage alembic revision --autogenerate -m $(msg)
	docker-compose down --remove-orphans

upgrade_rev ?= head
migration:
	docker-compose up files_storage -d
	docker exec -it files_storage alembic upgrade $(upgrade_rev)
	docker-compose down --remove-orphans

downgrade_rev ?= base
rollback_migration:
	docker-compose up files_storage -d
	docker exec -it files_storage alembic downgrade $(downgrade_rev)
	docker-compose down --remove-orphans
