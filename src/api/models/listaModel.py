from ..extension import db


#CLASE PARA LISTA DE DESEOS
class  ListDeseoModel(db.Model):
    __tablename__ = 'listDeseo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Usr.Cve_usuarios'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('productos.Cve_Productos'), nullable=False)
    user = db.relationship('UserModel', backref='listDeseo', lazy=True)
    product = db.relationship('ProductoModel', backref='listDeseo', lazy=True)

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return f"Lista de deseos (user_id = {self.user_id}, product_id = {self.product_id})"

