from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from model import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    phone_number = data.get('phoneNumber')
    password = data.get('password')
    role = data.get('role', 'user')
    
    if not all([username, email, phone_number, password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if User.query.filter((User.username == username) | (User.email == email) | (User.phoneNumber == phone_number)).first():
        return jsonify({'error': 'User already exists'}), 409
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, phoneNumber=phone_number, password=hashed_password, Role=role)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
    return jsonify({'message': 'Login successful', 'access_token': access_token, 'role': user.Role}), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({'message': f'Welcome {user.username}', 'role': user.Role}), 200
