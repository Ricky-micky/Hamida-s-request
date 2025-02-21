from flask import Blueprint, request, jsonify
from model import ComparisonResult, db

comparison_blueprint = Blueprint('comparison_blueprint', __name__)

# Create Comparison Result
@comparison_blueprint.route('/comparison_results', methods=['POST'])
def create_comparison():
    data = request.get_json()
    required_fields = [
        'product_name', 'shop_x_cost', 'shop_x_delivery_cost', 'shop_y_cost', 'shop_y_delivery_cost'
    ]
    
    if not all(data.get(field) is not None for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    new_comparison = ComparisonResult(**data)
    db.session.add(new_comparison)
    db.session.commit()
    return jsonify({'message': 'Comparison result recorded successfully'}), 201

# Get All Comparison Results
@comparison_blueprint.route('/comparison_results', methods=['GET'])
def get_comparison_results():
    comparisons = ComparisonResult.query.all()
    return jsonify([
        {
            'id': c.id, 'product_name': c.product_name,
            'shop_x_cost': c.shop_x_cost, 'shop_x_rating': c.shop_x_rating, 'shop_x_delivery_cost': c.shop_x_delivery_cost, 'shop_x_payment_mode': c.shop_x_payment_mode,
            'shop_y_cost': c.shop_y_cost, 'shop_y_rating': c.shop_y_rating, 'shop_y_delivery_cost': c.shop_y_delivery_cost, 'shop_y_payment_mode': c.shop_y_payment_mode,
            'marginal_benefit': c.marginal_benefit, 'cost_benefit': c.cost_benefit
        } for c in comparisons
    ]), 200

# Get Comparison Result by ID
@comparison_blueprint.route('/comparison_results/<int:comparison_id>', methods=['GET'])
def get_comparison(comparison_id):
    comparison = ComparisonResult.query.get_or_404(comparison_id)
    return jsonify({
        'id': comparison.id, 'product_name': comparison.product_name,
        'shop_x_cost': comparison.shop_x_cost, 'shop_x_rating': comparison.shop_x_rating, 'shop_x_delivery_cost': comparison.shop_x_delivery_cost, 'shop_x_payment_mode': comparison.shop_x_payment_mode,
        'shop_y_cost': comparison.shop_y_cost, 'shop_y_rating': comparison.shop_y_rating, 'shop_y_delivery_cost': comparison.shop_y_delivery_cost, 'shop_y_payment_mode': comparison.shop_y_payment_mode,
        'marginal_benefit': comparison.marginal_benefit, 'cost_benefit': comparison.cost_benefit
    }), 200

# Update Comparison Result
@comparison_blueprint.route('/comparison_results/<int:comparison_id>', methods=['PUT'])
def update_comparison(comparison_id):
    comparison = ComparisonResult.query.get_or_404(comparison_id)
    data = request.get_json()

    for key, value in data.items():
        setattr(comparison, key, value)

    db.session.commit()
    return jsonify({'message': 'Comparison result updated successfully'}), 200

# Delete Comparison Result
@comparison_blueprint.route('/comparison_results/<int:comparison_id>', methods=['DELETE'])
def delete_comparison(comparison_id):
    comparison = ComparisonResult.query.get_or_404(comparison_id)
    db.session.delete(comparison)
    db.session.commit()
    return jsonify({'message': 'Comparison result deleted successfully'}), 200
