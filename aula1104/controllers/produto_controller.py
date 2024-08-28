"""
Ruthy Nathyelle dos Santos Brasil utf-8 pt-br 
15/08/2024
"""
# Importando os módulos necessários do Flask
from flask import Blueprint, render_template, request, redirect, url_for

# Importando a classe 'Produto' do arquivo produto_model.py
from models.produto_model import Produto

# Criando um Blueprint. Este é um objeto que permite definir rotas em um módulo separado.
# Um Blueprint, em Flask, é um jeito de organizar um grupo de rotas relacionadas, funções de visualização e outros recursos de código.
produto_blueprint = Blueprint('produto', __name__)

# Definindo a rota raiz "/" e associando a função 'index' a esta rota.
# Quando um cliente solicita a URL '/', a função 'index' é chamada e a página retornada é renderizada.
@produto_blueprint.route("/")
def index():
    # Consultando todos os produtos do banco de dados
    produtos = Produto.get_produtos()
    # Renderizando o template 'index.html', passando a lista de produtos para ele.
    # O método render_template renderiza um template HTML que está armazenado em uma pasta de templates predefinida.
    return render_template('index.html', produtos=produtos)

# Definindo a rota "/novo" e associando a função 'novo' a esta rota.
# Esta rota aceita os métodos GET e POST.
@produto_blueprint.route("/novo", methods=['GET', 'POST'])
def novo():
    # Verificando se o método da requisição foi POST.
    if request.method == 'POST':
        # Obtendo os dados do formulário enviado na requisição POST.
        descricao = request.form.get('descricao', None)
        preco = request.form.get('preco', None)
        # Criando um novo objeto Produto com os dados obtidos do formulário.
        produto = Produto(descricao=descricao, preco=preco)
        # Salvando o novo produto no banco de dados.
        produto.salvar()
        # Redirecionando o cliente para a rota raiz.
        return redirect(url_for('index'))
    else:
        # Se o método da requisição for GET, apenas renderizamos o template 'novo.html'.
        return render_template('novo.html')

# Definindo a rota "/atualiza/<int:id>/<int:status>" e associando a função 'atualiza' a esta rota.
# Esta rota só aceita o método GET.
@produto_blueprint.route("/atualiza/<int:id>/<int:status>", methods=['GET'])
def atualiza(id, status):
    # Buscando no banco de dados o produto com o id fornecido na URL.
    produto = Produto.get_produto(id)
    # Atualizando o status do produto.
    produto.status = status
    # Salvando a alteração no banco de dados.
    produto.atualizar()
    # Redirecionando o cliente para a rota raiz.
    return redirect(url_for('index'))

# Definindo a rota "/deleta/<int:id>" e associando a função 'deleta' a esta rota.
# Esta rota só aceita o método GET.
@produto_blueprint.route("/deleta/<int:id>", methods=['GET'])
def deleta(id):
    # Buscando no banco de dados o produto com o id fornecido na URL.
    produto = Produto.get_produto(id)
   
    produto.deletar()

    return redirect(url_for('index'))

def init_app(app):
   
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/produto/novo', 'novo', novo, methods=['GET', 'POST'])
    app.add_url_rule('/produto/atualiza/<int:id>/<int:status>', 'atualiza', atualiza, methods=['GET'])
    app.add_url_rule('/produto/deleta/<int:id>', 'deleta', deleta, methods=['GET'])
