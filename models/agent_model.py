from extensions import db

class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    provision = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Agent {self.name}>"
