from ..extension import db

class ReseñaModel(db.Model):
    __tablename__ = 'reseñas'

    Cve_comentarios = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.Cve_Productos'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Usr.Cve_usuarios'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)  # Escala de 1 a 5, por ejemplo
    comentario = db.Column(db.Text)

    producto = db.relationship('ProductoModel', backref='reseñas')
    user = db.relationship('UserModel', backref='reseñas_usuario')

    def __repr__(self):
        return f"Reseña(id={self.id}, producto_id={self.producto_id}, user_id={self.user_id}, calificacion={self.calificacion})"
