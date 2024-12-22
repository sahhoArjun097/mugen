from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from models import mongo
from routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
mongo.init_app(app)
jwt = JWTManager(app)

# Register routes
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
