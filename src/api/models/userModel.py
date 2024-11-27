from ..extension import db
from .orderModel import OrderModel
from bcrypt import checkpw, gensalt, hashpw


class UserModel(db.Model):
    __tablename__ = 'Usr'
    Cve_usuarios = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    nombres = db.Column(db.String(250), nullable=False)
    Ap_Paterno = db.Column(db.String(250), nullable=False)
    Ap_Materno = db.Column(db.String(250), nullable=False)
    celular = db.Column(db.String(10), nullable=False)
    direccion = db.Column(db.String(250), nullable=False)
    rol = db.Column(db.String(100), default='Cliente')

    # Constructor
    def __init__(self, userName, password, email, nombres, Ap_Paterno, Ap_Materno, celular, direccion, rol='Cliente'):
        self.userName = userName
        self.email = email
        self.nombres = nombres
        self.Ap_Paterno = Ap_Paterno
        self.Ap_Materno = Ap_Materno
        self.celular = celular
        self.direccion = direccion
        self.rol = rol
        self.set_password(password)  # Encriptar contraseña directamente al crear el usuario

    # Método para encriptar la contraseña
    def set_password(self, password):
        self.password = hashpw(password.encode('utf8'), gensalt()).decode('utf8')

    # Método para verificar la contraseña
    def check_password(self, password):
        return checkpw(password.encode('utf8'), self.password.encode('utf8'))

    # Representación del modelo
    def __repr__(self):
        return f"Usuario (userName = {self.userName}, email = {self.email})"
