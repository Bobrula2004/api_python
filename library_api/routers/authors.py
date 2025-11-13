from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from typing import List, Optional
from library_api import models, schemas, db
from library_api.db import get_db

router = APIRouter(prefix="/api/v1/authors", tags=["authors"])


@router.post("/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.get("/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return author


@router.put("/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author_update: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    
    # Update author attributes
    for field, value in author_update.dict(exclude_unset=True).items():
        setattr(author, field, value)
    
    db.commit()
    db.refresh(author)
    return author


@router.delete("/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    
    db.delete(author)
    db.commit()
    return {"message": "Автор удален успешно"}


@router.get("/", response_model=List[schemas.Author])
def get_authors(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Количество пропущенных записей"),
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество возвращаемых записей")
):
    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return authors