#!/bin/bash

# Reestablece los dashboards en superset

docker exec -it superset_db psql -h localhost -p 5432 -U superset -c "DROP SCHEMA public CASCADE;"
docker exec -it superset_db psql -h localhost -p 5432 -U superset -c "CREATE SCHEMA public;"
docker exec -it superset_db pg_dump superset -U superset > db_backup.sql