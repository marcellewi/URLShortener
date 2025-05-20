# URL Shortener

A scalable URL shortening service built with FastAPI, SQLModel, and Alembic.

## Features

- Create shortened URLs from long URLs
- Redirect from short URLs to original URLs
- Get, update, and delete short URLs
- List all URLs with pagination
- Soft delete functionality to keep records while marking them as deleted
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

1. Run migrations to set up the database:
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

## Testing with Postman

Here's a step-by-step guide to test all endpoints using Postman:

### 1. Create a shortened URL
- Method: POST
- URL: `http://localhost:8000/api/urls/shorten`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
  ```json
  {
    "original_url": "https://example.com/very/long/path"
  }
  ```
- Expected response: Status 201 with the shortened URL data

### 2. Get all URLs
- Method: GET
- URL: `http://localhost:8000/api/urls`
- Optional query parameters:
  - `skip=0` (starting index)
  - `limit=10` (number of results)
- Expected response: Status 200 with an array of URL details

### 3. Get URL information
- Method: GET
- URL: `http://localhost:8000/api/urls/{short_code}` (replace {short_code} with the code from the previous response)
- Expected response: Status 200 with URL details

### 4. Update the URL
- Method: PUT
- URL: `http://localhost:8000/api/urls/{short_code}` (use the same short code)
- Headers: `Content-Type: application/json`
- Body (raw JSON):
  ```json
  {
    "original_url": "https://example.com/updated/path"
  }
  ```
- Expected response: Status 200 with updated URL details

### 5. Soft delete the URL
- Method: DELETE
- URL: `http://localhost:8000/api/urls/{short_code}` (use the same short code)
- Expected response: Status 200 with URL details showing `is_deleted: true`

### 6. Verify deletion
- Method: GET
- URL: `http://localhost:8000/api/urls/{short_code}` (use the same short code)
- Expected response: Status 404 Not Found

### 7. Check that deleted URLs don't appear in the list
- Method: GET
- URL: `http://localhost:8000/api/urls`
- Expected response: The deleted URL should not be included in the results

## Performance and Scalability

- Efficient database indexes for quick lookups
- Short codes generated with a fixed length of 6 characters
- Random string generation with collision detection
- Soft delete functionality to maintain data history
- Pagination for listing URLs to handle large datasets
- Caching can be added to improve performance further