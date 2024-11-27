from ..extension import db


#CLASE PARA LISTA DE DESEOS
class  ListDeseoModel(db.Model):
    __tablename__ = 'listDeseo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    

    def __init__(self, user_id, product_id):
        self.user_id = user_id
        self.product_id = product_id

    def __repr__(self):
        return f"Lista de deseos (user_id = {self.user_id}, product_id = {self.product_id})"

