from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, EqualTo


class DeveloperForm(FlaskForm):
    """Formulário para cadastrar um novo desenvolvedor."""
    nome = StringField('Nome do Desenvolvedor', validators=[DataRequired(message="O nome é obrigatório.")])
    senha = PasswordField("Senha",validators=[DataRequired(message="O nome é obrigatório.")])
    senha_confirmacao = PasswordField("Comfirmar senha",validators=[ EqualTo('senha', message='Senha deve ser igual a digitada no campo Senha')])
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):
    nome = StringField('Nome do Desenvolvedor', validators=[DataRequired(message="O nome é obrigatório.")])
    senha = PasswordField("Senha",validators=[DataRequired(message="O nome é obrigatório.")])
    submit = SubmitField('Logar')

class TarefaForm(FlaskForm):
    """Formulário para criar uma nova tarefa e atribuí-la a um desenvolvedor."""
    id_desenvolvedor = SelectField('Desenvolvedor', coerce=int, validators=[DataRequired(message="Selecione um desenvolvedor.")])
    nome = StringField('Nome da Tarefa', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    prioridade = IntegerField('Prioridade (1 a 10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    prazo = DateField('Data de Entrega', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Criar Tarefa')

class TarefaPesquisarForm(FlaskForm):
    data_busca = DateField('Filtrar por Data de Entrega (opcional)', render_kw={"type": "date"})
    submit = SubmitField('Pesquisar')

class TarefaAtualizarForm(FlaskForm):
    id_desenvolvedor = SelectField('Desenvolvedor', coerce=int, validators=[DataRequired()])
    nome = StringField('Nome da Tarefa', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    prioridade = IntegerField('Prioridade (1 a 10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    prazo = DateField('Data de Entrega', validators=[DataRequired()], format='%Y-%m-%d', render_kw={"type": "date"})
    submit = SubmitField('Atualizar Tarefa')