// ============ CONFIGURACIÓN ============
const API_URL = 'http://localhost/api';
let currentCategory = 'all';
let cart = [];
let products = [];
let currentUser = null;
let isLoginMode = true;

// ============ NAVEGACIÓN ============
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = link.dataset.page;
        
        // Actualizar links activos
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Mostrar página correspondiente
        document.querySelectorAll('.page-section').forEach(s => s.classList.remove('active'));
        document.getElementById(`page-${page}`).classList.add('active');
        
        // Cargar datos según página
        if (page === 'orders') loadOrders();
        if (page === 'profile') loadProfile();
    });
});

// ============ TOAST NOTIFICACIONES ============
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ============ AUTENTICACIÓN ============
async function checkAuth() {
    try {
        const response = await fetch(`${API_URL}/me`, { credentials: 'include' });
        if (response.ok) {
            currentUser = await response.json();
            document.getElementById('navUsername').textContent = `👤 ${currentUser.username}`;
            document.getElementById('navAuthBtn').innerHTML = `<i class="fas fa-sign-out-alt"></i> Salir`;
            return true;
        }
    } catch (error) {
        console.log('No autenticado');
    }
    return false;
}

function toggleAuth() {
    if (currentUser) {
        logout();
    } else {
        openAuth();
    }
}

function openAuth() {
    document.getElementById('authModal').classList.add('show');
    document.getElementById('authModalTitle').textContent = 'Iniciar Sesión';
    document.getElementById('authSubmitBtn').innerHTML = '<i class="fas fa-sign-in-alt"></i> Iniciar Sesión';
    isLoginMode = true;
    document.getElementById('emailGroup').style.display = 'block';
    document.getElementById('toggleAuthBtn').textContent = '¿No tienes cuenta? Regístrate';
}

function closeAuth() {
    document.getElementById('authModal').classList.remove('show');
}

function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    document.getElementById('authModalTitle').textContent = isLoginMode ? 'Iniciar Sesión' : 'Registrarse';
    document.getElementById('authSubmitBtn').innerHTML = isLoginMode 
        ? '<i class="fas fa-sign-in-alt"></i> Iniciar Sesión' 
        : '<i class="fas fa-user-plus"></i> Registrarse';
    document.getElementById('toggleAuthBtn').textContent = isLoginMode 
        ? '¿No tienes cuenta? Regístrate' 
        : '¿Ya tienes cuenta? Inicia Sesión';
    document.getElementById('emailGroup').style.display = isLoginMode ? 'block' : 'block';
}

async function handleAuth(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    const endpoint = isLoginMode ? '/login' : '/register';
    const data = isLoginMode ? { username, password } : { username, email, password };
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            closeAuth();
            await checkAuth();
            await loadProducts();
            await loadCart();
            showToast(isLoginMode ? '✅ Sesión iniciada!' : '✅ Usuario registrado!', 'success');
        } else {
            showToast(`❌ ${result.error}`, 'error');
        }
    } catch (error) {
        showToast('❌ Error de conexión', 'error');
    }
}

async function logout() {
    try {
        await fetch(`${API_URL}/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        currentUser = null;
        document.getElementById('navUsername').textContent = 'Invitado';
        document.getElementById('navAuthBtn').innerHTML = '<i class="fas fa-sign-in-alt"></i> Entrar';
        await loadProducts();
        await loadCart();
        showToast('👋 Sesión cerrada', 'info');
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
    }
}

// ============ PRODUCTOS ============
async function loadProducts(category = 'all') {
    try {
        const url = category === 'all' 
            ? `${API_URL}/products` 
            : `${API_URL}/products?category=${category}`;
        
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        products = await response.json();
        document.getElementById('productsCount').textContent = `${products.length} productos`;
        renderProducts(products);
    } catch (error) {
        console.error('Error cargando productos:', error);
        document.getElementById('productGrid').innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 50px;">
                <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: #ff9800;"></i>
                <h3>Error al cargar productos</h3>
                <p style="color: #666;">${error.message}</p>
                <button onclick="loadProducts()" class="btn-primary" style="margin-top: 15px;">
                    <i class="fas fa-sync"></i> Reintentar
                </button>
            </div>
        `;
    }
}

function renderProducts(products) {
    const grid = document.getElementById('productGrid');
    grid.innerHTML = '';

    if (!products || products.length === 0) {
        grid.innerHTML = `
            <div style="grid-column: 1/-1; text-align: center; padding: 50px;">
                <i class="fas fa-box-open" style="font-size: 3rem; color: #888;"></i>
                <h3>No hay productos</h3>
                <p style="color: #666;">Vuelve más tarde</p>
            </div>
        `;
        return;
    }

    products.forEach(product => {
        const stockStatus = product.stock <= 0 ? 'agotado' : 
                           product.stock <= 5 ? 'ultimos' : '';
        const stockText = product.stock <= 0 ? 'Agotado' :
                         product.stock <= 5 ? `¡Últimas ${product.stock}!` : 
                         `${product.stock} disponibles`;

        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <div class="product-image">

            <img src="${product.image_url || '/images/goku-ui.jpg'}" 
            alt="${product.name}" 
            onerror="this.src='/images/goku-ui.jpg'">

                ${stockStatus ? `<span class="stock-badge ${stockStatus}">${stockStatus === 'agotado' ? 'Agotado' : '¡Últimas!'}</span>` : ''}
            </div>
            <div class="product-info">
                <h3>${product.name}</h3>
                <div class="product-category"><i class="fas fa-tag"></i> ${product.category}</div>
                <div class="product-price">$${product.price.toFixed(2)}</div>
                <div class="product-stock">${stockText}</div>
                <button class="btn-add" onclick="addToCart(${product.id})" ${product.stock <= 0 ? 'disabled' : ''}>
                    <i class="fas fa-cart-plus"></i> ${product.stock > 0 ? 'Añadir' : 'Agotado'}
                </button>
            </div>
        `;
        grid.appendChild(card);
    });
}

// ============ CARRITO ============
async function loadCart() {
    if (!currentUser) return;
    
    try {
        const response = await fetch(`${API_URL}/cart`, { credentials: 'include' });
        if (response.ok) {
            cart = await response.json();
            updateCartUI();
        }
    } catch (error) {
        console.error('Error cargando carrito:', error);
    }
}

async function addToCart(productId) {
    if (!currentUser) {
        showToast('⚠️ Debes iniciar sesión', 'info');
        openAuth();
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/cart`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_id: productId, quantity: 1 }),
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            cart = result;
            updateCartUI();
            const product = products.find(p => p.id === productId);
            showToast(`✅ ${product ? product.name : 'Producto'} añadido al carrito!`, 'success');
        } else {
            showToast(`❌ ${result.error || 'Error al añadir'}`, 'error');
        }
    } catch (error) {
        console.error('Error añadiendo al carrito:', error);
        showToast('❌ Error al añadir al carrito', 'error');
    }
}

function updateCartUI() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('navCartBadge').textContent = count;
}

async function openCart() {
    if (!currentUser) {
        showToast('⚠️ Debes iniciar sesión', 'info');
        openAuth();
        return;
    }
    
    try {
        await loadCart();
        
        const container = document.getElementById('cartItems');
        const totalSpan = document.getElementById('cartTotal');
        
        container.innerHTML = '';
        let total = 0;

        if (cart.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">🛒</div>
                    <h3>Carrito vacío</h3>
                    <p>Agrega productos para comenzar</p>
                </div>
            `;
        } else {
            cart.forEach(item => {
                const div = document.createElement('div');
                div.className = 'cart-item';
                div.innerHTML = `
                    <div class="cart-item-info">
                        <img src="${item.image_url || 'https://placehold.co//50x50'}" alt="${item.name}" class="cart-item-image">
                        <div>
                            <div class="cart-item-name">${item.name}</div>
                            <div class="cart-item-controls">
                                <button onclick="updateQuantity(${item.id}, ${item.quantity - 1})">−</button>
                                <span>${item.quantity}</span>
                                <button onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                            </div>
                        </div>
                    </div>
                    <div>
                        <div class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</div>
                        <button class="cart-item-remove" onclick="removeFromCart(${item.id})">×</button>
                    </div>
                `;
                container.appendChild(div);
                total += item.price * item.quantity;
            });
        }

        totalSpan.textContent = total.toFixed(2);
        document.getElementById('cartModal').classList.add('show');
    } catch (error) {
        console.error('Error abriendo carrito:', error);
        showToast('❌ Error al abrir el carrito', 'error');
    }
}

function closeCart() {
    document.getElementById('cartModal').classList.remove('show');
}

async function updateQuantity(itemId, newQuantity) {
    if (newQuantity < 0) return;
    
    try {
        const response = await fetch(`${API_URL}/cart/${itemId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ quantity: newQuantity }),
            credentials: 'include'
        });
        
        if (response.ok) {
            cart = await response.json();
            updateCartUI();
            await openCart();
        }
    } catch (error) {
        console.error('Error actualizando cantidad:', error);
    }
}

async function removeFromCart(itemId) {
    try {
        const response = await fetch(`${API_URL}/cart/${itemId}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        
        if (response.ok) {
            cart = await response.json();
            updateCartUI();
            await openCart();
        }
    } catch (error) {
        console.error('Error eliminando item:', error);
    }
}

// ============ CHECKOUT ============
function proceedToCheckout() {
    if (cart.length === 0) {
        showToast('⚠️ El carrito está vacío', 'info');
        return;
    }
    closeCart();
    document.getElementById('checkoutModal').classList.add('show');
}

function closeCheckout() {
    document.getElementById('checkoutModal').classList.remove('show');
}

async function processCheckout(event) {
    event.preventDefault();
    
    const shippingAddress = document.getElementById('shippingAddress').value;
    const paymentMethod = document.getElementById('paymentMethod').value;
    
    try {
        const response = await fetch(`${API_URL}/checkout`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ shipping_address: shippingAddress, payment_method: paymentMethod }),
            credentials: 'include'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            closeCheckout();
            cart = [];
            updateCartUI();
            await loadProducts();
            showToast(`🎉 ¡Compra #${result.order_id} realizada! Total: $${result.total.toFixed(2)}`, 'success');
        } else {
            showToast(`❌ ${result.error}`, 'error');
        }
    } catch (error) {
        console.error('Error en checkout:', error);
        showToast('❌ Error al procesar la compra', 'error');
    }
}

// ============ PEDIDOS ============
async function loadOrders() {
    if (!currentUser) {
        document.getElementById('ordersList').innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🔒</div>
                <h3>Inicia sesión</h3>
                <p>Para ver tus pedidos</p>
                <button class="btn-primary" onclick="openAuth()" style="margin-top: 15px;">
                    <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
                </button>
            </div>
        `;
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/orders`, { credentials: 'include' });
        if (!response.ok) throw new Error('Error al cargar pedidos');
        
        const orders = await response.json();
        const container = document.getElementById('ordersList');
        
        if (orders.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">📦</div>
                    <h3>No tienes pedidos</h3>
                    <p>¡Compra algo para empezar!</p>
                </div>
            `;
        } else {
            container.innerHTML = orders.map(order => `
                <div class="order-card">
                    <div class="order-header">
                        <span class="order-id">#${order.id}</span>
                        <span class="order-status status-${order.status}">${order.status}</span>
                    </div>
                    <div class="order-date">
                        <i class="far fa-calendar-alt"></i> ${new Date(order.created_at).toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                    </div>
                    <div class="order-items">
                        ${order.items.map(item => `
                            <div class="order-item">
                                <span>${item.product_name} × ${item.quantity}</span>
                                <span>$${item.subtotal.toFixed(2)}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="order-total">Total: $${order.total.toFixed(2)}</div>
                    <div style="font-size: 0.8rem; color: #888; margin-top: 8px;">
                        <i class="fas fa-truck"></i> ${order.shipping_address || 'Sin dirección'} 
                        · ${order.payment_method || 'Sin método de pago'}
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error cargando pedidos:', error);
        document.getElementById('ordersList').innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">❌</div>
                <h3>Error al cargar pedidos</h3>
                <button class="btn-primary" onclick="loadOrders()" style="margin-top: 15px;">
                    <i class="fas fa-sync"></i> Reintentar
                </button>
            </div>
        `;
    }
}

// ============ PERFIL ============
async function loadProfile() {
    if (!currentUser) {
        document.getElementById('profileContent').innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">🔒</div>
                <h3>Inicia sesión</h3>
                <p>Para ver tu perfil</p>
                <button class="btn-primary" onclick="openAuth()" style="margin-top: 15px;">
                    <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
                </button>
            </div>
        `;
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/orders`, { credentials: 'include' });
        const orders = response.ok ? await response.json() : [];
        
        document.getElementById('profileContent').innerHTML = `
            <div class="profile-avatar">👤</div>
            <div class="profile-name">${currentUser.username}</div>
            <div class="profile-email"><i class="fas fa-envelope"></i> ${currentUser.email}</div>
            <div class="profile-stats">
                <div class="stat-card">
                    <div class="stat-number">${orders.length}</div>
                    <div class="stat-label">Pedidos</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${cart.length}</div>
                    <div class="stat-label">Items en carrito</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${products.length}</div>
                    <div class="stat-label">Productos disponibles</div>
                </div>
            </div>
            <button class="btn-primary" onclick="logout()" style="margin-top: 20px;">
                <i class="fas fa-sign-out-alt"></i> Cerrar Sesión
            </button>
        `;
    } catch (error) {
        console.error('Error cargando perfil:', error);
    }
}

// ============ EVENTOS ============
document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCategory = btn.dataset.category;
        loadProducts(currentCategory);
    });
});

// ============ CIERRE DE MODALES ============
window.onclick = function(event) {
    const modals = ['authModal', 'cartModal', 'checkoutModal'];
    modals.forEach(id => {
        const modal = document.getElementById(id);
        if (event.target === modal) {
            modal.classList.remove('show');
        }
    });
};

// ============ INICIO ============
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Iniciando Tienda Otaku...');
    const authed = await checkAuth();
    await loadProducts();
    if (authed) {
        await loadCart();
    }
});
