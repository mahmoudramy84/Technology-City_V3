from flask import Flask, jsonify, request
from flask_cors import CORS
from models.user import User
from models.product import Product
from models.review import Review
from models import storage
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
CORS(app, supports_credentials=True)

# Get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = storage.all(User).values()
    serialized_users = [user.to_dict() for user in users]
    return jsonify(serialized_users)

# Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    products = storage.all(Product).values()
    serialized_products = [product.to_dict() for product in products]
    return jsonify(serialized_products)

# Get all reviews
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = storage.all(Review).values()
    serialized_reviews = [review.to_dict() for review in reviews]
    return jsonify(serialized_reviews)

#Get Product by ID
@app.route('/api/products/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = storage.get(Product, product_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

#Get User by ID:
@app.route('/api/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "User not found"}), 404

#Get Review by ID:
@app.route('/api/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    return jsonify({"error": "Review not found"}), 404

# Create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201

# Create a new product
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(**data)
    storage.new(new_product)
    storage.save()
    return jsonify(new_product.to_dict()), 201

# Create a new review
@app.route('/api/reviews', methods=['POST'])
def create_review():
    data = request.json
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201

# Update a user
@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = storage.get(User, user_id)
    if user:
        for key, value in data.items():
            setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

# Delete a user
@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

# Update a product
@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = storage.get(Product, product_id)
    if product:
        for key, value in data.items():
            setattr(product, key, value)
        storage.save()
        return jsonify(product.to_dict()), 200
    return jsonify({"error": "Product not found"}), 404

# Delete a product
@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = storage.get(Product, product_id)
    if product:
        storage.delete(product)
        storage.save()
        return jsonify({"message": "Product deleted successfully"}), 200
    return jsonify({"error": "Product not found"}), 404

# Update a review
@app.route('/api/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.json
    review = storage.get(Review, review_id)
    if review:
        for key, value in data.items():
            setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
    return jsonify({"error": "Review not found"}), 404

# Delete a review
@app.route('/api/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({"message": "Review deleted successfully"}), 200
    return jsonify({"error": "Review not found"}), 404

# Implement User Signup Endpoint
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    existing_user = next((user for user in storage.all(User).values() if user.email == email), None)

    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    #hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=password, first_name=first_name, last_name=last_name)
    storage.new(new_user)
    storage.save()

    return jsonify({'message': 'User registered successfully'}), 201

# Implement User Authentication Endpoint
@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = next((user for user in storage.all(User).values() if user.email == email), None)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    print("Password provided:", password)
    print("Hashed password in database:", user.password)

    if not (user.password == password):
        print("Password check failed")
        return jsonify({'error': 'Invalid password'}), 401

    print("Password check passed")

    return jsonify({'message': 'User login successful'}), 200


if __name__ == '__main__':
    app.run(debug=True)
