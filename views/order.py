from flask import Blueprint, request, jsonify
from model import Order, db

order_blueprint = Blueprint('order_blueprint', __name__)

# Create Order
@order_blueprint.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    if not all([data.get('user_id'), data.get('product_id'), data.get('quantity')]):
        return jsonify({'error': 'Required fields are missing'}), 400

    new_order = Order(**data)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully'}), 201

# Get All Orders
@order_blueprint.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': o.id, 'user_id': o.user_id, 'product_id': o.product_id, 'quantity': o.quantity
    } for o in orders]), 200

# Get Single Order
@order_blueprint.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({'id': order.id, 'user_id': order.user_id, 'product_id': order.product_id}), 200

# Update Order
@order_blueprint.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    order.quantity = data.get('quantity', order.quantity)
    db.session.commit()
    return jsonify({'message': 'Order updated successfully'}), 200

# Delete Order
@order_blueprint.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'}), 200
