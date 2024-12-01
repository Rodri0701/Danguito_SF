from flask import Flask, Response, request
from flask_restful import reqparse, Api, Resource, fields, marshal_with, abort
from api.models.productModel import db, ProductoModel
import json
import re

product_arg = parse = reqparse.RequestParser()
product_arg.add_argument('Cve_Productos', type=int, required=False, help='id is required')
product_arg.add_argument('nombreProducto', type=str, required=True, help='name is required')
product_arg.add_argument('precio', type=int, required=True, help='price is required')
product_arg.add_argument('descripcion', type=str, required=False, help='description is required')
product_arg.add_argument('categoria', type=str, required=True, help='category is required')
product_arg.add_argument('stock', type=int, required=True, help='stock is required')
product_arg.add_argument('imagen', type=str, required=False, help='image is required')

#CAMPOS DE SALIDA.
productFields={
    'nombreProducto': fields.String,
    'precio': fields.Integer,
    'descripcion': fields.String,
    'categoria': fields.String,
    'stock': fields.Integer,
    'imagen': fields.String
}   

#CLASE PARA VER O AGREGAR PRODUCTOS
class Products(Resource):
    #VER LOS PRODUCTOS
    @marshal_with(productFields)
    #VER TODOS LOS PRODUCTOS
    def get(self):
        productos = ProductoModel.query.all()
        if not productos:
            return {'message': 'No hay productos'}, 404
        return productos, 200

#AGREGAR PRODUCTOS:
    @marshal_with(productFields)
    def post(self):
        productos = product_arg.parse_args()
        #VALIDACIONES.
        #El nombre del producto ya existe.
        if ProductoModel.query.filter_by(nombreProducto=productos['nombreProducto']).first():
            abort(400, message="El producto ya existe")
        #El precio no puede ser negativo.
        if productos['precio'] < 0:
            abort(400, message="El precio no puede ser negativo")
        #El stock no puede ser negativo.
        if productos['stock'] < 0:
            abort(400, message="El stock no puede ser negativo")
        #La categoria no puede estar vacia.
        if not productos['categoria']:
            abort(400, message="La categoria no puede estar vacia")
        #La categoria solo puede contener letras.
        if not re.match(r"^[a-zA-Z\s]+$", productos['categoria']):
            abort(400, message="La categoria solo puede contener letras")
        #El precio solo deben ser números
        if not re.match(r"^[0-9]+$", str(productos['precio'])):
            abort(400, message="El precio solo debe ser un número")
            #El stock solo deben ser números
        if not re.match(r"^[0-9]+$", str(productos['stock'])):
            abort(400, message="El stock solo debe ser un número")
        
        #CREAR PRODUCTO
        producto = ProductoModel(nombreProducto=productos['nombreProducto'], precio=productos['precio'], descripcion=productos['descripcion'], categoria=productos['categoria'], stock=productos['stock'], imagen=productos['imagen'])
        db.session.add(producto)
        db.session.commit()
        return producto, 201
    
#CLASE PARA VER, ACTUALIZAR O BORRAR UN PRODUCTO
class Product(Resource):
    @marshal_with(productFields)
    #VER UN PRODUCTO
    def get(self, id):
        producto = ProductoModel.query.get(id)
        if producto is None:
            abort(404, message="Producto no encontrado")
        return producto, 200
    
    #Eliminar un producto
    @marshal_with(productFields)
    def delete(self, id):
        producto = ProductoModel.query.filter_by(Cve_Productos=id).first()
        if producto is None:
            abort(404, message="Producto no encontrado")
        db.session.delete(producto)
        db.session.commit()
        return Response(json.dumps({'message': 'Producto eliminado'}), status=200, mimetype='application/json')
        
    #EDITAR UN PRODUCTO
    @marshal_with(productFields)
    def put(self, id):
        producto = ProductoModel.query.get(id)
        if producto is None:
            abort(404, message="Producto no encontrado")
        productos = product_arg.parse_args()
        #VALIDACIONES.
        #El precio no puede ser negativo.
        if productos['precio'] < 0:
            abort(400, message="El precio no puede ser negativo")
        #El stock no puede ser negativo.
        if productos['stock'] < 0:
            abort(400, message="El stock no puede ser negativo")
        #La categoria no puede estar vacia.
        if not productos['categoria']:
            abort(400, message="La categoria no puede estar vacia")
        #La categoria solo puede contener letras.
        if not re.match(r"^[a-zA-Z\s]+$", productos['categoria']):
            abort(400, message="La categoria solo puede contener letras")
        #El precio solo deben ser números
        if not re.match(r"^[0-9]+$", str(productos['precio'])):
            abort(400, message="El precio solo debe ser un número")
            #El stock solo deben ser números
        if not re.match(r"^[0-9]+$", str(productos['stock'])):
            abort(400, message="El stock solo debe ser un número")

        producto.nombreProducto = productos['nombreProducto']
        producto.precio = productos['precio']
        producto.descripcion = productos['descripcion']
        producto.categoria = productos['categoria']
        producto.stock = productos['stock']
        producto.imagen = productos['imagen']
        db.session.commit()
        return producto, 200