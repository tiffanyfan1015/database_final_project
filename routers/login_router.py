from flask import Blueprint, request, jsonify
from controllers.login_controller import get_users, get_user_by_id, add_user, update_user, delete_user, login

login_bp = Blueprint('login_bp', __name__)

@login_bp.get('/users')
def get_users_route():
    response = get_users()
    return jsonify(response['data']), response['status_code']

@login_bp.get('/users/<user_id>')
def get_user_route(user_id):
    response = get_user_by_id(user_id)
    return jsonify(response['data']), response['status_code']

@login_bp.post('/users')
def add_user_route():
    data = request.get_json()
    response = add_user(data)
    return jsonify(response['message']), response['status_code']

@login_bp.put('/users/<user_id>')
def update_user_route(user_id):
    data = request.get_json()
    response = update_user(user_id, data)
    return jsonify(response['message']), response['status_code']

@login_bp.delete('/users/<user_id>')
def delete_user_route(user_id):
    response = delete_user(user_id)
    return jsonify(response['message']), response['status_code']

@login_bp.post('/login')
def login_route():
    data = request.get_json()
    response = login(data)
    return jsonify(response['message']), response['status_code']