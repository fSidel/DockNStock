from os import environ
from flask import Flask
from database import db
from models import Users, Products
from routes.user import user_bp
from routes.product import product_bp
from routes.like import like_bp
from routes.comment import comment_bp
from routes.supermarket import supermarket_bp
from routes.owns import owns_bp
from routes.wants import wants_bp

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@db:5432/appdb"

db.init_app(app)  
with app.app_context():
    db.create_all()
    #add elements only if products table is 
    """ if not Products.query.first():
        products = [
        Products(name="Mele", weight="1kg", photo="https://www.laboutiquedelbiologico.it/4860-medium_default/mele-stark-biologiche-500-g.jpg", description="Mele rosse"),
        Products(name="Banane", weight="1kg", photo="https://www.focus.it/site_stored/imgs/0005/030/banane.1020x680.jpg", description="Banane"),
        Products(name="Pomodori", weight="500g", photo="https://media.istockphoto.com/id/847335116/it/foto/pomodori-sulla-vite.jpg?s=612x612&w=0&k=20&c=c0A6VYC9KHH02u2n_THcFcVztvQU2mAKUPVbnIw2cGo=", description="Pomodori"),
        Products(name="Carne Macinata", weight="500g", photo="https://media.istockphoto.com/id/488387982/it/foto/carne-macinata.jpg?s=612x612&w=0&k=20&c=gma4bgvxYJvvW0u-BsXvVOIyMf7TalFQITzbP9hNHpo=", description="Carne bovina macinata fresca"),
        Products(name="Petto di Pollo", weight="500g", photo="https://dalfcarnishoponline.it/wp-content/uploads/2021/12/DALF-Petto-di-pollo-a-fette.jpg", description="Filetti di petto di pollo"),
        Products(name="Parmigiano", weight="200g", photo="https://parmigianoreggiano.museidelcibo.it/wp-content/uploads/sites/2/2021/05/83.07-A-SCUOLA-DI-CIBO.jpg", description="Parmigiano Reggiano stagionato 24 mesi"),
        Products(name="Uova", weight="6pz", photo="https://media.istockphoto.com/id/451505631/it/foto/due-uova-isolato-su-bianco.jpg?s=612x612&w=0&k=20&c=G3QO1WmURmmRI5w0DZBYLB1GUl9eKW5IGpjh12-VjsY=", description="Uova biologiche"),
        Products(name="Latte", weight="1L", photo="https://www.papilla.net/img/prodotti/833x1000_foto-latte-fresco-intero-alta-qualita.webp", description="Latte intero pastorizzato"),
        Products(name="Burro", weight="250g", photo="https://media.istockphoto.com/id/177834117/it/foto/burro-isolato-su-bianco.jpg?s=612x612&w=0&k=20&c=tDFnTtDS54Yl2jv4aX_arbXv7NvhZBd8SERQuJQ_yGg=", description="Burro fresco"),
        Products(name="Pane", weight="500g", photo="https://img.freepik.com/foto-premium/pane-confezionato-in-carta-su-tavola-di-legno_491799-11045.jpg", description="Pane fresco di giornata"),
        Products(name="Pasta", weight="1kg", photo="https://img.freepik.com/foto-gratuito/pasta-cruda_58702-1343.jpg", description="Pasta di semola di grano duro"),
        Products(name="Riso", weight="1kg", photo="https://www.ristorantedalele.it/wp-content/uploads/2022/01/Le-origini-del-riso1.jpg", description="Riso per risotti"),
        Products(name="Cous Cous", weight="500g", photo="https://www.giallozafferano.it/images/ricette/5/572/foto_hd/hd650x433_wm.jpg", description="Cous cous"),
        Products(name="Farina", weight="1kg", photo="https://www.molinosquillario.it/wp-content/uploads/2019/11/manitoba-farina.jpg", description="Farina di grano tenero tipo 00"),
        Products(name="Biscotti", weight="400g", photo="https://www.lacucinaimperfetta.com/wp-content/uploads/2013/10/Biscotti-al-burro.jpg", description="Biscotti al burro"),
        Products(name="Olio EVO", weight="750ml", photo="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Olive_Oil_%28Unsplash%29.jpg/1200px-Olive_Oil_%28Unsplash%29.jpg", description="Olio extravergine d'oliva italiano"),
        Products(name="Zucchero", weight="1kg", photo="https://media.istockphoto.com/id/1420446362/it/foto/zucchero-semolato-bianco-e-zollette-di-zucchero-raffinato-in-primo-piano-in-cucina.jpg?s=612x612&w=0&k=20&c=K7bCoYILF0mPtKClgNoeYlMmMM1HNl3mvanVq-JMduM=", description="Zucchero bianco raffinato"),
        Products(name="Sale", weight="1kg", photo="https://media.istockphoto.com/id/1051727580/it/foto/cristalli-di-sale-poco-profondo-in-una-pallina-cucchiaio-su-un-tavolo-grigio-scuro-sfondo-per.jpg?s=612x612&w=0&k=20&c=AJTPsqit4_VD-panxXrOZMSgaYr2ulU1-U5jkBPp-mE=", description="Sale marino fino"),
        Products(name="Caffè", weight="250g", photo="https://shop.torrefazionexcelsior.it/themes/Blulab201508/img/_p/570w/11-caffe-macinato-cucchiaio.jpg", description="Caffè macinato"),
        Products(name="Acqua Naturale", weight="1.5L", photo="https://www.bordopalermo.it/public/images/acqua%20no%20logo.jpg", description="Acqua minerale naturale"),
        Products(name="Aranciata", weight="1.5L", photo="https://media.istockphoto.com/id/1460988855/it/foto/succo-darancia-in-una-bottiglia-di-vetro.jpg?s=612x612&w=0&k=20&c=D0r7qTeaslWhf1npfqfzi4Pi94N3NvwgVUGa9bKNnkI=", description="Bevanda analcolica all'arancia")
        ]
        db.session.add_all(products)
        db.session.commit()
        print("✅ Prodotti inseriti nel database.") """

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(like_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(supermarket_bp)
app.register_blueprint(owns_bp)
app.register_blueprint(wants_bp)


