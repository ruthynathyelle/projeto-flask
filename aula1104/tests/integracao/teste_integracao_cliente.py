import unittest
from app import create_app, db
from models.cliente_model import Clientes

class TestClientes(unittest.TestCase):

    def setUp(self):
        # Configura o aplicativo para o modo de teste
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        # Cria o contexto da aplicação e o banco de dados de teste
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        # Remove o banco de dados de teste após cada teste
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_criar_cliente(self):
        # Testa a criação de um novo cliente
        cliente = Clientes(
            nome="Ruthy Nathyelle",
            cpf="56297316376",
            logradouro="Rua Teste",
            numero="123",
            complemento="Apto 101",
            bairro="Centro",
            cep="12345-678",
            cidade="Cidade Teste",
            uf="RO",
            telefone="69993486711",
            email="ruthy2015buritis@hotmail.com"
        )
        cliente.salvar()
        clientes = Clientes.query.all()
        self.assertEqual(len(clientes), 1)
        self.assertEqual(clientes[0].nome, "Ruthy Nathyelle")

    def test_atualizar_cliente(self):
        # Testa a atualização de um cliente existente
        cliente = Clientes(
            nome="Cliente Antigo",
            cpf="56297316376",
            logradouro="Rua Velha",
            numero="321",
            complemento="Apto 202",
            bairro="Bairro Velho",
            cep="87654-321",
            cidade="Cidade Velha",
            uf="SP",
            telefone="69993486712",
            email="cliente@velho.com"
        )
        cliente.salvar()

        cliente.nome = "Cliente Atualizado"
        cliente.atualizar()

        cliente_atualizado = Clientes.query.get(cliente.id)
        self.assertEqual(cliente_atualizado.nome, "Cliente Atualizado")

    def test_deletar_cliente(self):
        # Testa a exclusão de um cliente
        cliente = Clientes(
            nome="Cliente a Ser Deletado",
            cpf="56297316376",
            logradouro="Rua Delete",
            numero="123",
            complemento="Apto 303",
            bairro="Bairro Deletado",
            cep="44556-789",
            cidade="Cidade Deletada",
            uf="RJ",
            telefone="69993486713",
            email="deletar@cliente.com"
        )
        cliente.salvar()

        cliente.deletar()
        clientes_restantes = Clientes.query.all()
        self.assertEqual(len(clientes_restantes), 0)

if __name__ == "__main__":
    unittest.main()
