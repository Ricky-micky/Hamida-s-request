from flask import Flask,request,jsonify
from flask_migrate import Migrate
from model import db, User, Product, Shop, SearchHistory, ComparisonResult, Order, Payment
import africastalking

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cwalshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 


# Initialize the database with the app
db.init_app(app)

migrate = Migrate(app, db)

# Initialize Africa's Talking
africastalking.initialize(username='sandbox', api_key='atsk_69bc0eb6311a924f5104f19c0cf3ce51badf4216c9dc04e924beb28c9a74c28f735f718f')
sms = africastalking.SMS

@app.route('/payments', methods=['POST'])
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

#import views after the db is 
from views.payment import payment_blueprint
from views.shops import shop_blueprint
from views.product import product_blueprint
from views.User import user_blueprint
from views.order import order_blueprint
from views.ComparionResult import comparison_blueprint
from views.search_histry import search_history_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(shop_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(comparison_blueprint)
app.register_blueprint(search_history_blueprint)
app.register_blueprint(payment_blueprint)


if __name__ == '__main__':
    app.run(debug=True)
