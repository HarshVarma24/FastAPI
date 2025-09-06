from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:root@localhost:5432/telusko_db"
engine = create_engine(db_url) # Add your database URL and configurations here
session = sessionmaker(autocommit = False, autoflush = False, bind = engine)
