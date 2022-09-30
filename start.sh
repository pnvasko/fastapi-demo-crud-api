#!/usr/bin/env bash

export ENVIRONMENT=LOCAL
export DB_POSTGRES_HOST=localhost
export DB_POSTGRES_USER=admin
export DB_POSTGRESS_PASSWORD=secret
export DB_POSTGRES_PORT=5432
export DB_POSTGRES_DATABASE=crud-sample

uvicorn app.main:app --host 0.0.0.0 --port 8000
