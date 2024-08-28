import unittest
from flask import Flask
from models.produto_model import Produto
from controllers.produto_controller import produto_blueprint

class TestProdutoBlueprint(unittest.TestCase):
    def setUp(self):
        # Cria uma instância do aplicativo Flask para os testes
        self.app = Flask(__name__)
        self.app.register_blueprint(produto_blueprint, url_prefix='/produto')
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use um banco de dados SQLite para teste
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Configura o banco de dados para teste
        with self.app.app_context():
            from flask_sqlalchemy import SQLAlchemy
            self.db = SQLAlchemy(self.app)
            self.db.create_all()

    def tearDown(self):
        # Remove o banco de dados após os testes
        with self.app.app_context():
            self.db.drop_all()

    def test_index(self):
        # Testa a rota raiz
        response = self.client.get('/produto/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Produto', response.data)  # Verifica se a palavra 'Produto' está na resposta

    def test_novo(self):
        # Testa a criação de um novo produto
        response = self.client.post('/produto/novo', data=dict(descricao='Produto Teste', preco='10.00'))
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso
        response = self.client.get('/produto/')
        self.assertIn(b'Produto Teste', response.data)  # Verifica se o produto foi adicionado

    def test_atualiza(self):
        # Testa a atualização de um produto
        produto = Produto(descricao='Produto para Atualizar', preco='20.00')
        produto.salvar()
        produto_id = produto.id
        response = self.client.get(f'/produto/atualiza/{produto_id}/1')
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso
        produto_atualizado = Produto.get_produto(produto_id)
        self.assertEqual(produto_atualizado.status, 1)

    def test_deleta(self):
        # Testa a exclusão de um produto
        produto = Produto(descricao='Produto para Deletar', preco='30.00')
        produto.salvar()
        produto_id = produto.id
        response = self.client.get(f'/produto/deleta/{produto_id}')
        self.assertEqual(response.status_code, 302)  # Redireciona após sucesso
        produto_deletado = Produto.get_produto(produto_id)
        self.assertIsNone(produto_deletado)

if __name__ == '__main__':
    unittest.main()
