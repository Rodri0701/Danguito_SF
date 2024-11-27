from ..extension import db


class OrderModel(db.Model):
    __tablename__ = "ordenes"

    idOrden = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    PrecioTotal = db.Column(db.Integer, nullable=False)
    FechaOrden = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(20), nullable=False)


#CONSTRUCTOR
    def __init__(self, user_id, product_id, cantidad, PrecioTotal,FechaOrden ,status):
        self.user_id = user_id
        self.product_id = product_id
        self.cantidad = cantidad
        self.PrecioTotal = PrecioTotal
        self.FechaOrden = FechaOrden
        self.status = status
    
    def __repr__(self):
        return f"Orden (user_id = {self.user_id}, product_id = {self.product_id}, cantidad = {self.cantidad}, PrecioTotal = {self.PrecioTotal}, FechaOrden = {self.FechaOrden}, status = {self.status})"