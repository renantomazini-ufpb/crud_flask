from app import db

class Pessoa(db.Model):
    __tablename__ = 'pessoa'

    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(100), nullable= False)
    cargo = db.Column(db.String(50))
    setor = db.Column(db.String(50))
    salario = db.Column(db.Float)
    tipo = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=False)

    def to_dict(self): #converte para json
        return{
            "id": self.id,
            "nome": self.nome,
            "cargo": self.cargo,
            "salario": self.salario,
            "tipo": self.tipo,
            "ativo": self.ativo
        }
    
    def __repr__(self):
        return f"<pessoa id={self.id} nome='{self.nome}'>"
    
    def ativar(self):
        self.ativo = True #fazer a rota

    def desativar(self):
        self.ativo = False #fazer a rota
