from .extentions import db
from datetime import datetime, timezone

# This is not a table.
class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer(), primary_key = True)
    created_at = db.Column(db.DateTime(timezone = True), 
                           default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone = True), 
                           default = lambda: datetime.now(timezone.utc)
                           onupdate = lambda: datetime.now(timezone.utc))
    

class User(BaseModel):
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False, unique = True)
    
    manager_requests = db.relationship("ManagerRequest", back_populates = "user")

class ManagerRequest(BaseModel):
    data = db.Column(db.JSON())
    status = db.Column(db.Enum("approved", "rejected", "created"))
    request_type = db.Column(String)
    
    # to know who creted the request.
    user_id = db.Column(db.Integer(), db.ForiegnKey("user.id"))
    # for db.relationship. 
    user = db.relationship("User", back_populates = "manager_requests")

class Section(BaseModel):
    name = db.Column(db.String, nullable = False)
    
    # Relationship
    products = db.relationship("Product", back_populates = "section")
    
class Product(BaseModel):
    name = db.Column(db.String, nullable = False)
    price = db.Column(db.Numeric(10, 2), nullable = False)
    stock = db.Column(db.Numeric(10, 2))
    expiry = db.Column(db.DateTime(timezone = True))
    mfd = db.Column(db.DateTime(timezone = True))
    unit_of_sale = db.Column(db.Enum("kg", "litre", "unit")) # kg/liter/unit
    section_id = db.Column(db.Integer(), nullable = False, db.ForiegnKey("section.id"))
    
    # Relationship
    section = db.relationship("Section", back_populates = "products")
    product = db.relationship("SaleItem", back_populates = "sale_items")
    
    
class Sale(BaseModel):
    total_amount = db.Column(db.Numeric(10, 2))
    
    customer_id = db.Column(db.Integer(), db.ForiegnKey("user.id"))
    
    # Relationship
    sale_items = db.relationship("SaleItem", back_populates = "sale")
    
    
    
class SaleItem(BaseModel):
    quantity = db.Column(db.Numeric(10, 2))
    price_at_sale = db.Column(db.Numeric(10, 2), nullable = False)
    
    product_id = db.Column(db.Integer(), db.ForiegnKey("product.id"))
    sale_id = db.Column(db.Integer(), db.ForiegnKey("sale.id"))
    
    # Relationship
    sale = db.relationship("Sale", back_populates = "sale_items")
    product = db.relationship("Product", back_populates = "product")