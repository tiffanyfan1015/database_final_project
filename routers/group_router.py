from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from controllers.group_controller import *

group_bp = Blueprint('group_bp', __name__)

@group_bp.route('/groups', methods=['GET'])
def get_groups_route():
    response = get_groups()
    return render_template('groups.html', data=response['data'])

@group_bp.get('/group/<group_name>')
def get_group_route(group_name):
    response = get_group_by_id(group_name)
    return jsonify(response['data']), response['status_code']

@group_bp.route('/group', methods=['GET', 'POST'])
def create_group_route():
    if request.method == 'POST':
        data = request.form.to_dict()
        response = create_group(data)
        if response['status_code'] == 201:
            status = "success-message"
        else:
            status = "error-message"
        return render_template('create_group.html', message=response['message'], status=status)
    
    return render_template('create_group.html')

@group_bp.route('/group/update/<group_name>', methods=['POST'])
def update_group_route(group_name):
    group_info = request.form.get('group_info')

    response = update_group(group_name, group_info)
    if response['status_code'] == 200:
        status = "success-message"
    else:
        status = "error-message"

    return redirect(url_for("group_bp.get_groups_route", message=response["message"], status=status))


@group_bp.route('/group/delete/<group_name>', methods=['POST'])
def delete_group_route(group_name):
    response = delete_group(group_name)
    if response['status_code'] == 200:
        status = "success-message"
    else:
        status = "error-message"

    return redirect(url_for("group_bp.get_groups_route", message=response["message"], status=status))
