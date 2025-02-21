from flask import Blueprint, request, jsonify
from model import Payment, db

payment_blueprint = Blueprint('payment_blueprint', __name__)

# Create Payment
@payment_blueprint.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    if not all([data.get('order_id'), data.get('amount'), data.get('status')]):
        return jsonify({'error': 'Required fields are missing'}), 400

    new_payment = Payment(**data)
    db.session.add(new_payment)
    db.session.commit()

    # Send SMS confirmation@payment_blueprint.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    if not all([data.get('order_id'), data.get('amount'), data.get('status')]):
        return jsonify({'error': 'Required fields are missing'}), 400

    new_payment = Payment(**data)
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment recorded successfully'}), 201

    try:
        recipients = ["+254712345678"]  # Replace with the recipient's phone number in international format
        message = f"Payment of {data['amount']} has been recorded successfully. Thank you for your purchase!"
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print(f"Error sending SMS: {e}")

    return jsonify({'message': 'Payment recorded successfully and SMS sent'}), 201

# @payment_blueprint.route('/payments', methods=['POST'])
# def create_payment():
#     data = request.get_json()
#     if not all([data.get('order_id'), data.get('amount'), data.get('status')]):
#         return jsonify({'error': 'Required fields are missing'}), 400

#     new_payment = Payment(**data)
#     db.session.add(new_payment)
#     db.session.commit()
#     return jsonify({'message': 'Payment recorded successfully'}), 201

# Get All Payments
@payment_blueprint.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([{
        'id': p.id, 'order_id': p.order_id, 'amount': p.amount, 'status': p.status
    } for p in payments]), 200

# Get Single Payment
@payment_blueprint.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify({'id': payment.id, 'order_id': payment.order_id, 'amount': payment.amount}), 200

# Update Payment
@payment_blueprint.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json()
    payment.status = data.get('status', payment.status)
    db.session.commit()
    return jsonify({'message': 'Payment updated successfully'}), 200

# Delete Payment
@payment_blueprint.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted successfully'}), 200
