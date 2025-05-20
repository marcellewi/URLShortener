# URL Shortener

A scalable URL shortening service built with FastAPI, SQLModel, and Alembic.

## Features

- Create shortened URLs from long URLs
- Redirect from short URLs to original URLs
- Get, update, and delete short URLs
- List all URLs with pagination
- Soft delete functionality
- Efficient 6-character alphanumeric codes
- PostgreSQL database with SQLModel ORM

## Running with Docker

1. Clone the repository

2. Start the application with Docker Compose:
   ```
   docker compose up --build
   ```

3. The application will be available at `http://localhost:8000`

4. To stop and remove containers and volumes:
   ```
   docker compose down -v
   ```

## Manual Installation

1. Set up your PostgreSQL database

2. Create a `.env` file with the following variables:
   ```
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=url_shortener
   ```

3. Install dependencies with Poetry:
   ```
   poetry install
   ```

4. Run migrations to set up the database:
   ```
   alembic upgrade head
   ```

5. Start the application:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `GET /{short_code}` - Redirect to the original URL

- `GET /api/urls` - Get all URLs (with pagination)
  - Query parameters:
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum number of records to return (default: 100)

- `POST /api/urls/shorten` - Create a shortened URL
  ```json
  {
    "original_url": "https://example.com/very/long/path"
  }
  ```

- `GET /api/urls/{short_code}` - Get URL information

- `PUT /api/urls/{short_code}` - Update a short URL
  ```json
  {
    "original_url": "https://new-example.com/updated/path"
  }
  ```

- `DELETE /api/urls/{short_code}` - Soft delete a URL

## API Documentation

When the application is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`