from flask import Flask, Response
from flask_restful import reqparse, Api, Resource, fields, marshal_with, abort
from api.models.userModel import UserModel
from api.models.productModel import ProductoModel
from api.models.orderModel import OrderModel
from api.extension import db  # Asegúrate de importar db correctamente
import json
from datetime import datetime
# Argumentos para la creación de una nueva orden
order_args = reqparse.RequestParser()
order_args.add_argument("user_id", type=int, help="ID del usuario es requerido", required=True)
order_args.add_argument("product_id", type=int, help="ID del producto es requerido", required=True)
order_args.add_argument("cantidad", type=int, help="Cantidad es requerida", required=True)
order_args.add_argument("PrecioTotal", type=int, help="Precio total es requerido", required=True)
order_args.add_argument("FechaOrden", type=str, help="Fecha es requerida", required=True)
order_args.add_argument("status", type=str, help="Estado es requerido", required=True)

# Campos de salida
order_fields = {
    "user_id": fields.Integer,
    "product_id": fields.Integer,
    "cantidad": fields.Integer,
    "PrecioTotal": fields.Integer,
    "FechaOrden": fields.DateTime,
    "status": fields.String
}

# Clase para ver o agregar órdenes
class Orders(Resource):
    @marshal_with(order_fields)
    def get(self):
        orders = OrderModel.query.all()
        return orders, 200

    @marshal_with(order_fields)
    def post(self):
        args = order_args.parse_args()
        
        # Verificar si el usuario existe
        user = UserModel.query.filter_by(Cve_usuarios=args["user_id"]).first()
        if not user:
            abort(404, message="Usuario no encontrado con id {}".format(args["user_id"]))
        
        # Verificar si el producto existe
        product = ProductoModel.query.filter_by(Cve_Productos=args["product_id"]).first()
        if not product:
            abort(404, message="Producto no encontrado con id {}".format(args["product_id"]))
        
        # Verificar si hay suficiente stock
        if product.stock < args["cantidad"]:
            abort(400, message="No hay suficiente stock para el producto {}".format(args["product_id"]))
        
        # Convertir la cadena de la fecha a un objeto datetime
        FechaOrden = datetime.strptime(args["FechaOrden"], "%Y-%m-%dT%H:%M:%S")
        
        # Crear la orden
        order = OrderModel(
            user_id=args["user_id"],
            product_id=args["product_id"],
            cantidad=args["cantidad"],
            PrecioTotal=args["PrecioTotal"],
            FechaOrden=FechaOrden,
            status=args["status"]
        )
        
        # Reducir el stock
        product.stock -= args["cantidad"]
        
        # Guardar los cambios
        db.session.add(order)
        db.session.commit()
        
        # Guardar los cambios en el producto
        db.session.commit()

        return order, 201

# CLASE PARA VER, BORRAR O EDITAR UNA SOLA ORDEN
class Order(Resource):
    @marshal_with(order_fields)
    def get(self, id):
        order = OrderModel.query.filter_by(idOrden=id).first()
        if not order:
            abort(404, message="Orden no encontrada con id {}".format(id))
        return order, 200

    @marshal_with(order_fields)
    def put(self, id):
        args = order_args.parse_args()
        order = OrderModel.query.filter_by(idOrden=id).first()
        if not order:
            abort(404, message="Orden no encontrada con id {}".format(id))
        # Verificar si el usuario existe
        user = UserModel.query.filter_by(Cve_usuarios=args["user_id"]).first()
        if not user:
            abort(404, message="Usuario no encontrado con id {}".format(args["user_id"]))
        
        # Verificar si el producto existe
        product = ProductoModel.query.filter_by(Cve_Productos=args["product_id"]).first()
        if not product:
            abort(404, message="Producto no encontrado con id {}".format(args["product_id"]))
        
        # Verificar si hay suficiente stock
        if product.stock < args["cantidad"]:
            abort(400, message="No hay suficiente stock para el producto {}".format(args["product_id"]))
        
        # Convertir la cadena de la fecha a un objeto datetime
        FechaOrden = datetime.strptime(args["FechaOrden"], "%Y-%m-%dT%H:%M:%S")
        
        order.user_id = args["user_id"]
        order.product_id = args["product_id"]
        order.cantidad = args["cantidad"]
        order.PrecioTotal = args["PrecioTotal"]
        order.FechaOrden = FechaOrden
        order.status = args["status"]
        db.session.commit()
        return order, 200

    def delete(self, id):
        order = OrderModel.query.filter_by(idOrden=id).first()
        if not order:
            abort(404, message="Orden no encontrada con id {}".format(id))
        db.session.delete(order)
        db.session.commit()
        return Response(json.dumps({"message": "Orden eliminada con éxito"}), status=200, mimetype="application/json")