#!/bin/bash

# Make script exit on first error
set -e

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry is not installed. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
echo "Installing dependencies..."
poetry install

# Create PostgreSQL database if it doesn't exist
echo "Setting up PostgreSQL database..."
if command -v psql &> /dev/null; then
    # Check if database exists
    if ! psql -lqt | cut -d \| -f 1 | grep -qw url_shortener; then
        echo "Creating database url_shortener..."
        createdb url_shortener || echo "Failed to create database. You may need to create it manually."
    else
        echo "Database url_shortener already exists."
    fi
else
    echo "PostgreSQL client not found. Please ensure the database is created manually."
fi

# Create migrations/versions directory if it doesn't exist
mkdir -p app/migrations/versions

# Run migrations
echo "Running database migrations..."
export PYTHONPATH=$PWD
poetry run alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI application..."
poetry run uvicorn app.main:app --reload
