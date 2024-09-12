#!/bin/bash

set -e

# cresting the custom user and database

psql -v ON_ERROR_STOP=1 --username postgres --dbname postgres <<-EOSQL
    CREATE USER "$POSTGRES_USER" WITH PASSWORD "$POSTGRES_PASSWORD";
    CREATE DATABASE "$POSTGRES_DB";
    GRANT ALL PRIVILEGES ON DATABASE "$POSTGRES_DB" TO "$POSTGRES_USER";
EOSQL