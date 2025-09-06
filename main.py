from fastapi import Depends, FastAPI
from models import Product  # Importing the Product model
from database import session, engine # Importing database session and engine
import database_model  # Importing the database models
from sqlalchemy.orm import Session

app = FastAPI()

database_model.Base.metadata.create_all(bind = engine) #Creating all tables in the database


@app.get("/")  #Root endpoint, Decorator for GET requests
def greet():
    return "Hello, World!"  #Return a greeting message
    
products = [
    Product(id=1, name="Laptop", price=999.99, description="A high-performance laptop", quantity=10),
    Product(id=2, name="Smartphone", price=499.99, description="A latest model smartphone", quantity=25),
    Product(id=3, name="Headphones", price=199.99, description="Noise-cancelling headphones", quantity=15),
]  #List to store products

def get_db():
    db = session() #Creating a new database session
    try:
        yield db
    finally:
        db.close() #Closing the database session

def init_db():
    db = session() #Creating a new database session
    count = db.query(database_model.Product).count #Counting existing products in the database
    if count == 0:
        for product in products:
            db.add(database_model.Product(**product.model_dump())) #Adding products to the database
        db.commit() #Committing the changes to the database
init_db() #Initialize the database with sample products
  
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(database_model.Product).all() #Querying all products from the database
    return db_products  #Return the list of products
    
@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_model.Product).filter(database_model.Product.id == id).first()
    if db_product:
        return db_product #Return a product by its ID (adjusting for zero-based index)
    return "Product not found"

@app.post("/product")            
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/product/{id}")  
def update_product(id: int, updated_product: Product):
    for i in range(len(products)):
        if products[i].id == id: #Finding the product by ID. 
            products[i] = updated_product
            return updated_product
    return {"error": "Product not found"}
    
@app.delete("/product/{id}")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return {"message": "Product deleted"}
    return {"error": "Product not found"}
    