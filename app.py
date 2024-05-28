from flask import Flask, jsonify, request
from flask_cors import CORS
from models.user import User
from models.product import Product
from models.review import Review
from models.cart import Cart
from models import storage
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask, send_from_directory
from datetime import timedelta
from dotenv import load_dotenv
import os
import logging
from sqlalchemy.orm import joinedload

app = Flask(__name__)
CORS(app, supports_credentials=True)
load_dotenv()

@app.route('/api/doc')
def api_doc():
    return send_from_directory('static', 'api_doc.html')

UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# JWT secret key (replace with a secure random string in production)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)  # Set token expiration time
jwt = JWTManager(app)

logging.basicConfig(level=logging.ERROR)

@app.teardown_appcontext
def close_storage(exception):
    storage.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Get all users
@app.route('/api/users', methods=['GET'])
#@jwt_required()
def get_users():
    users = storage.all(User).values()
    serialized_users = [user.to_dict() for user in users]
    return jsonify(serialized_users)

# Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = storage.all(Product).values()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        app.logger.error(f"Exception on /api/products [GET]: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

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
#@jwt_required()
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
    file = request.files.get('image_url')  # Get image file

    # Handle image upload if a file is provided
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        data['image_url'] = file_path  # Associate image path with product data

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
@jwt_required()
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

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Create a new user with hashed password
    new_user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name)
    storage.new(new_user)
    storage.save()

    return jsonify({'message': 'User registered successfully'}), 201


# Implement User Authentication Endpoint
@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Get all users from storage
    users = storage.all(User).values()

    # Find the user with the specified email
    user = next((user for user in users if user.email == email), None)

    if user and check_password_hash(user.password, password):
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Endpoint to handle image uploads
@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image_url' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image_url']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Create the uploads directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

    return jsonify({'error': 'Upload failed'}), 500

# Get all items in the user's cart
@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart_items():
    try:
        user_id = get_jwt_identity()
        with storage.session_scope() as session:
            user = session.query(User).options(joinedload(User.cart_items)).get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            cart_items = [cart_item.to_dict() for cart_item in user.cart_items]
            return jsonify(cart_items), 200
    except Exception as e:
        app.logger.error(f"Exception on /api/cart [GET]: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Add a product to the user's cart
@app.route('/api/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    product = storage.get(Product, product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart_item = next((item for item in user.cart_items if item.product_id == product_id), None)
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        storage.new(cart_item)

    storage.save()
    return jsonify(cart_item.to_dict()), 201

# Remove a product from the user's cart
@app.route('/api/cart/<product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart_item = next((item for item in user.cart_items if item.product_id == product_id), None)
    if not cart_item:
        return jsonify({"error": "Product not in cart"}), 404

    storage.delete(cart_item)
    storage.save()
    return jsonify({"result": "Product removed from cart"})

if __name__ == '__main__':
    app.run(debug=True)
