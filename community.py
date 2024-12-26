import os
from flask import Flask, render_template
from routers.community_router import community_bp

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET"),

# 註冊藍圖（Blueprint）
app.register_blueprint(community_bp)

@app.route('/')
def home():
    return render_template('community_index.html')  # 渲染首頁

if __name__ == '__main__':
    app.run(debug=True)
