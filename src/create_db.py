from app import app, db
from api.models.userModel import UserModel
from api.models.productModel import ProductoModel
from api.models.listaModel import ListDeseoModel
from api.models.comentarios import ReseñaModel


with app.app_context():
    db.create_all()
    print("Base de datos creada")