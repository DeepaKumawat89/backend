from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt, datetime
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abef4efc4f756df701259c378c9133934515cf651c3af713a42b688504c96bd8'
client = MongoClient('mongodb+srv://user_1234:user123456@cluster0.a68dltx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client["auth_demo"]

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if db.users.find_one({'email': data['email']}):
        return jsonify({'error': 'Email already exists'}), 400
    hashed_pw = generate_password_hash(data['password'])
    db.users.insert_one({'email': data['email'], 'password': hashed_pw})
    return jsonify({'message': 'Signup successful!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.users.find_one({'email': data['email']})
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = jwt.encode({
        'user_id': str(user['_id']),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

