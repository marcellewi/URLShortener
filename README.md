# URL Shortener

A scalable URL shortening service built with FastAPI, SQLModel, and Alembic.

## Features

- Create shortened URLs from long URLs
- Redirect from short URLs to original URLs
- View statistics for a shortened URL (clicks, creation date, etc.)
- Efficient 6-character alphanumeric codes for short URLs
- PostgreSQL database for storage
- SQLModel for unified models between database and API

## Installation

1. Clone the repository
2. Set up your PostgreSQL database
3. Create a `.env` file with the following variables:
   ```
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=url_shortener
   ```
4. Install dependencies with Poetry:
   ```
   poetry install
   ```

## Running the Application

1. Run migrations to set up the database (optional, as SQLModel creates tables on startup):
   ```
   alembic upgrade head
   ```

2. Start the application:
   ```
   python -m app.main
   ```
   
   Or use the startup script:
   ```
   ./startup.sh
   ```

3. The application will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/urls/shorten` - Create a shortened URL
  ```json
  {
    "original_url": "https://example.com/very/long/path"
  }
  ```

- `GET /{short_code}` - Redirect to the original URL

- `GET /{short_code}/stats` - Get statistics for a shortened URL (clicks, creation date, etc.)

- `GET /api/urls/{short_code}/stats` - Alternative endpoint for getting URL statistics

## Performance and Scalability

- Efficient database indexes for quick lookups
- Short codes generated with a fixed length of 6 characters
- Random string generation with collision detection
- Caching can be added to improve performance further