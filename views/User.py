from flask import Blueprint, request, jsonify
from model import User, db
from werkzeug.security import generate_password_hash, check_password_hash

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/register', methods=['POST'])
def register_user():
    get_user_inputs = request.get_json()

    username = get_user_inputs.get("username")
    email = get_user_inputs.get("email")
    phoneNumber = get_user_inputs.get("phoneNumber")
    password = get_user_inputs.get("password")
    Role = get_user_inputs.get("Role")

    # Validate inputs
    if not all([username, email, phoneNumber, password, Role]):
        return jsonify({'error': 'All fields are required'}), 400

    # Check if the email is already registered
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user instance
    create_new_user = User(
        username=username,
        email=email,
        phoneNumber=phoneNumber,
        password=hashed_password,
        Role=Role
    )

    # Add and commit to the database
    db.session.add(create_new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201
# ✅ Fetch All Users
@user_blueprint.route('/users', methods=['GET'])
def fetch_all_users():
    users = User.query.all()
    users_list = [
        {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'phonenumber': user.phonenumber
        }
        for user in users
    ]
    return jsonify({'users': users_list, 'total_users': len(users)}), 200


# ✅ Get Single User
@user_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'phonenumber': user.phonenumber
    }), 200


# ✅ Update User
@user_blueprint.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.phonenumber = data.get('phonenumber', user.phonenumber)

    if 'password' in data:
        user.password = generate_password_hash(data['password'])

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200


# ✅ Delete User
@user_blueprint.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


# ✅ User Login
@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        }
    }), 200


# ✅ Search Users by Email or Username
@user_blueprint.route('/search', methods=['GET'])
def search_users():
    query = request.args.get('q', '')

    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    users = User.query.filter(
        (User.email.ilike(f"%{query}%")) | (User.username.ilike(f"%{query}%"))
    ).all()

    users_list = [
        {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email
        }
        for user in users
    ]

    return jsonify({"users": users_list, "total_results": len(users)}), 200
