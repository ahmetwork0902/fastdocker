from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.staticfiles import StaticFiles

# Создание экземпляра FastAPI
app = FastAPI()

# Подключите папку static как статическую директорию
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение к базе данных
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@db:5432/sqlfastdocker"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


# Определение моделей данных
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

    def __repr__(self):
        return f"<Item id={self.id}, name={self.name}>"

# Определение схем данных для валидации запросов
class ItemCreate(BaseModel):
    name: str
    description: str


# Определение CRUD-методов
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate, db=Depends(get_db)):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
