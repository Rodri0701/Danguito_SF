from flask import Flask, Response, request
from flask_restful import reqparse, Api, Resource, fields, marshal_with, abort
from api.models.listaModel import db, ListDeseoModel
import json
import re

listaDeseo_arg = reqparse.RequestParser()
listaDeseo_arg.add_argument('id', type=int, required=False, help='id is required')
listaDeseo_arg.add_argument('user_id', type=int, required=True, help='user_id is required')
listaDeseo_arg.add_argument('product_id', type=int, required=True, help='product_id is required')

#CAPOS DE SALIDA
listaDeseo_fields = {
    'user_id': fields.Integer,
    'product_id': fields.Integer
}

#CLASE PARA VER O AGREGAR LISTA DE DESEOS
class ListasDeseos(Resource):
    #VER LOS PRODUCTOS EN LA LISTA
    @marshal_with(listaDeseo_fields)
    #VER TODOS LOS PRODUCTOS EN LA LISTA
    def get(self):
        listaDeseo = ListDeseoModel.query.all()
        if not listaDeseo:
            return {'message': 'La lista esta vacia'}, 404
        return listaDeseo, 200
    #AGREGAR PRODUCTOS A LA LISTA
    @marshal_with(listaDeseo_fields)
    def post(self):
        args = listaDeseo_arg.parse_args()
        listaDeseo = ListDeseoModel(user_id=args['user_id'], product_id =args['product_id'])
        db.session.add(listaDeseo)
        db.session.commit()
        return listaDeseo, 201
    
#CLASE PARA VER, ELIMINAR O EDITAR UNA LISTA DE DESEOS
class ListaDeseo(Resource):
    #VER UN PRODUCTO EN LA LISTA
    @marshal_with(listaDeseo_fields)
    def get(self, id):
        listaDeseo = ListDeseoModel.query.get(id)
        if listaDeseo is None:
            abort(404, message="Producto no encontrado")
        return listaDeseo, 200
    #Eliminar un producto de la lista
    @marshal_with(listaDeseo_fields)
    def delete(self, id):
        listaDeseo = ListDeseoModel.query.filter_by(id=id).first()
        if listaDeseo is None:
            abort(404, message="Producto no encontrado")
        db.session.delete(listaDeseo)
        db.session.commit()
        return Response(json.dumps({'message': 'Producto eliminado'}), status=200, mimetype='application/json')
    #EDITAR UN PRODUCTO DE LA LISTA
    @marshal_with(listaDeseo_fields)
    def put(self, id):
        listaDeseo = ListDeseoModel.query.get(id)
        if listaDeseo is None:
            abort(404, message="Producto no encontrado")
        args = listaDeseo_arg.parse_args()
        listaDeseo.user_id = args['user_id']
        listaDeseo.product_id = args['product_id']
        db.session.commit()
        return listaDeseo, 200