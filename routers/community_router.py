from flask import Blueprint, request, redirect, url_for, render_template  # type: ignore
from controllers.community_controller import handle_group, create_group, get_community_by_group_id, get_posts_by_group_id, get_chat_by_group, send_message_to_chat

community_bp = Blueprint('community_bp', __name__)

@community_bp.route('/community', methods=['GET', 'POST'])
def community_page():
    if request.method == 'POST':
        group_id = request.form['group_id']
        group_exists, group_name = handle_group(group_id)
        if group_exists:
            return redirect(url_for('community_bp.view_community', group_id=group_id))
        else:
            create_group(group_id)
            return redirect(url_for('community_bp.view_community', group_id=group_id))
    return render_template('enter_group.html')

@community_bp.route('/community/<group_id>')
def view_community(group_id):
    community = get_community_by_group_id(group_id)
    posts = get_posts_by_group_id(group_id) 
    return render_template('community.html', community=community, posts=posts)

@community_bp.route('/community/<group_id>/chatroom')
def view_chat_room(group_id):
    return render_template('chatroom.html', group_id=group_id)

@community_bp.route('/community/<group_id>/recommend')
def view_recommend(group_id):
    return render_template('recommend.html', group_id=group_id)

@community_bp.route('/community/<group_id>/chatroom', methods=['GET'])
def view_chatroom(group_id):
    chats = get_chat_by_group(group_id)  
    return render_template('chatroom.html', group_id=group_id, chats=chats)

@community_bp.route('/community/<group_id>/chatroom', methods=['POST'])
def send_message(group_id):
    # 這段可以再加user
    message = request.form['message']
    send_message_to_chat(group_id, message)
    return redirect(url_for('community_bp.view_chatroom', group_id=group_id))


