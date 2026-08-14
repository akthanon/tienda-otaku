from database import get_db
from models import Product

# Mapeo de imágenes por nombre de producto
image_mapping = {
    "Figura Goku Ultra Instinct": "/images/goku-ui.jpg",
    "Manga One Piece Vol. 1 Edición Especial": "/images/onepiece.jpg",
    "Collar Sharingan": "/images/sharingan.jpg",
    "Figura Sailor Moon Edición Limitada": "/images/sailormoon.jpg",
    "Set de Postales Studio Ghibli": "/images/ghibli.jpg",
    "Manga Attack on Titan Box Set": "/images/aot.jpg",
    "Figura de Nezuko": "/images/nezuko.jpg",
    "Edición Coleccionista Evangelion": "/images/eva.jpg",
    "Figura de Goku SSJ Blue": "/images/goku-ui.jpg",  # Reutilizando imagen de Goku
    "Sword Art Online Figurine Asuna": "/images/asuna.jpg",
    "Peluche Totoro Gigante": "/images/totoro.jpg",
}

def update_product_images():
    db = get_db()
    
    # Obtener todos los productos
    products = db.query(Product).all()
    
    updated_count = 0
    for product in products:
        if product.name in image_mapping:
            old_image = product.image_url
            product.image_url = image_mapping[product.name]
            updated_count += 1
            print(f"✅ {product.name}: {old_image} → {product.image_url}")
        else:
            # Si no tiene imagen asignada, usar una imagen por defecto según categoría
            default_images = {
                "figuras": "/images/goku-ui.jpg",
                "mangas": "/images/onepiece.jpg",
                "accesorios": "/images/sharingan.jpg",
                "ediciones": "/images/eva.jpg"
            }
            product.image_url = default_images.get(product.category, "/images/goku-ui.jpg")
            updated_count += 1
            print(f"🔄 {product.name} (categoría: {product.category}): → {product.image_url}")
    
    db.commit()
    print(f"\n✅ {updated_count} productos actualizados con imágenes locales")
    db.close()

if __name__ == "__main__":
    update_product_images()
