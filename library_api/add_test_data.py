"""
Simple script to add test data to the database
"""
import sys
import os
# Add the parent directory to sys.path to import library_api
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from library_api.db import SessionLocal
from library_api.models import Author, Genre, Book

def add_test_data():
    db = SessionLocal()
    
    try:
        # Create test genres
        genres_data = [
            {"name": "Роман"},
            {"name": "Поэзия"},
            {"name": "Драма"},
            {"name": "Фантастика"},
            {"name": "Фэнтези"},
        ]
        
        for genre_data in genres_data:
            existing_genre = db.query(Genre).filter(Genre.name == genre_data["name"]).first()
            if not existing_genre:
                genre = Genre(**genre_data)
                db.add(genre)
        
        db.commit()
        print("Genres added successfully")
        
        # Create test authors
        authors_data = [
            {"name": "Лев Толстой", "bio": "Русский писатель, один из величайших писателей в истории литературы"},
            {"name": "Фёдор Достоевский", "bio": "Русский писатель, философ, мыслитель"},
            {"name": "Александр Пушкин", "bio": "Русский поэт, драматург и прозаик"},
        ]
        
        for author_data in authors_data:
            existing_author = db.query(Author).filter(Author.name == author_data["name"]).first()
            if not existing_author:
                author = Author(**author_data)
                db.add(author)
        
        db.commit()
        print("Authors added successfully")
        
        # Get genres and authors for creating books
        genres = db.query(Genre).all()
        authors = db.query(Author).all()
        
        # Create test books
        books_data = [
            {
                "title": "Война и мир",
                "isbn": "978-5-17-084201-2",
                "publication_year": 1869,
                "description": "Эпический роман о русском обществе в период войн 1805-1820 годов",
                "page_count": 1272,
                "author_id": authors[0].id if authors else 1,
                "genre_id": genres[0].id if genres else 1
            },
            {
                "title": "Преступление и наказание",
                "isbn": "978-5-17-084202-9",
                "publication_year": 1866,
                "description": "Роман о внутренней борьбе Родиона Раскольникова",
                "page_count": 672,
                "author_id": authors[1].id if len(authors) > 1 else 1,
                "genre_id": genres[0].id if genres else 1
            }
        ]
        
        for book_data in books_data:
            existing_book = db.query(Book).filter(Book.isbn == book_data["isbn"]).first()
            if not existing_book:
                book = Book(**book_data)
                db.add(book)
        
        db.commit()
        print("Books added successfully")
        print(f"Added {len(genres_data)} genres, {len(authors_data)} authors, and {len(books_data)} books to the database")

    except Exception as e:
        print(f"Error adding test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_test_data()