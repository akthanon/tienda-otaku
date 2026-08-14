from flask import Flask, request, jsonify, session
from flask_cors import CORS
from database import get_db, init_db
from models import Product, CartItem, User, Order, OrderItem
from datetime import datetime
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Para sesiones

# Configurar CORS
CORS(app, origins=[
    'https://otaku.cuackerman.uk',
    'http://otaku.cuackerman.uk',
    'https://otaku-backend.cuackerman.uk',
    'http://localhost:48080',
    'http://localhost:5000'
], supports_credentials=True)

# Inicializar base de datos
init_db()

# ============ USUARIOS ============

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    db = get_db()
    
    # Verificar si el usuario existe
    existing_user = db.query(User).filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({'error': 'Usuario o email ya existe'}), 400
    
    # Hash de contraseña (simple, en producción usar bcrypt)
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=password_hash
    )
    
    db.add(new_user)
    db.commit()
    
    return jsonify({
        'message': 'Usuario registrado exitosamente',
        'user_id': new_user.id
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db = get_db()
    
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    user = db.query(User).filter(
        User.username == data['username'],
        User.password == password_hash
    ).first()
    
    if not user:
        return jsonify({'error': 'Credenciales incorrectas'}), 401
    
    # Guardar usuario en sesión
    session['user_id'] = user.id
    session['username'] = user.username
    
    return jsonify({
        'message': 'Login exitoso',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout exitoso'})

@app.route('/api/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({'error': 'No autenticado'}), 401
    
    db = get_db()
    user = db.query(User).filter(User.id == session['user_id']).first()
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })

# ============ PRODUCTOS ============

@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    db = get_db()
    
    if category:
        products = db.query(Product).filter(Product.category == category).all()
    else:
        products = db.query(Product).all()
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'image_url': p.image_url,
        'description': p.description,
        'stock': p.stock
    } for p in products])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    db = get_db()
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'category': product.category,
        'image_url': product.image_url,
        'description': product.description,
        'stock': product.stock
    })

# ============ CARRITO ============

@app.route('/api/cart', methods=['GET'])
def get_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    
    db = get_db()
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == session['user_id']
    ).all()
    
    result = []
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            result.append({
                'id': item.id,
                'product_id': item.product_id,
                'name': product.name,
                'price': product.price,
                'quantity': item.quantity,
                'image_url': product.image_url
            })
    
    return jsonify(result)

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    db = get_db()
    
    # Verificar stock
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    if product.stock < quantity:
        return jsonify({'error': 'Stock insuficiente'}), 400
    
    # Verificar si ya está en el carrito
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == session['user_id'],
        CartItem.product_id == product_id
    ).first()
    
    if cart_item:
        if product.stock < cart_item.quantity + quantity:
            return jsonify({'error': 'Stock insuficiente'}), 400
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=session['user_id'],
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)
    
    db.commit()
    return get_cart()

@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    
    db = get_db()
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == session['user_id']
    ).first()
    
    if not cart_item:
        return jsonify({'error': 'Item no encontrado'}), 404
    
    db.delete(cart_item)
    db.commit()
    return get_cart()

@app.route('/api/cart/<int:item_id>', methods=['PUT'])
def update_cart_quantity(item_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    
    data = request.json
    new_quantity = data.get('quantity')
    
    db = get_db()
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.user_id == session['user_id']
    ).first()
    
    if not cart_item:
        return jsonify({'error': 'Item no encontrado'}), 404
    
    if new_quantity <= 0:
        db.delete(cart_item)
    else:
        # Verificar stock
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if product.stock < new_quantity:
            return jsonify({'error': 'Stock insuficiente'}), 400
        cart_item.quantity = new_quantity
    
    db.commit()
    return get_cart()

# ============ PEDIDOS ============

@app.route('/api/checkout', methods=['POST'])
def checkout():
    if 'user_id' not in session:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    
    data = request.json
    db = get_db()
    
    # Obtener items del carrito
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == session['user_id']
    ).all()
    
    if not cart_items:
        return jsonify({'error': 'Carrito vacío'}), 400
    
    # Calcular total y verificar stock
    total = 0
    order_items_data = []
    
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            return jsonify({'error': f'Producto {item.product_id} no encontrado'}), 404
        
        if product.stock < item.quantity:
            return jsonify({'error': f'Stock insuficiente para {product.name}'}), 400
        
        subtotal = product.price * item.quantity
        total += subtotal
        
        order_items_data.append({
            'product_id': product.id,
            'quantity': item.quantity,
            'price': product.price,
            'product': product
        })
    
    # Crear pedido
    order = Order(
        user_id=session['user_id'],
        total=total,
        status='pending',
        shipping_address=data.get('shipping_address', ''),
        payment_method=data.get('payment_method', 'pending')
    )
    
    db.add(order)
    db.flush()  # Para obtener el ID del pedido
    
    # Crear items del pedido
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data['product_id'],
            quantity=item_data['quantity'],
            price=item_data['price']
        )
        db.add(order_item)
        
        # Actualizar stock
        item_data['product'].stock -= item_data['quantity']
    
    # Vaciar carrito
    for item in cart_items:
        db.delete(item)
    
    db.commit()
    
    return jsonify({
        'message': 'Pedido creado exitosamente',
        'order_id': order.id,
        'total': total,
        'status': order.status
    }), 201

@app.route('/api/orders', methods=['GET'])
def get_orders():
    if 'user_id' not in session:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    
    db = get_db()
    orders = db.query(Order).filter(
        Order.user_id == session['user_id']
    ).order_by(Order.created_at.desc()).all()
    
    result = []
    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        items_data = []
        for item in items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            items_data.append({
                'product_name': product.name if product else 'Producto eliminado',
                'quantity': item.quantity,
                'price': item.price,
                'subtotal': item.price * item.quantity
            })
        
        result.append({
            'id': order.id,
            'total': order.total,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'shipping_address': order.shipping_address,
            'payment_method': order.payment_method,
            'items': items_data
        })
    
    return jsonify(result)

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Debes iniciar sesión'}), 401
    
    db = get_db()
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == session['user_id']
    ).first()
    
    if not order:
        return jsonify({'error': 'Pedido no encontrado'}), 404
    
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    items_data = []
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        items_data.append({
            'product_name': product.name if product else 'Producto eliminado',
            'quantity': item.quantity,
            'price': item.price,
            'subtotal': item.price * item.quantity
        })
    
    return jsonify({
        'id': order.id,
        'total': order.total,
        'status': order.status,
        'created_at': order.created_at.isoformat(),
        'shipping_address': order.shipping_address,
        'payment_method': order.payment_method,
        'items': items_data
    })

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    
    # Validar datos
    required_fields = ['name', 'price', 'category']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Falta el campo {field}'}), 400
    
    db = get_db()
    new_product = Product(
        name=data['name'],
        price=float(data['price']),
        category=data['category'],
        image_url=data.get('image_url', '/images/totoro.jpg'),
        description=data.get('description', '')
    )
    
    db.add(new_product)
    db.commit()
    
    return jsonify({
        'message': 'Producto agregado exitosamente',
        'product': {
            'id': new_product.id,
            'name': new_product.name,
            'price': new_product.price,
            'category': new_product.category
        }
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
