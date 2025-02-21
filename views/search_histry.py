from flask import Blueprint, request, jsonify
from model import SearchHistory, db
from datetime import datetime

search_history_blueprint = Blueprint('search_history_blueprint', __name__)

# Create Search History Entry
@search_history_blueprint.route('/search_history', methods=['POST'])
def create_search_history():
    data = request.get_json()
    if not all([data.get('user_id'), data.get('query')]):
        return jsonify({'error': 'User ID and query are required'}), 400

    new_search = SearchHistory(user_id=data['user_id'], query=data['query'])
    db.session.add(new_search)
    db.session.commit()
    return jsonify({'message': 'Search history recorded successfully'}), 201

# Get All Search History
@search_history_blueprint.route('/search_history', methods=['GET'])
def get_search_history():
    searches = SearchHistory.query.all()
    return jsonify([
        {'id': s.id, 'user_id': s.user_id, 'query': s.query, 'searched_at': s.searched_at}
        for s in searches
    ]), 200

# Get Search History for a Specific User
@search_history_blueprint.route('/search_history/user/<int:user_id>', methods=['GET'])
def get_search_history_by_user(user_id):
    searches = SearchHistory.query.filter_by(user_id=user_id).all()
    if not searches:
        return jsonify({'message': 'No search history found for this user'}), 404
    return jsonify([
        {'id': s.id, 'user_id': s.user_id, 'query': s.query, 'searched_at': s.searched_at}
        for s in searches
    ]), 200

# Delete a Search History Entry
@search_history_blueprint.route('/search_history/<int:search_id>', methods=['DELETE'])
def delete_search_history(search_id):
    search = SearchHistory.query.get_or_404(search_id)
    db.session.delete(search)
    db.session.commit()
    return jsonify({'message': 'Search history entry deleted successfully'}), 200
