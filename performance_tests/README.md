# Performance Testing with k6

This directory contains a simple performance test for the URL Shortener API using [k6](https://k6.io/).

## Prerequisites

- Install k6: https://k6.io/docs/getting-started/installation/

## Available Test

`simple_test.js` - Tests the URL shortening endpoint

## Running Tests

### Standard Method

Make sure the URL Shortener application is running (using Docker Compose or directly) before running tests.

```bash
k6 run performance_tests/simple_test.js
```

### Using In-Memory SQLite Database

You can run the test with an in-memory SQLite database to avoid affecting your production database:

```bash
poetry run python performance_tests/run_with_inmemory.py
```

This script:
1. Sets up an in-memory SQLite database
2. Starts a server using this database
3. Runs the simple_test.js with k6
4. Cleans up automatically when done

### Custom Options

To run the test with custom options:

```bash
k6 run --vus 20 --duration 60s performance_tests/simple_test.js
```

## Test Result Interpretation

After running a test, k6 will display:

- **Data sent/received**: How much data was transferred
- **Response time**: Min, max, average, and median response times
- **Request rate**: Requests per second 
- **Success rate**: Percentage of successful responses
- **Checks**: Results of any checks defined in the test

## Modifying Tests

You can modify test parameters by:

1. Editing the options in the test file
2. Using command-line flags when running k6
