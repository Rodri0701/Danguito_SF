from flask import Flask, Response, jsonify, request
from flask_restful import reqparse, Api, Resource, fields, marshal_with, abort
from api.models.userModel import UserModel, db
import json
import re

user_args = reqparse.RequestParser()
user_args.add_argument("userName", type=str, help="Name of the user is required", required=True)
user_args.add_argument("password", type=str, help="Password of the user is required", required=True)
user_args.add_argument("email", type=str, help="Email of the user is required", required=False)
user_args.add_argument("nombres", type = str, help="Name of the user is required", required=False)
user_args.add_argument("Ap_Paterno", type = str, help="Last name of the user is required", required=False)
user_args.add_argument("Ap_Materno", type = str, help="Last name of the user is required", required=False)
user_args.add_argument("celular", type = str, help="Cell phone of the user is required", required=False)
user_args.add_argument("direccion", type = str, help="Address of the user is required",required=False)
user_args.add_argument("rol", type = str)

#CAMPOS DE SALIDA
userFields={
    'userName': fields.String,
    'password': fields.String,
    'email': fields.String,
    'nombres': fields.String,
    'Ap_Paterno': fields.String,
    'Ap_Materno': fields.String,
    'celular': fields.String,
    'direccion': fields.String,
    
}

#CLASE PARA VER O AGREGAR USUARIOS  
class Users(Resource):
    #OBTENER USUARIOS
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        if not users:
            abort(404, message="No hay usuarios")
        return users,200
    
    #AGREGAR UN NUEVO USUARIO
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        #VALIDACIONES
        if not re.match(r"[^@]+@[^@]+\.[^@]+", args['email']):
            abort(400, message="El correo no es valido")
        if len(args['password']) < 8:
            abort(400, message="La contraseña debe tener al menos 8 caracteres")
        if not re.match(r"^[a-zA-Z\s]+$", args['nombres']):
            abort(400, message="El nombre solo puede contener letras")
        if not re.match(r"^[a-zA-Z\s]+$", args['Ap_Paterno']):
            abort(400, message="El apellido paterno solo puede contener letras")
        if not re.match(r"^[a-zA-Z\s]+$", args['Ap_Materno']):
            abort(400, message="El apellido materno solo puede contener letras")
        if not re.match(r"^[0-9]+$", args['celular']):
            abort(400, message="El celular solo puede contener numeros")
        if args['rol'] == 'Administrador':
            admin = UserModel.query.filter_by(rol='Administrador').first()
            if admin:
                abort(400, message="Ya existe un administrador")
        #rol por defecto es "clinete"
        if not args['rol']:
            args['rol'] = 'Cliente'
       #El correo ya existe.
        if UserModel.query.filter_by(email=args['email']).first():
            abort(400, message="El correo ya existe")

        #VERIFICAR SI EL USUARIO YA EXISTE
        user = UserModel.query.filter_by(userName=args['userName']).first()
        if user:
            abort(400, message="El usuario ya existe")

    

        #CREAR EL USUARIO
        user = UserModel(userName=args['userName'], password=args['password'], email=args['email'], nombres=args['nombres'], Ap_Paterno=args['Ap_Paterno'], Ap_Materno=args['Ap_Materno'], celular=args['celular'], direccion=args['direccion'], rol = args['rol'])
        db.session.add(user)
        db.session.commit()
        return jsonify ({"message": "Usuario creado con exito"}), 200


#CLASE PARA MOSTRAR, EDITAR O ELIMINAR A UN SOLO USUARIOS
class User(Resource):
    #OBTENER USUARIO
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(Cve_usuarios=id).first()
        if not user:
            abort(404, message="No se encontro el usuario")
        return user,200
    
    #ELIMINAR USUARIO
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(Cve_usuarios=id).first()
        if not user:
            abort(404, message="No se encontro el usuario")
        db.session.delete(user)
        db.session.commit()
        return Response(json.dumps({'message': 'Usuario eliminado'}), status=200, mimetype='application/json')

    #EDITAR USUARIO YA EXISTENTE
    @marshal_with(userFields)
    def put(self, id):
        # Buscar el usuario por su ID
        user = UserModel.query.filter_by(Cve_usuarios=id).first()

        # Verificar si el usuario existe
        if not user:
            abort(404, message="Usuario no encontrado")

        # Obtener los datos del cliente
        data = request.get_json()

        # Validar y actualizar campos
        if 'email' in data:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
                abort(400, message="El correo no es válido")
            user.email = data['email']

        if 'password' in data:
            if len(data['password']) < 8:
                abort(400, message="La contraseña debe tener al menos 8 caracteres")
            user.password = data['password']  # **Recuerda encriptarla**

        if 'nombres' in data:
            if not re.match(r"^[a-zA-Z\s]+$", data['nombres']):
                abort(400, message="El nombre solo puede contener letras")
            user.nombres = data['nombres']

        if 'Ap_Paterno' in data:
            if not re.match(r"^[a-zA-Z\s]+$", data['Ap_Paterno']):
                abort(400, message="El apellido paterno solo puede contener letras")
            user.Ap_Paterno = data['Ap_Paterno']

        if 'Ap_Materno' in data:
            if not re.match(r"^[a-zA-Z\s]+$", data['Ap_Materno']):
                abort(400, message="El apellido materno solo puede contener letras")
            user.Ap_Materno = data['Ap_Materno']

        if 'celular' in data:
            if not re.match(r"^[0-9]+$", data['celular']):
                abort(400, message="El celular solo puede contener números")
            user.celular = data['celular']

        if 'direccion' in data:
            user.direccion = data['direccion']

        # Confirmar cambios en la base de datos
        user.userName = data['userName']
        user.password = data['password']
        user.email = data['email']
        user.nombres = data['nombres']
        user.Ap_Paterno = data['Ap_Paterno']
        user.Ap_Materno = data['Ap_Materno']
        user.celular = data['celular']
        user.direccion = data['direccion']
        db.session.commit()
        return user, 200
    

      
        


#CLASE PARA INICIAR SESION DE UN USUARIO YA REGISTRADO
class Login(Resource):
    def post(self):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(userName=args['userName']).first()
        if not user:
            abort(404, message="No se encontro el usuario")
        if not user.check_password(args['password']):
            abort(400, message="Contraseña incorrecta")
        #si el rol es admin o si el rol es cliente
        if user.rol == 'admin' or user.rol == 'cliente':
            abort(400, message="Hola")
                        
        return Response(json.dumps({'message': 'Usuario logueado, Hola '+ ' ' +user.userName +' '+ user.rol}), status=200, mimetype='application/json')
       