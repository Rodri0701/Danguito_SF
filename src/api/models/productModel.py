from ..extension import db

class ProductoModel(db.Model):
    __tablename__ = 'productos'
    Cve_Productos = db.Column(db.Integer, primary_key=True) 
    nombreProducto = db.Column(db.String(100), nullable=False, unique= True)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    

    #CONTRUCTOR
    def __init__(self, nombreProducto, precio, descripcion, categoria, stock):
        self.nombreProducto = nombreProducto
        self.precio = precio
        self.descripcion = descripcion
        self.categoria = categoria
        self.stock = stock

    #Representacion del modelo
    def __repr__(self):
        return f"Producto (nombreProducto = {self.nombreProducto}, precio = {self.precio}, descripcion = {self.descripcion}, categoria = {self.categoria}, stock = {self.stock})"
    

