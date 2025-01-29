from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
app = Flask(__name__)
app.config["SECRET_KEY"] = 'BLACK_SWORDSMAN'
app.config["JWT_SECRET_KEY"] = "BLACK_SWORDSMAN"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True)  # Allow React.js to interact with Flask API

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

# Register endpoint
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# Login endpoint
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        # Generate token
        import json
        access_token = create_access_token(identity=json.dumps({"id": user.id, "username": user.username}))
        print("Access Token:", access_token)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# Example protected route
@app.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    identity = get_jwt_identity()
    user_data = json.loads(identity)  # Convert back to a dictionary
    return jsonify({"message": f"Welcome {user_data['username']}!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
