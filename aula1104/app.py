"""
Ruthy Nathyelle dos Santos Brasil utf-8 pt-br 
15/08/2024
"""

# Importação das bibliotecas e módulos necessários
from flask import Flask, render_template, request, redirect, url_for, flash
from models.produto_model import Produto  # Importação da classe Produto do modelo
from models.cliente_model import Clientes # from sqlalchemy import create_engine, inspect
from dao.database import db  # Importação da instância do SQLAlchemy criada em database.py
import os


# Função para criar uma instância do aplicativo Flask
def create_app():
    app = Flask(__name__)  # Cria a instância do aplicativo Flask

    # Configura o URI do banco de dados de maneira portátil
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # captura o diretório absoluto 
                                                           # onde o script está sendo executado

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'ifro2024.db')  
        # junta o caminho de forma portátil

    app.secret_key = 'seu segredo'  # adiciona uma chave secreta para permitir flash messages
    db.init_app(app)  # Inicializa o SQLAlchemy com o aplicativo Flask
    return app


# Função para criar as tabelas no banco de dados
def create_tables():
    with app.app_context():  # Cria um contexto para o aplicativo Flask
        db.create_all()  # Cria todas as tabelas no banco de dados
        print('Tabelas criadas com sucesso!')


# Cria a instância do aplicativo Flask e configura o banco de dados
app = create_app()


# Cria as tabelas no banco de dados se necessário
create_tables()


# Rota principal do aplicativo que exibe todos os produtos

@app.route('/')
def index():
    produtos = Produto.get_produtos()  # Obtém todos os produtos do banco de dados
    return render_template('produto/novo.html', produtos=produtos)  # Renderiza o template novo.html com os produtos


# Rota para adicionar um novo produto
@app.route('/produto/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':  # Se o método da requisição é POST
        descricao = request.form.get('descricao', None)  # Obtém a descrição do produto do form
        preco = request.form.get('preco', None)  # Obtém o preço do produto do form

        # Verifica se o preço é um número válido
        try:
            preco = float(preco)
        except ValueError:
            flash('O preço deve ser um número válido.')  # Exibe uma mensagem de erro
            produtos = Produto.get_produtos()  # Obtém todos os produtos do banco de dados
            return render_template('produto/novo.html', produtos=produtos)  # Renderiza o template novo.html com os produtos

        produto = Produto(descricao=descricao, preco=preco)  # Cria uma nova instância do produto
        produto.salvar()  # Salva o produto no banco de dados

    produtos = Produto.get_produtos()  # Obtém todos os produtos do banco de dados
    return render_template('produto/novo.html', produtos=produtos)  # Renderiza o template novo.html com os produtos


# Rota para atualizar um produto
@app.route('/produto/editar/<float:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.get_produto(id)  # Obtém o produto pelo ID
    if request.method == 'POST':  # Se o método da requisição é POST
        descricao = request.form.get('descricao')  # Obtém a descrição do produto do form
        preco = request.form.get('preco')  # Obtém o preço do produto do form

        # Verifica se o preço é um número válido
        try:
            preco = float(preco)
        except ValueError:
            flash('O preço deve ser um número válido.')  # Exibe uma mensagem de erro
            return render_template('produto/atualizar.html', produto=produto)  # Renderiza o template editar.html com o produto

        produto.descricao = descricao  # Atualiza a descrição do produto
        produto.preco = preco  # Atualiza o preço do produto
        produto.atualizar()  # Atualiza o produto no banco de dados
        return redirect(url_for('index'))  # Redireciona para a rota '/'
    return render_template('produto/atualizar.html', produto=produto)  # Renderiza o template editar.html com o produto


# Rota para atualizar o status de um produto
@app.route('/produto/atualizar/<int:id>/<int:status>', methods=['GET', 'POST'])  # Alteração aqui, 'status' adicionado como parâmetro
def atualizar_produto(id, status):  # Alteração aqui, 'status' adicionado como parâmetro
    produto = Produto.get_produto(id)  # Obtém o produto pelo ID
    produto.status = status  # Atualiza o status do produto
    produto.atualizar()  # Atualiza o produto no banco de dados
    return redirect(url_for('index'))  # Redireciona para a rota '/'


# Rota para deletar um produto
@app.route('/produto/deletar/<id>', methods=['GET'])
def deletar_produto(id):
    produto = Produto.get_produto(id)  # Obtém o produto pelo ID
    produto.deletar()  # Deleta o produto do banco de dados
    return redirect(url_for('index'))  # Redireciona para a rota '/'

#CLIENTES
@app.route('/clientes')
def index_clientes():
    clientes = Clientes.get_clientes()  # Obtém todos os clientes do banco de dados
    return render_template('cliente/novo_cliente.html', clientes=clientes)  # Renderiza o template novo_cliente.html com os clientes

# Rota para adicionar um novo cliente
@app.route('/clientes/novo', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':  # Se o método da requisição é POST
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

        # Valida os dados do cliente
        '''if not nome or not cpf or not email or '@' not in email:
            flash('Nome, CPF e email são obrigatórios, e o email deve ser válido.')  # Exibe uma mensagem de erro
            clientes = Clientes.get_clientes()  # Obtém todos os clientes do banco de dados
            return render_template('cliente/index_cliente.html', clientes=clientes)  # Renderiza o template novo_cliente.html com os clientes'''

    try:
            cliente = Clientes(nome=nome, cpf=cpf, logradouro=logradouro, numero=numero, complemento=complemento,
                                bairro=bairro, cep=cep, cidade=cidade, uf=uf, telefone=telefone, email=email)
            cliente.salvar()  # Salva o cliente no banco de dados
            flash('Cliente adicionado com sucesso!', 'success')  # Mensagem de sucesso
            return redirect(url_for('index_clientes'))  # Redireciona para a lista de clientes
    except ValueError as e:
            flash(f'Erro: {e}', 'error')  # Mensagem de erro

    return render_template('cliente/novo_cliente.html')  

# Renderiza o template novo_cliente.html com os clientes
@app.route('/cliente/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Clientes.get_cliente(id)  # Obtém o cliente pelo ID
    if request.method == 'POST':  # Se o método da requisição é POST
        nome = request.form.get('nome')  # Obtém o nome do cliente do form
        cpf = request.form.get('cpf')  # Obtém o CPF do cliente do form
        logradouro = request.form.get('logradouro')  # Obtém o logradouro do cliente do form
        numero = request.form.get('numero')  # Obtém o número do endereço do cliente do form
        complemento = request.form.get('complemento')  # Obtém o complemento do endereço do cliente do form
        bairro = request.form.get('bairro')  # Obtém o bairro do cliente do form
        cep = request.form.get('cep')  # Obtém o CEP do cliente do form
        cidade = request.form.get('cidade')  # Obtém a cidade do cliente do form
        uf = request.form.get('uf')  # Obtém a UF do cliente do form
        telefone = request.form.get('telefone')  # Obtém o telefone do cliente do form
        email = request.form.get('email')  # Obtém o email do cliente do form

        # Atualiza os dados do cliente
        cliente.nome = nome
        cliente.cpf = cpf
        cliente.logradouro = logradouro
        cliente.numero = numero
        cliente.complemento = complemento
        cliente.bairro = bairro
        cliente.cep = cep
        cliente.cidade = cidade
        cliente.uf = uf
        cliente.telefone = telefone
        cliente.email = email
        cliente.atualizar()  # Atualiza o cliente no banco de dados

        return redirect(url_for('index_clientes'))  # Redireciona para a rota '/clientes'
    
    return render_template('cliente/atualizar_cliente.html', cliente=cliente)  # Renderiza o template atualizar_cliente.html com os dados do cliente

@app.route('/cliente/atualizar/<int:id>/<int:status>', methods=['GET', 'POST'])
def atualizar_cliente(id, status):
    cliente = Clientes.get_cliente(id)  # Obtém o cliente pelo ID
    cliente.status = status  # Atualiza o status do cliente
    cliente.atualizar()  # Atualiza o cliente no banco de dados
    return redirect(url_for('index_clientes'))  # Redireciona para a rota '/clientes'

@app.route('/cliente/deletar/<int:id>', methods=['GET'])
def deletar_cliente(id):
    cliente = Clientes.get_cliente(id)  # Obtém o cliente pelo ID
    cliente.deletar()  # Deleta o cliente do banco de dados
    return redirect(url_for('index_clientes'))  # Redireciona para a rota '/clientes'


# Verifica se o script está sendo executado diretamente e não importado
if __name__ == '__main__':
    app.run(debug=True)

