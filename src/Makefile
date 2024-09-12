
# ### Docker management commands 
 
docker-up: 
	docker compose -p movio_api_service -f dev.yml up --build -d --remove-orphans

docker-down: 
	docker compose -p movio_api_service -f dev.yml down

docker-down-v: 
	docker compose -p movio_api_service -f dev.yml down -v

docker-logs: 
	docker compose -p movio_api_service -f dev.yml logs 

docker-logs-movio: 
	docker compose -p movio_api_service -f dev.yml logs movio-api

docker-restart-movio: 
	docker compose -p movio_api_service -f dev.yml restart movio-api

docker-restart-nginx:
	docker compose -p movio_api_service -f dev.yml restart nginx

docker-restart-worker:
	docker compose -p movio_api_service -f dev.yml restart  movio-celery-worker

docker-exec-movio: 
	docker compose -p movio_api_service -f dev.yml exec movio-api /bin/bash 

docker-check-movio:
	docker compose -p movio_api_service -f dev.yml run --rm movio-api python manage.py check --deploy 

# ## 


# ### Docker Volume and Postgres Database 

docker-exec-pg: 
	docker compose -p movio_api_service -f dev.yml exec postgres /bin/bash 

docker-pgdb: 
	docker compose -p movio_api_service -f dev.yml exec postgres psql --username="$(POSTGRES_USER)" --dbname="$(POSTGRES_DB)" 

# ## 



# ### Services logs commands 

docker-logs-pg: 
	docker compose -p movio_api_service -f dev.yml logs postgres

# ## 



# ### Django Commands

makemigrations: 
	docker compose -p movio_api_service -f dev.yml run --rm movio-api python manage.py makemigrations

migrate: 
	docker compose -p movio_api_service -f dev.yml run --rm movio-api python manage.py migrate

collectstatic: 
	docker compose -p movio_api_service -f dev.yml run --rm movio-api python manage.py collectstatic --no-input --clear 

superuser: 
	docker compose -p movio_api_service -f dev.yml run --rm movio-api python manage.py createsuperuser 

# ## 