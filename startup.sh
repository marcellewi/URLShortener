#!/bin/bash

set -e

if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

echo "Installing dependencies..."
poetry install

echo "Setting up PostgreSQL database..."
if command -v psql &> /dev/null; then    
    if ! psql -lqt | cut -d \| -f 1 | grep -qw url_shortener; then
        echo "Creating database url_shortener..."
        createdb url_shortener || echo "Failed to create database. You may need to create it manually."
    else
        echo "Database url_shortener already exists."
    fi
else
    echo "PostgreSQL client not found. Please ensure the database is created manually."
fi


mkdir -p app/migrations/versions

echo "Running database migrations..."
export PYTHONPATH=$PWD
poetry run alembic upgrade head

echo "Starting FastAPI application..."
poetry run uvicorn app.main:app --reload
