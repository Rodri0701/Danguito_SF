from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from api.extension import db
from src.api.controllers.controllerUser import Users, User, Login  #CONTROLADORES PARA LOS USUARIOS
from src.api.controllers.controllerProduct import Product, Products #CONTROLADORES PARA LOS PRODUCTOS
from src.api.controllers.controllerOrder import Orders, Order #CONTROLADORES PARA LAS ORDENES
from src.api.controllers.controllerLista import ListasDeseos, ListaDeseo #CONTROLADORES PARA LAS LISTAS
from src.api.controllers.controllerComentary import Comentarios, Comentario #CONTROLADORES PARA LOS COMENTARIOS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DANGUITO.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)


CORS(app)


#RUTAS PARA EL API USERS
api.add_resource(Users, '/api/User/') #RUTA PARA VER TODOS LOS USUARIOS  Y AGREGAR NUEVOS
api.add_resource(User, '/api/User/<int:id>') #RUTA PARA VER, EDITAR O ELIMINAR UN USUARIO
api.add_resource(Login, '/api/Login/') #RUTA PARA INICIAR SESION

#RUTAS PARA EL API PRODUCTS
api.add_resource(Products, '/api/Product/') #RUTA PARA VER TODOS LOS PRODUCTOS Y AGREGAR NUEVOS
api.add_resource(Product, '/api/Product/<int:id>') #RUTA PARA VER, EDITAR O ELIMINAR UN PRODUCTO

#RUTAS PARA ORDENES
api.add_resource(Orders, '/api/Order/') #RUTA PARA VER TODAS LAS ORDENES Y AGREGAR NUEVAS
api.add_resource(Order, '/api/Order/<int:id>') #RUTA PARA VER, EDITAR O ELIMINAR UNA ORDEN

#RUTAS PARA LISTAS
api.add_resource(ListasDeseos, '/api/Lista/') #RUTA PARA VER TODAS LAS LISTAS Y AGREGAR NUEVAS
api.add_resource(ListaDeseo, '/api/Lista/<int:id>') #RUTA PARA VER, EDITAR O ELIMINAR UNA LISTA

#RUTAS PARA COMENTARIOS
api.add_resource(Comentarios, '/api/Comentario/') #RUTA PARA VER TODOS LOS COMENTARIOS Y AGREGAR NUEVOS
api.add_resource(Comentario, '/api/Comentario/<int:id>') #RUTA PARA VER, EDITAR O ELIMINAR UN COMENTARIO

@app.route('/')
def index():
    return '<h1> BIENVENIDO A DANGUITO SF <h1>'

if __name__ == '__main__':
    app.run(debug=True)