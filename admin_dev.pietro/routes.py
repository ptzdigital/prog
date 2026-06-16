from flask import render_template, redirect, url_for, flash, session, request
from model import Desenvolvedor, Tarefa
from forms import DeveloperForm, LoginForm, TarefaForm, TarefaPesquisarForm, TarefaAtualizarForm
from app import app, db

ADMIN_NOME = "admin"
ADMIN_SENHA = "123456"

@app.route('/')
def index():
    usuario_logado = False
    if 'usuario' in session:
        usuario_logado = True
    form = LoginForm()
    """Rota principal que exibe todos os desenvolvedores e tarefas cadastradas."""
    developers = Desenvolvedor.query.order_by(Desenvolvedor.nome).all()
    tarefas = Tarefa.query.order_by(Tarefa.prazo).all()
    return render_template('index.html', developers=developers, tarefas=tarefas,
                           logado=usuario_logado, form = form, usuario=session.get("usuario"))

@app.route('/logar',methods=['POST',"GET"])
def logar():
    usuario_logado = False
    form = LoginForm()

    if form.validate_on_submit():

        # LOGIN ADMIN
        if form.nome.data == ADMIN_NOME and form.senha.data == ADMIN_SENHA:
            session["usuario"] = ADMIN_NOME
            session["usuario_id"] = -1
            session["admin"] = True

            flash('Administrador logado com sucesso!', 'success')
            return redirect(url_for('index'))

        # LOGIN NORMAL
        usuario = Desenvolvedor.query.filter_by(
            nome=form.nome.data,
            senha=form.senha.data
        ).first()

        if usuario:
            session["usuario"] = usuario.nome
            session["usuario_id"] = usuario.id
            session["admin"] = False

            flash('Usuário logado com sucesso!', 'success')
            return redirect(url_for('index'))

        flash('Nome ou senha inválido!', 'error')

    developers = Desenvolvedor.query.order_by(Desenvolvedor.nome).all()
    tarefas = Tarefa.query.order_by(Tarefa.prazo).all()

    return render_template(
        'index.html',
        developers=developers,
        tarefas=tarefas,
        logado=usuario_logado,
        form=form,
        usuario=session.get("usuario")
    )

@app.route('/deslogar',methods=['POST','GET'])
def deslogar():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    form = LoginForm()
    session.pop('usuario',None)
    session.pop('usuario_id',None)
    session.pop('admin',None)
    flash('Usuário deslogado com sucesso!', 'success')
    developers = Desenvolvedor.query.order_by(Desenvolvedor.nome).all()
    tarefas = Tarefa.query.order_by(Tarefa.prazo).all()
    return render_template('index.html', developers=developers, tarefas=tarefas,
                           logado=False, form = form,usuario=None)


@app.route('/cadastrar-desenvolvedor', methods=['GET', 'POST'])
def registrar_desenvolvedor():
    usuario_logado = False
    if 'usuario' in session:
        usuario_logado = True
    else:
        return redirect(url_for("logar"))
    """Rota para acessar o formulário e cadastrar novos desenvolvedores."""
    form = DeveloperForm()
    # Processa o formulário se enviado com método POST e passar nas validações
    if form.validate_on_submit():
        new_dev = Desenvolvedor(nome=form.nome.data,
                                senha = form.senha.data)
        db.session.add(new_dev)
        db.session.commit()
        flash('Desenvolvedor cadastrado com sucesso!', 'success')
        return redirect(url_for('registrar_desenvolvedor'))
    if form.errors:
        flash('Preencha corretamente os dados!', 'error')
    return render_template('registrar_desenvolvedor.html', form=form,usuario=session.get("usuario"),logado=usuario_logado)

@app.route('/criar-tarefa', methods=['GET', 'POST'])
def criar_tarefa():
    usuario_logado = False
    if 'usuario' in session:
        usuario_logado = True
    else:
        return redirect(url_for("logar"))
    """Rota para visualizar o formulário e criar novas tarefas vinculadas aos desenvolvedores."""
    form = TarefaForm()
    # Popula o SelectField de desenvolvedor_id dinamicamente com as opções do banco de dados
    devs = Desenvolvedor.query.all()
    devs_list = []
    for d in devs:
        devs_list.append((d.id, d.nome))
    form.id_desenvolvedor.choices = devs_list

    # Verifica se os dados do formulário são válidos e processa o cadastro
    if form.validate_on_submit():
        nova_tarefa = Tarefa(
            nome=form.nome.data,
            descricao=form.descricao.data,
            prioridade=form.prioridade.data,
            prazo=form.prazo.data,
            id_desenvolvedor=form.id_desenvolvedor.data
        )
        db.session.add(nova_tarefa)
        db.session.commit()
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('criar_tarefa'))
    return render_template('criar_tarefa.html', form=form,usuario=session.get("usuario"),logado=usuario_logado)

@app.route('/pesquisar-tarefas', methods=['GET', 'POST'])
def buscar_tarefas():
    usuario_logado = False
    if 'usuario' in session:
        usuario_logado = True
    else:
        return redirect(url_for("logar"))
    form = TarefaPesquisarForm()
    # Por padrão, mostra todas as tarefas ordenadas por data
    tarefas = Tarefa.query.order_by(Tarefa.prazo).all()

    if form.validate_on_submit():
        if form.data_busca.data:
            tarefas = Tarefa.query.filter_by(prazo=form.data_busca.data).order_by(Tarefa.prioridade).all()
        else:
            tarefas = Tarefa.query.order_by(Tarefa.prazo).all()

    return render_template('busca_tarefas.html', form=form, tarefas=tarefas,usuario=session.get("usuario"),logado=usuario_logado)

@app.route('/editar-tarefa/<int:id_tarefa>/<string:origem>', methods=['GET', 'POST'])
def editar_tarefa(id_tarefa, origem):
    usuario_logado = False
    if 'usuario' in session:
        usuario_logado = True
    else:
        return redirect(url_for("logar"))   
    if session.get("admin"):
        tarefa = Tarefa.query.filter_by(id=id_tarefa).one_or_none()
    else:

        tarefa = Tarefa.query.filter_by(
        id=id_tarefa,
        id_desenvolvedor=session.get("usuario_id")
    ).one_or_none()
    
    if tarefa != None:
        form = TarefaAtualizarForm(obj=tarefa)  # Pré-preenche o formulário com os dados atuais
        devs = Desenvolvedor.query.all()
        devs_list = []
        for d in devs:
            devs_list.append((d.id, d.nome))
        form.id_desenvolvedor.choices = devs_list
        print(request.url_rule)
        print(form.validate_on_submit())
        print(origem)
        if form.validate_on_submit() and origem != "buscar_tarefas" :
            # Atualiza os campos manualmente para garantir compatibilidade de tipos
            tarefa.nome = form.nome.data
            tarefa.descricao = form.descricao.data
            tarefa.prioridade = form.prioridade.data
            tarefa.prazo = form.prazo.data
            tarefa.id_desenvolvedor = form.id_desenvolvedor.data
            
            db.session.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
            return redirect(url_for('buscar_tarefas'))
    else:
        flash('Você não pode editar uma tarefa que não é sua!', 'error')
        return redirect(url_for('buscar_tarefas'))
    return render_template('editar_tarefa.html', form=form, tarefa=tarefa,usuario=session.get("usuario"),logado=usuario_logado)

@app.route('/deletar-tarefa/<int:id_tarefa>', methods=['POST'])
def deletar_tarefa(id_tarefa):
    if 'usuario' in session:
        usuario_logado = True
    else:
        return redirect(url_for("logar"))
    
    if session.get("admin"):
        tarefa = Tarefa.query.filter_by(id=id_tarefa).one_or_none()
    else:
        tarefa = Tarefa.query.filter_by(id=id_tarefa,id_desenvolvedor=session.get("usuario_id")).one_or_none()
    if tarefa != None:
        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa deletada com sucesso!', 'success')
    else:
        flash('Essa tarefa não pertence a você!', 'error')
    return redirect(url_for('buscar_tarefas'))

@app.route("/deletar_usuario/<int:id_usuario>", methods=["POST"])
def deletar_usuario(id_usuario):

    if 'usuario' not in session:
        return redirect(url_for("logar"))

    if not session.get("admin"):
        flash('Apenas o administrador pode deletar usuários!', 'error')
        return redirect(url_for('index'))

    dev = Desenvolvedor.query.filter_by(id=id_usuario).one_or_none()
    if dev != None:
        deslogar_usuario = False
        if(dev.id == session.get("usuario_id")):
            deslogar_usuario = True
        db.session.delete(dev)
        db.session.commit()
        flash('Usuário deletado com sucesso!', 'success')
        if(dev.id == session.get("usuario_id")):
            return redirect(url_for('deslogar'))
    else:
        flash('Usuário não encontrado!', 'error')
    return redirect(url_for('index'))