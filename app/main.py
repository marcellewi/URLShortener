from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controller.api import api_router

app = FastAPI(
    title="URL Shortener",
    description="A URL Shortener application with SQLAlchemy and Alembic",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the URL Shortener application"}


app.include_router(api_router, prefix="/api")
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
