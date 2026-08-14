from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
import os

DATABASE_PATH = os.environ.get('DATABASE_PATH', 'otaku_store.db')
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    return SessionLocal()

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = get_db()
    from models import Product
    
    if db.query(Product).count() == 0:
        # Productos con imágenes LOCALES
        sample_products = [
            Product(
                name="Figura Goku Ultra Instinct",
                price=45.99,
                category="figuras",
                image_url="/images/goku-ui.jpg",  # ← CAMBIADO A LOCAL
                description="Figura de Goku en modo Ultra Instinct - Edición limitada",
                stock=10
            ),
            Product(
                name="Manga One Piece Vol. 1 Especial",
                price=19.99,
                category="mangas",
                image_url="/images/onepiece.jpg",  # ← CAMBIADO A LOCAL
                description="Primer volumen de One Piece con cubierta holográfica",
                stock=15
            ),
            Product(
                name="Collar Sharingan",
                price=12.50,
                category="accesorios",
                image_url="/images/sharingan.jpg",  # ← CAMBIADO A LOCAL
                description="Collar plateado con diseño Sharingan de Naruto",
                stock=20
            ),
            Product(
                name="Figura Sailor Moon Limitada",
                price=89.99,
                category="ediciones",
                image_url="/images/sailormoon.jpg",  # ← CAMBIADO A LOCAL
                description="Figura coleccionable de Sailor Moon con base especial",
                stock=5
            ),
            Product(
                name="Set Postales Studio Ghibli",
                price=8.99,
                category="accesorios",
                image_url="/images/ghibli.jpg",  # ← CAMBIADO A LOCAL
                description="Set de 10 postales de películas de Studio Ghibli",
                stock=30
            ),
            Product(
                name="Attack on Titan Box Set",
                price=79.99,
                category="mangas",
                image_url="/images/aot.jpg",  # ← CAMBIADO A LOCAL
                description="Caja con los primeros 5 volúmenes de Attack on Titan",
                stock=8
            ),
            Product(
                name="Figura Nezuko Kamado",
                price=54.99,
                category="figuras",
                image_url="/images/nezuko.jpg",  # ← CAMBIADO A LOCAL
                description="Figura de Nezuko de Demon Slayer con efectos de luz",
                stock=12
            ),
            Product(
                name="Evangelion Box Set Coleccionista",
                price=129.99,
                category="ediciones",
                image_url="/images/eva.jpg",  # ← CAMBIADO A LOCAL
                description="Box set de Evangelion con artbook y figuras",
                stock=3
            ),
            Product(
                name="Sword Art Online Figurine Asuna",
                price=69.99,
                category="figuras",
                image_url="/images/asuna.jpg",  # ← CAMBIADO A LOCAL
                description="Figura de Asuna de Sword Art Online en traje de batalla",
                stock=7
            ),
            Product(
                name="Peluche Totoro Gigante",
                price=35.99,
                category="accesorios",
                image_url="/images/totoro.jpg",  # ← CAMBIADO A LOCAL
                description="Peluche suave de Totoro de 40cm",
                stock=15
            ),
        ]
        
        db.add_all(sample_products)
        db.commit()
        print(f"✅ {len(sample_products)} productos creados con imágenes locales")
    
    db.close()
