from fastapi import FastAPI
from library_api.routers import books, authors, genres
from library_api import models
from library_api.db import engine


app = FastAPI(
    title="Библиотека API",
    description="Комплексный API для управления книгами в библиотеке с CRUD-операциями, фильтрацией, сортировкой и пагинацией",
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
        "message": "Библиотека",
        "docs": "/docs",
        "redoc": "/redoc"
    }