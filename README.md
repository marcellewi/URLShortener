# URL Shortener Service

A scalable URL shortening service built with FastAPI, SQLModel, and PostgreSQL.

## Architecture Overview

This service is built using a modern tech stack with clean architecture principles:

- **Backend**: FastAPI framework for high-performance API endpoints
- **Database**: PostgreSQL with SQLModel ORM for data persistence
- **Migration**: Alembic for database migrations
- **Containerization**: Docker and Docker Compose for easy deployment
- **Project Structure**:
  - `app/models`: Data models and schemas
  - `app/services`: Business logic and service layer
  - `app/controller`: API route definitions and controllers
  - `app/database`: Database connection and configuration
  - `app/migrations`: Database migration scripts
  - `performance_tests`: k6 performance tests

The application follows a layered architecture separating concerns:
- REST API endpoints in controllers
- Business logic in services
- Data access through models
- PostgreSQL for persistent storage

## Setup and Deployment Instructions

### Prerequisites
- Docker and Docker Compose

### Deployment Steps

1. Clone the repository
   ```
   git clone <repository-url>
   ```

2. Deploy with Docker Compose
   ```
   docker compose up --build
   ```

3. The application will be available at:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. To stop and clean up
   ```
   docker compose down -v
   ```

## API Endpoints

The service provides the following key endpoints:

- `GET /{short_code}` - Redirect to the original URL
- `POST /api/urls/shorten` - Create a shortened URL
- `GET /api/urls` - Get all URLs (with pagination)
- `GET /api/urls/{short_code}` - Get URL information
- `PUT /api/urls/{short_code}` - Update a short URL
- `DELETE /api/urls/{short_code}` - Soft delete a URL
- `GET /api/analytics/urls` - Get most clicked URLs
- `GET /api/analytics/urls/{short_code}` - Get analytics for a specific URL
- `GET /api/analytics/summary` - Get analytics summary

Complete API documentation is available at the Swagger UI endpoint when the service is running.

## Development Setup

For local development without Docker:

1. Set up a PostgreSQL database
2. Configure environment variables in `.env`
3. Install dependencies: `poetry install`
4. Run migrations: `alembic upgrade head`
5. Start the application: `uvicorn app.main:app --reload`

## Performance Testing

The project includes performance tests using [k6](https://k6.io/).

### Prerequisites
- Install k6: https://k6.io/docs/getting-started/installation/

### Running Performance Tests
1. Make sure the application is running
2. Run the test:
   ```
   k6 run performance_tests/simple_test.js
   ```

3. For more options and details, see the [performance_tests/README.md](performance_tests/README.md)

## Assumptions

During development, the following assumptions were made:

1. The service is meant to be self-contained and deployable as a standalone application
2. Short codes are 6-character alphanumeric strings by default
3. Soft deletion is preferred over hard deletion to preserve analytics data
4. PostgreSQL is suitable for the expected scale and performance requirements
5. The service does not implement authentication/authorization (could be added in future iterations)