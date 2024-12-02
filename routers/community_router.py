from flask import Blueprint, render_template, request, jsonify

from controllers.community_controller import get_community, get_posts

community_bp = Blueprint('community_bp', __name__)

# 路由：查看社區（group）
@community_bp.route('/community/<int:group_id>', methods=['GET'])
def community_page(group_id):
    community = get_community(group_id)
    posts = get_posts(group_id)
    return render_template('community.html', community=community, posts=posts)

# 路由：發送消息到聊天室
@community_bp.route('/community/<int:group_id>/chat', methods=['POST'])
def send_chat(group_id):
    message = request.form.get('message')
    # 這裡可以調用控制器來處理消息發送
    return jsonify({'message': 'Message sent successfully'}), 200
