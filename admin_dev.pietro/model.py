from app import db

class Desenvolvedor(db.Model):
    """Modelo representando um Desenvolvedor."""
    id = db.Column(db.Integer,  primary_key=True)
    nome = db.Column(db.String(25), nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    # Relação 1-para-N com Task: Um desenvolvedor pode ter várias tarefas
    tarefa = db.relationship('Tarefa', backref='desenvolvedor', lazy=True, cascade='all, delete-orphan')

class Tarefa(db.Model):
    """Modelo representando uma Tarefa atribuída a um Desenvolvedor."""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    prioridade = db.Column(db.Integer, nullable=False)
    prazo = db.Column(db.Date, nullable=False)
    # Chave estrangeira que vincula a tarefa ao ID de um desenvolvedor
    id_desenvolvedor = db.Column(db.Integer, db.ForeignKey('desenvolvedor.id'), nullable=False)