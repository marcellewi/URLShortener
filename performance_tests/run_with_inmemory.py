import subprocess
import threading
import time
from contextlib import contextmanager

import uvicorn
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database.db import get_session
from app.main import app

# Create in-memory SQLite database
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
SQLModel.metadata.create_all(engine)

# Create a test session
test_session = Session(engine)


# Override get_session with our test session
def get_test_session():
    return test_session


app.dependency_overrides[get_session] = get_test_session


# Start server in a separate thread with in-memory database
def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


@contextmanager
def run_server_with_inmemory():
    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    print("Starting server with in-memory SQLite database...")
    time.sleep(2)  # Give the server time to start

    try:
        yield
    finally:
        # Clean up
        app.dependency_overrides.clear()
        print("Cleaned up in-memory database")


if __name__ == "__main__":
    # First make sure k6 is installed
    print("Checking if k6 is installed...")
    try:
        subprocess.run(["k6", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("k6 is not installed or not in the PATH. Please install k6 first.")
        print("Visit: https://k6.io/docs/get-started/installation/")
        exit(1)

    # Start server with in-memory database and run the k6 test
    with run_server_with_inmemory():
        print("Running k6 performance test with in-memory database...")
        k6_command = ["k6", "run", "performance_tests/simple_test.js"]
        subprocess.run(k6_command)

    print("Performance test completed.")
