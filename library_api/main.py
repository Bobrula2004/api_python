from fastapi import FastAPI
from library_api.routers import books, authors, genres
from library_api import models
from library_api.db import engine


app = FastAPI(
    title="Library Management API",
    description="A comprehensive API for managing books in a library with CRUD operations, filtering, sorting and pagination",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Library Management API",
        "docs": "/docs",
        "redoc": "/redoc"
    }