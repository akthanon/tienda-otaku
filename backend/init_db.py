from database import get_db, init_db
from models import Product

def init_products():
    db = get_db()
    
    # Verificar si ya hay productos
    if db.query(Product).count() > 0:
        print("✅ Base de datos ya inicializada")
        return
    
    # Productos con imágenes locales
    products = [
        Product(
            name="Figura Goku Ultra Instinct",
            price=45.99,
            category="figuras",
            image_url="/images/goku-ui.jpg",
            description="Figura de Goku en modo Ultra Instinct - Edición limitada",
            stock=10
        ),
        Product(
            name="Manga One Piece Vol. 1 Especial",
            price=19.99,
            category="mangas",
            image_url="/images/onepiece.jpg",
            description="Primer volumen de One Piece con cubierta holográfica",
            stock=15
        ),
        Product(
            name="Collar Sharingan",
            price=12.50,
            category="accesorios",
            image_url="/images/sharingan.jpg",
            description="Collar plateado con diseño Sharingan de Naruto",
            stock=20
        ),
        # ... más productos
    ]
    
    db.add_all(products)
    db.commit()
    print(f"✅ {len(products)} productos inicializados")
    db.close()

if __name__ == "__main__":
    init_db()
    init_products()
