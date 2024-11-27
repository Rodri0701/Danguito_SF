from flask import Flask, Response, request
from flask_restful import reqparse, Api, Resource, fields, marshal_with, abort
from api.models.comentarios import db, ReseñaModel
import json
import re

comentario_arg = reqparse.RequestParser()
comentario_arg.add_argument('Cve_comentarios', type=int, required=False, help='id is required')
comentario_arg.add_argument('producto_id', type=int, required=True, help='product id is required')
comentario_arg.add_argument('user_id', type=int, required=True, help='user id is required')
comentario_arg.add_argument('calificacion', type=int, required=True, help='puntuacion is required')
comentario_arg.add_argument('comentario', type=str, required=True, help='comentario is required')

#CAPOS DE SALIDA
comentarioFieds ={
    'producto_id': fields.Integer,
    'user_id': fields.Integer,
    'calificacion': fields.Integer,
    'comentario': fields.String
}

#CLASE PARA VER O AGREGAR COMENTARIOS
class Comentarios(Resource):
    #VER LOS COMENTARIOS
    @marshal_with(comentarioFieds)
    #VER TODOS LOS COMENTARIOS
    def get(self):
        comentarios = ReseñaModel.query.all()
        if not comentarios:
            return {'message': 'No hay comentarios'}, 404
        return comentarios, 200
    #AGREGAR UN COMENTARIO
    @marshal_with(comentarioFieds)
    def post(self):
        args = comentario_arg.parse_args()
        comentario = ReseñaModel(args['producto_id'], args['user_id'], args['calificacion'], args['comentario'])
        db.session.add(comentario)
        db.session.commit()
        return comentario, 201
    
#CLASE PARA VER, EDITAR O ELIMINAR UN COMENTARIO
class Comentario(Resource):
    #VER UN COMENTARIO
    @marshal_with(comentarioFieds)
    def get(self, id):
        comentario = ReseñaModel.query.filter_by(Cve_comentarios=id).first()
        if not comentario:
            return {'message': 'No existe el comentario'}, 404
        return comentario, 200
    #EDITAR UN COMENTARIO
    @marshal_with(comentarioFieds)
    def put(self, id):
        args = comentario_arg.parse_args()
        comentario = ReseñaModel.query.filter_by(Cve_comentarios=id).first()
        if not comentario:
            return {'message': 'No existe el comentario'}, 404
        comentario.producto_id = args['producto_id']
        comentario.user_id = args['user_id']
        comentario.calificacion = args['calificacion']
        comentario.comentario = args['comentario']
        db.session.commit()
        return comentario, 200
    #ELIMINAR UN COMENTARIO
    def delete(self, id):
        comentario = ReseñaModel.query.filter_by(Cve_comentarios=id).first()
        if not comentario:
            return {'message': 'No existe el comentario'}, 404
        db.session.delete(comentario)
        db.session.commit()
        return {'message': 'Comentario eliminado'}, 200