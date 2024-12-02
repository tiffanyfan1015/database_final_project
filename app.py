from flask import Flask
from routers.login_router import login_bp
# from routers.game_filtering_router import game_filtering_bp
app = Flask(__name__)

app.register_blueprint(login_bp)

@app.route('/')
def home():
    return "Welcome to the Flask API Server!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
