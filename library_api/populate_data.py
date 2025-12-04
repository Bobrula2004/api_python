"""
Script to populate the database with test data for authors, genres, and books
"""
import sys
import os

# Add the parent directory to sys.path to import library_api
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from library_api.db import SessionLocal
from library_api.models import Author, Genre, Book


def create_test_data():
    db: Session = SessionLocal()
    
    try:
        # Create test genres
        genres_data = [
            {"name": "Роман"},
            {"name": "Поэзия"},
            {"name": "Драма"},
            {"name": "Фантастика"},
            {"name": "Фэнтези"},
            {"name": "Научная литература"},
            {"name": "Биография"},
            {"name": "Исторический роман"},
            {"name": "Детектив"},
            {"name": "Приключения"}
        ]
        
        for genre_data in genres_data:
            existing_genre = db.query(Genre).filter(Genre.name == genre_data["name"]).first()
            if not existing_genre:
                genre = Genre(name=genre_data["name"])
                db.add(genre)
        
        db.commit()
        print("Genres created successfully")
        
        # Create test authors
        authors_data = [
            {"name": "Лев Толстой", "bio": "Русский писатель, один из величайших писателей в истории литературы"},
            {"name": "Фёдор Достоевский", "bio": "Русский писатель, философ, мыслитель"},
            {"name": "Александр Пушкин", "bio": "Русский поэт, драматург и прозаик"},
            {"name": "Агата Кристи", "bio": "Английская писательница, автор детективов"},
            {"name": "Дж. Р. Р. Толкин", "bio": "Английский писатель, филолог, профессор"},
            {"name": "Айзек Азимов", "bio": "Американский писатель-фантаст, популяризатор науки"},
            {"name": "Эрнест Хемингуэй", "bio": "Американский писатель и журналист"},
            {"name": "Марк Твен", "bio": "Американский писатель, юморист"}
        ]
        
        for author_data in authors_data:
            existing_author = db.query(Author).filter(Author.name == author_data["name"]).first()
            if not existing_author:
                author = Author(name=author_data["name"], bio=author_data["bio"])
                db.add(author)
        
        db.commit()
        print("Authors created successfully")
        
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
                "author_id": authors[0].id,
                "genre_id": genres[0].id
            },
            {
                "title": "Преступление и наказание",
                "isbn": "978-5-17-084202-9",
                "publication_year": 1866,
                "description": "Роман о внутренней борьбе Родиона Раскольникова",
                "page_count": 672,
                "author_id": authors[1].id,
                "genre_id": genres[0].id
            },
            {
                "title": "Евгений Онегин",
                "isbn": "978-5-17-084203-6",
                "publication_year": 1833,
                "description": "Роман в стихах, признанный вершиной творчества Пушкина",
                "page_count": 288,
                "author_id": authors[2].id,
                "genre_id": genres[1].id
            },
            {
                "title": "Десять негритят",
                "isbn": "978-0-06-207350-4",
                "publication_year": 1939,
                "description": "Классический детектив Агаты Кристи",
                "page_count": 256,
                "author_id": authors[3].id,
                "genre_id": genres[8].id
            },
            {
                "title": "Властелин колец",
                "isbn": "978-0-544-00341-5",
                "publication_year": 1954,
                "description": "Эпическая фэнтезийная история о борьбе за Кольцо Всевластья",
                "page_count": 1216,
                "author_id": authors[4].id,
                "genre_id": genres[4].id
            },
            {
                "title": "Основание",
                "isbn": "978-0-553-29335-0",
                "publication_year": 1951,
                "description": "Научно-фантастический роман о падении Галактической Империи",
                "page_count": 244,
                "author_id": authors[5].id,
                "genre_id": genres[3].id
            },
            {
                "title": "Старик и море",
                "isbn": "978-0-684-80333-1",
                "publication_year": 1952,
                "description": "Роман о старом кубинском рыбаке Сантьяго",
                "page_count": 127,
                "author_id": authors[6].id,
                "genre_id": genres[0].id
            },
            {
                "title": "Приключения Тома Сойера",
                "isbn": "978-0-486-40077-6",
                "publication_year": 1876,
                "description": "Приключенческий роман о мальчике на Миссисипи",
                "page_count": 224,
                "author_id": authors[7].id,
                "genre_id": genres[9].id
            }
        ]
        
        for book_data in books_data:
            existing_book = db.query(Book).filter(Book.isbn == book_data["isbn"]).first()
            if not existing_book:
                book = Book(**book_data)
                db.add(book)
        
        db.commit()
        print("Books created successfully")
        print(f"Added {len(genres_data)} genres, {len(authors_data)} authors, and {len(books_data)} books to the database")
        
    except Exception as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()