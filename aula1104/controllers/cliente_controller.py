from flask import Blueprint, flash, render_template, request, redirect, url_for
from models.cliente_model import Clientes  # Importe a classe Clientes do seu modelo

# Criando um Blueprint para o cliente
cliente_blueprint = Blueprint('cliente', __name__)

# Rota para visualizar todos os clientes
@cliente_blueprint.route("/clientes")
def index():
    # Consultar todos os clientes
    clientes = Clientes.query.all()  # Assumindo que você está usando SQLAlchemy, ajuste conforme necessário
    return render_template('cliente/novo_cliente.html', clientes=clientes)

# Rota para adicionar um novo cliente
@cliente_blueprint.route("/clientes/novo", methods=['GET', 'POST'])
def novo_cliente():
    try:
        nome = request.form.get('nome', None)
        cpf = request.form.get('cpf', None)
        logradouro = request.form.get('logradouro', None)
        numero = request.form.get('numero', None)
        complemento = request.form.get('complemento', None)
        bairro = request.form.get('bairro', None)
        cep = request.form.get('cep', None)
        cidade = request.form.get('cidade', None)
        uf = request.form.get('uf', None)
        telefone = request.form.get('telefone', None)
        email = request.form.get('email', None)

        # Criando um novo objeto cliente
        cliente = Clientes(nome=nome, cpf=cpf, logradouro=logradouro, numero=numero, complemento=complemento, bairro=bairro, cep=cep, cidade=cidade, uf=uf, telefone=telefone, email=email)
        
        # Salvando o cliente no banco de dados
        cliente.salvar()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('cliente/novo_cliente.html',))
    
    except ValueError as e:
            flash(f'Erro: {e}', 'error')

    clientes = Clientes.get_clientes()
    return render_template('cliente/novo_cliente.html', clientes=clientes, **request.form)
# Rota para atualizar um cliente
@cliente_blueprint.route("/clientes/atualiza/<int:id>", methods=['GET', 'POST'])
def atualiza_cliente(id):
    cliente = Clientes.query.get(id)  # Assumindo que você está usando SQLAlchemy, ajuste conforme necessário
    if request.method == 'POST':
        cliente.nome = request.form.get('nome', cliente.nome)
        cliente.cpf = request.form.get('cpf', cliente.cpf)
        cliente.logradouro = request.form.get('logradouro', cliente.logradouro)
        cliente.numero = request.form.get('numero', cliente.numero)
        cliente.complemento = request.form.get('complemento', cliente.complemento)
        cliente.bairro = request.form.get('bairro', cliente.bairro)
        cliente.cep = request.form.get('cep', cliente.cep)
        cliente.cidade = request.form.get('cidade', cliente.cidade)
        cliente.uf = request.form.get('uf', cliente.uf)
        cliente.telefone = request.form.get('telefone', cliente.telefone)
        cliente.email = request.form.get('email', cliente.email)

        cliente.atualizar()  # Assumindo que você tem um método atualizar no modelo, ajuste conforme necessário
        
        return redirect(url_for('cliente.index'))
   
# Rota para deletar um cliente
@cliente_blueprint.route("/clientes/deleta/<int:id>", methods=['GET'])
def deleta_cliente(id):
    cliente = Clientes.query.get(id)  # Assumindo que você está usando SQLAlchemy, ajuste conforme necessário
    if cliente:
        cliente.deletar()  # Assumindo que você tem um método deletar no modelo, ajuste conforme necessário
    return redirect(url_for('cliente.index'))

# Função para inicializar as rotas no app
def init_app(app):
    app.add_url_rule('/clientes', 'index', index)  # Rota para visualizar todos os clientes
    app.add_url_rule('/clientes/novo', 'novo_cliente', novo_cliente, methods=['GET', 'POST']) 
    app.add_url_rule('/clientes/atualiza/<int:id>', 'atualiza_cliente', atualiza_cliente, methods=['GET', 'POST'])
    app.add_url_rule('/clientes/deleta/<int:id>', 'deleta_cliente', deleta_cliente, methods=['GET'])
