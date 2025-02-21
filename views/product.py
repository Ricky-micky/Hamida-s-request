from flask import Blueprint, request, jsonify
from model import Product, db

product_blueprint = Blueprint('product_blueprint', __name__)

# Create Product
@product_blueprint.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    if not all([data.get('name'), data.get('price'), data.get('delivery_cost'), data.get('shop_id')]):
        return jsonify({'error': 'Required fields are missing'}), 400

    new_product = Product(**data)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# Get All Products
@product_blueprint.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id, 'name': p.name, 'price': p.price, 'shop_id': p.shop_id
    } for p in products]), 200

# Get Single Product
@product_blueprint.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price}), 200

# Update Product
@product_blueprint.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

# Delete Product
@product_blueprint.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200
