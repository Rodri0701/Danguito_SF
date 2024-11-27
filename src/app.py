from flask import Flask
from flask_restful import Api
from api.extension import db
from src.api.controllers.controllerUser import Users, User, Login  #CONTROLADORES PARA LOS USUARIOS
from src.api.controllers.controllerProduct import Products, Product #CONTROLADORES PARA LOS PRODUCTOS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DANGUITO.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

#RUTAS PARA EL API USERS
api.add_resource(Users, '/api/User/') #RUTA PARA VER TODOS LOS USUARIOS  Y AGREGAR NUEVOS
api.add_resource(User, '/api/User/<int:id>') #RUTA PARA VER, EDITAR O ELIMINAR UN USUARIO
api.add_resource(Login, '/api/Login/') #RUTA PARA INICIAR SESION

#RUTAS PARA EL API PRODUCTS
api.add_resource(Products, '/api/Product/') #RUTA PARA VER TODOS LOS PRODUCTOS Y AGREGAR NUEVOS
api.add_resource(Product, '/api/Product/<int:id>') #RUTA PARA VER, EDITAR O ELIMINAR UN PRODUCTO

#RUTAS PARA ORDENES





@app.route('/')
def index():
    return '<h1> BIENVENIDO A DANGUITO SF <h1>'

if __name__ == '__main__':
    app.run(debug=True)