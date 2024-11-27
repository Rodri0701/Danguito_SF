from ..extension import db

class ReseñaModel(db.Model):
    __tablename__ = 'reseñas'

    Cve_comentarios = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)  # Escala de 1 a 5, por ejemplo
    comentario = db.Column(db.Text)

    def __init__(self, producto_id, user_id, calificacion, comentario):
        self.producto_id = producto_id
        self.user_id = user_id
        self.calificacion = calificacion
        self.comentario = comentario

    def __repr__(self):
        return f"Reseña(id={self.id}, producto_id={self.producto_id}, user_id={self.user_id}, calificacion={self.calificacion})"
