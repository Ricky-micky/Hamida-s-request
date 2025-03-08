from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    phoneNumber = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    Role = db.Column(db.String, nullable =False, default = "user")

    search_history = db.relationship('SearchHistory', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    product_price = db.Column(db.Float)
    product_rating = db.Column(db.Float)
    product_url = db.Column(db.String(255))
    delivery_cost = db.Column(db.Float)
    shop_name = db.Column(db.String(100))
    payment_mode = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    navigate_link = db.Column(db.String(255))  # New field for the navigation link

    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id', name='fk_product_shop'), nullable=False)  # Specify constraint name
    comparisons = db.relationship('ComparisonResult', backref='product', lazy=True)
    
    shop = db.relationship('Shop', backref='shop_products')


class Shop(db.Model):
    __tablename__ = 'shops'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)


class SearchHistory(db.Model):
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query = db.Column(db.String, nullable=False)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)


class ComparisonResult(db.Model):
    __tablename__ = 'comparison_results'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    shop_x_cost = db.Column(db.Float, nullable=False)
    shop_x_rating = db.Column(db.Float)
    shop_x_delivery_cost = db.Column(db.Float, nullable=False)
    shop_x_payment_mode = db.Column(db.String)
    shop_y_cost = db.Column(db.Float, nullable=False)
    shop_y_rating = db.Column(db.Float)
    shop_y_delivery_cost = db.Column(db.Float, nullable=False)
    shop_y_payment_mode = db.Column(db.String)
    marginal_benefit = db.Column(db.Float)
    cost_benefit = db.Column(db.Float)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('orders', lazy=True))


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String, nullable=False)  # e.g., "Pending", "Completed"

    order = db.relationship('Order', backref=db.backref('payment', uselist=False))



