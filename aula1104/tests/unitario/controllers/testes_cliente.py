from flask_testing import TestCase
from app import create_app, db
from models.cliente_model import Clientes
from controllers.cliente_controller import cliente_blueprint

class TestClienteController(TestCase):

    def create_app(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.register_blueprint(cliente_blueprint)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        cliente1 = Clientes(
            nome='Fulano',
            cpf='79562326438',
            logradouro='Rua 1',
            numero='1',
            complemento='',
            bairro='Bairro 1',
            cep='11111-111',
            cidade='Cidade 1',
            uf='UF',
            telefone='111111111',
            email='cliente1@teste.com'
        )
        db.session.add(cliente1)
        db.session.commit()

        response = self.client.get('/clientes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fulano', response.data)

    def test_novo_cliente(self):
        data = {
            'nome': 'Novo Cliente',
            'cpf': '56297316376',
            'logradouro': 'Rua Teste',
            'numero': '123',
            'complemento': 'Apto 1',
            'bairro': 'Centro',
            'cep': '12345-678',
            'cidade': 'Cidade Teste',
            'uf': 'TS',
            'telefone': '123456789',
            'email': 'teste@cliente.com'
        }
        response = self.client.post('/clientes/novo', data=data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após criar cliente
        cliente = Clientes.query.filter_by(cpf='56297316376').first()
        self.assertIsNotNone(cliente)

    def test_atualiza_cliente(self):
        cliente = Clientes(
            nome='Teste Cliente',
            cpf='56297316376',
            logradouro='Rua Teste',
            numero='123',
            complemento='Apto 1',
            bairro='Centro',
            cep='12345-678',
            cidade='Cidade Teste',
            uf='TS',
            telefone='123456789',
            email='teste@cliente.com'
        )
        db.session.add(cliente)
        db.session.commit()

        data = {
            'nome': 'Cliente Atualizado',
            'cpf': '78272817292',
            'logradouro': 'Rua Atualizada',
            'numero': '321',
            'complemento': 'Apto 2',
            'bairro': 'Novo Bairro',
            'cep': '76880-000',
            'cidade': 'Nova Cidade',
            'uf': 'RO',
            'telefone': '987654321',
            'email': 'atualizado@cliente.com'
        }
        response = self.client.post(f'/clientes/atualiza/{cliente.id}', data=data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento após atualizar cliente

        cliente_atualizado = Clientes.query.get(cliente.id)
        self.assertEqual(cliente_atualizado.nome, 'Cliente Atualizado')
        self.assertEqual(cliente_atualizado.cpf, '78272817292')

    def test_deleta_cliente(self):
        cliente = Clientes(
            nome='Teste Cliente',
            cpf='78272817292',
            logradouro='Rua Teste',
            numero='123',
            complemento='Apto 1',
            bairro='Centro',
            cep='76880-000',
            cidade='Cidade Teste',
            uf='RO',
            telefone='123456789',
            email='teste@cliente.com'
        )
        db.session.add(cliente)
        db.session.commit()

        response = self.client.get(f'/clientes/deleta/{cliente.id}')
        self.assertEqual(response.status_code, 302)  # Redirecionamento após deletar cliente

        cliente_deletado = Clientes.query.get(cliente.id)
        self.assertIsNone(cliente_deletado)

if __name__ == '__main__':
    import unittest
    unittest.main()
