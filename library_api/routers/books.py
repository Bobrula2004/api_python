from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from library_api import models, schemas
from library_api.db import get_db

router = APIRouter(prefix="/api/v1/books", tags=["books"])


@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # Проверяем есть ли такой автор и жанр
    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    genre = db.query(models.Genre).filter(models.Genre.id == book.genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")

    # Проверяем индификатор ISBN
    if book.isbn:
        existing_book = db.query(models.Book).filter(models.Book.isbn == book.isbn).first()
        if existing_book:
            raise HTTPException(status_code=400, detail="Книга с таким ISBN уже существует")

    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    # При обновлении ISBN проверьте, существует ли он уже для другой книги.
    if book_update.isbn and book_update.isbn != book.isbn:
        existing_book = db.query(models.Book).filter(
            models.Book.isbn == book_update.isbn
        ).filter(models.Book.id != book_id).first()
        if existing_book:
            raise HTTPException(status_code=400, detail="Книга с таким ISBN уже существует")

    # Проверьте автора и жанр, если они обновляются
    if book_update.author_id is not None:
        author = db.query(models.Author).filter(models.Author.id == book_update.author_id).first()
        if not author:
            raise HTTPException(status_code=404, detail="Автор не найден")

    if book_update.genre_id is not None:
        genre = db.query(models.Genre).filter(models.Genre.id == book_update.genre_id).first()
        if not genre:
            raise HTTPException(status_code=404, detail="Жанр не найден")

    # Обновить атрибуты книги
    for field, value in book_update.dict(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    db.delete(book)
    db.commit()
    return {"message": "Книга успешно удалена"}


@router.get("/", response_model=schemas.PaginatedResponse)
def get_books(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество возвращаемых записей"),
    author_id: Optional[int] = Query(None, description="Фильтровать по идентификатору автора"),
    genre_id: Optional[int] = Query(None, description="Фильтровать по идентификатору жанра"),
    author_name: Optional[str] = Query(None, description="Фильтр по имени автора (частичное совпадение)"),
    genre_name: Optional[str] = Query(None, description="Фильтр по названию жанра (частичное совпадение)"),
    title: Optional[str] = Query(None, description="Фильтр по названию книги (частичное совпадение)"),
    sort_by: str = Query("created_at", description="Поле для сортировки"),
    sort_order: str = Query("desc", description="Порядок сортировки: по возрастанию или по убыванию")
):
    query = db.query(models.Book).join(models.Book.author).join(models.Book.genre)


    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)

    if genre_id is not None:
        query = query.filter(models.Book.genre_id == genre_id)

    if author_name is not None:
        query = query.filter(models.Author.name.ilike(f"%{author_name}%"))

    if genre_name is not None:
        query = query.filter(models.Genre.name.ilike(f"%{genre_name}%"))

    if title is not None:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))


    sort_fields_map = {
        "id": models.Book.id,
        "title": models.Book.title,
        "publication_year": models.Book.publication_year,
        "created_at": models.Book.created_at,
        "author_name": models.Author.name,
        "genre_name": models.Genre.name
    }

    if sort_by in sort_fields_map:
        sort_column = sort_fields_map[sort_by]
    else:
        sort_column = models.Book.created_at


    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))


    total = query.count()


    books = query.offset(skip).limit(limit).all()


    pages = (total + limit - 1) // limit

    return schemas.PaginatedResponse(
        items=books,
        total=total,
        page=(skip // limit) + 1,
        limit=limit,
        pages=pages
    )