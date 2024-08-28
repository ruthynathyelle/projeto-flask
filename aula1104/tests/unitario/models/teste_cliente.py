from flask_testing import TestCase
from app import create_app, db
from models.cliente_model import Clientes

class TestClientesModel(TestCase):

    def create_app(self):
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_cliente(self):
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
        self.assertEqual(Clientes.query.count(), 1)

    def test_get_cliente(self):
        cliente = Clientes(
            nome='Teste Cliente',
            cpf='56297316376',
            logradouro='Rua Teste',
            numero='123',
            complemento='Apto 1',
            bairro='Centro',
            cep='76870-074',
            cidade='Cidade Teste',
            uf='RO',
            telefone='123456789',
            email='teste@cliente.com'
        )
        db.session.add(cliente)
        db.session.commit()
        cliente_query = Clientes.query.get(cliente.id)
        self.assertEqual(cliente_query.id, cliente.id)

    def test_update_cliente(self):
        cliente = Clientes(
            nome='Teste Cliente',
            cpf='56297316376',
            logradouro='Rua Teste',
            numero='123',
            complemento='Apto 1',
            bairro='Centro',
            cep='76870-074',
            cidade='Cidade Teste',
            uf='RO',
            telefone='123456789',
            email='teste@cliente.com'
        )
        db.session.add(cliente)
        db.session.commit()
        cliente.nome = 'Cliente Atualizado'
        cliente.cpf = '78272817292'
        cliente.logradouro = 'Rua Atualizada'
        cliente.numero = '321'
        cliente.complemento = 'Apto 2'
        cliente.bairro = 'Novo Bairro'
        cliente.cep = '76880-000'
        cliente.cidade = 'Nova Cidade'
        cliente.uf = 'RO'
        cliente.telefone = '987654321'
        cliente.email = 'atualizado@cliente.com'
        db.session.commit()
        cliente_atualizado = Clientes.query.get(cliente.id)
        self.assertEqual(cliente_atualizado.nome, 'Cliente Atualizado')
        self.assertEqual(cliente_atualizado.cpf, '78272817292')

    def test_delete_cliente(self):
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
        db.session.delete(cliente)
        db.session.commit()
        cliente_deletado = Clientes.query.get(cliente.id)
        self.assertIsNone(cliente_deletado)

    def test_get_all_clientes(self):
        cliente1 = Clientes(
            nome='fulano',
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
        cliente2 = Clientes(
            nome='Clientee',
            cpf='02397680513',
            logradouro='Rua 2',
            numero='2',
            complemento='',
            bairro='Bairro 2',
            cep='22222-222',
            cidade='Cidade 2',
            uf='UF',
            telefone='222222222',
            email='cliente2@teste.com'
        )
        db.session.add(cliente1)
        db.session.add(cliente2)
        db.session.commit()
        todos_clientes = Clientes.query.all()
        self.assertEqual(len(todos_clientes), 2)

if __name__ == '__main__':
    import unittest
    unittest.main()
