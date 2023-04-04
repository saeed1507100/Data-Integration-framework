docker compose down
docker buildx build . --tag extended_airflow:latest --platform linux/amd64
docker compose up airflow-init
docker compose up