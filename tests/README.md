# URL Shortener - Tests

This directory contains unit and integration tests for the URL Shortener application.

## Running Tests

To run all tests:

```bash
poetry run pytest
```

## Test Coverage

The tests cover the following functionality:

1. Basic application health check
2. URL shortening functionality
3. URL retrieval by short code
4. Custom alias functionality

These tests use a SQLite in-memory database for testing, which is isolated from the production database. 