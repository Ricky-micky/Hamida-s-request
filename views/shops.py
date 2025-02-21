from flask import Blueprint, request, jsonify
from model import Shop, db

shop_blueprint = Blueprint('shop_blueprint', __name__)

# Create Shop
@shop_blueprint.route('/shops', methods=['POST'])
def create_shop():
    data = request.get_json()
    if not all([data.get('name'), data.get('url')]):
        return jsonify({'error': 'Required fields are missing'}), 400

    new_shop = Shop(**data)
    db.session.add(new_shop)
    db.session.commit()
    return jsonify({'message': 'Shop created successfully'}), 201

# Get All Shops
@shop_blueprint.route('/shops', methods=['GET'])
def get_shops():
    shops = Shop.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'url': s.url} for s in shops]), 200

# Get Single Shop
@shop_blueprint.route('/shops/<int:shop_id>', methods=['GET'])
def get_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    return jsonify({'id': shop.id, 'name': shop.name, 'url': shop.url}), 200

# Update Shop
@shop_blueprint.route('/shops/<int:shop_id>', methods=['PUT'])
def update_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    data = request.get_json()
    shop.name = data.get('name', shop.name)
    shop.url = data.get('url', shop.url)
    db.session.commit()
    return jsonify({'message': 'Shop updated successfully'}), 200

# Delete Shop
@shop_blueprint.route('/shops/<int:shop_id>', methods=['DELETE'])
def delete_shop(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    db.session.delete(shop)
    db.session.commit()
    return jsonify({'message': 'Shop deleted successfully'}), 200
