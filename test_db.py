import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from library_api.db import engine, SessionLocal
from library_api.models.database import Base

# Тест бд
try:

    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
    

    db = SessionLocal()
    print("Database session created successfully")
    

    from library_api.models.database import Author
    test_author = Author(name="Test Author", bio="A test author")
    db.add(test_author)
    db.commit()
    print(f"Test author created successfully with ID: {test_author.id}")
    

    db.delete(test_author)
    db.commit()
    db.close()
    
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()