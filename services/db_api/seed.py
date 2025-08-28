# seed.py

from app import app, db
from models import Products

def seed_products():
    products = [
        Products(name="Latte", weight="1L", photo="latte.jpg", description="Latte intero pastorizzato"),
        Products(name="Pane", weight="500g", photo="pane.jpg", description="Pane fresco di giornata"),
        Products(name="Pasta", weight="1kg", photo="pasta.jpg", description="Pasta di semola di grano duro"),
        Products(name="Riso", weight="1kg", photo="riso.jpg", description="Riso carnaroli per risotti"),
        Products(name="Olio EVO", weight="750ml", photo="olio.jpg", description="Olio extravergine d'oliva italiano"),
        Products(name="Uova", weight="6pz", photo="uova.jpg", description="Uova biologiche"),
        Products(name="Zucchero", weight="1kg", photo="zucchero.jpg", description="Zucchero bianco raffinato"),
        Products(name="Sale", weight="1kg", photo="sale.jpg", description="Sale marino fino"),
        Products(name="Farina", weight="1kg", photo="farina.jpg", description="Farina di grano tenero tipo 00"),
        Products(name="Burro", weight="250g", photo="burro.jpg", description="Burro fresco da panna di centrifuga"),
        Products(name="Cous Cous", weight="500g", photo="https://www.giallozafferano.it/images/ricette/5/572/foto_hd/hd650x433_wm.jpg", description="Cous cous integrale")
    ]

    with app.app_context():
        db.session.bulk_save_objects(products)
        db.session.commit()
        print("✅ Prodotti inseriti nel database.")

if __name__ == "__main__":
    print("Inizio inserimento prodotti nel database...")
    seed_products()
