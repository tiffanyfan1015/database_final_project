from flask import Blueprint, redirect, render_template, request, jsonify, session
from controllers.login_controller import *

login_bp = Blueprint('login_bp', __name__, template_folder='templates')


@login_bp.get('/users')
def get_users_route():
    response = get_users()
    return jsonify(response['data']), response['status_code']

@login_bp.get('/users/<user_id>')
def get_user_route(user_id):
    response = get_user_by_name(user_id)
    return jsonify(response['data']), response['status_code']

@login_bp.route('/signup', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        data = request.form.to_dict()
        response = add_user(data)
        if response['status_code'] == 201:
            status = "success-message"
            return redirect("/login")
        else: 
            status = "error-message"
            return render_template('signup.html', message=response['message'], status=status)
    return render_template('signup.html')

@login_bp.route('/users/password', methods=['GET', 'POST'])
def update_user_route():
    if 'username' not in session:
        return redirect('/login', message="Please login first", status="error-message")
    if request.method == 'POST':
        data = request.form.to_dict()
        data['username'] = session['username']
        response = update_user(data)
        if response['status_code'] == 200:
            redirect('/')
        else:
            return jsonify(response['message']), response['status_code']
    
    return render_template('modify_pwd.html')

@login_bp.delete('/users/<user_id>')
def delete_user_route(user_id):
    response = delete_user(user_id)
    return jsonify(response['message']), response['status_code']

@login_bp.route('/login', methods=['GET', 'POST'])
def login_route():
    if 'username' in session:
        return redirect('/')
    if request.method == 'POST':
        data = request.form.to_dict()
        response = login(data)
        if response['status_code'] == 200:  
            session['username'] = data['username']
            status = "success-message"
            return redirect('/')
        else:
            status = "error-message"
            return render_template('login.html', message=response['message'], status=status)
    
    return render_template('login.html')

@login_bp.route('/logout')
def logout_route():
    session.clear()
    return redirect("/")