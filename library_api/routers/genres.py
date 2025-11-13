from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from library_api import models, schemas
from library_api.db import get_db

router = APIRouter(prefix="/api/v1/genres", tags=["genres"])


@router.post("/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    # Проверка на наличие жанра
    existing_genre = db.query(models.Genre).filter(
        models.Genre.name == genre.name
    ).first()
    if existing_genre:
        raise HTTPException(status_code=400, detail="Жанр с таким названием уже существует")
    
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


@router.get("/{genre_id}", response_model=schemas.Genre)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    return genre


@router.put("/{genre_id}", response_model=schemas.Genre)
def update_genre(genre_id: int, genre_update: schemas.GenreUpdate, db: Session = Depends(get_db)):
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    

    if genre_update.name is not None:
        existing_genre = db.query(models.Genre).filter(
            models.Genre.name == genre_update.name
        ).filter(models.Genre.id != genre_id).first()
        if existing_genre:
            raise HTTPException(status_code=400, detail="Жанр с таким названием уже существует")
    
    # Обновление атрибутов жанра
    for field, value in genre_update.dict(exclude_unset=True).items():
        if value is not None:
            setattr(genre, field, value)
    
    db.commit()
    db.refresh(genre)
    return genre


@router.delete("/{genre_id}")
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    
    db.delete(genre)
    db.commit()
    return {"message": "Жанр успешно удален"}


@router.get("/", response_model=List[schemas.Genre])
def get_genres(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество возвращаемых записей")
):
    genres = db.query(models.Genre).offset(skip).limit(limit).all()
    return genres