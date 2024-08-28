"""
Ruthy Nathyelle dos Santos Brasil utf-8 pt-br 
15/08/2024
"""

# Importação da instância do SQLAlchemy criada no arquivo database.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from dao.database import db
import regex

class Validador:

    @staticmethod
    def valida_nome(nome):
        if not nome:
            raise ValueError('Nome inválido.')
        pattern = r'^[\p{L}\'\-\s]+$'
        if not regex.match(pattern, nome):
            raise ValueError('Nome inválido. Não use números ou caracteres especiais.')
        nome = regex.sub(r'\s+', ' ', nome).strip()
        partes_do_nome = nome.split()
        preposicoes = ['da', 'de', 'do', 'das', 'dos']
        nome_formatado = ' '.join([parte.capitalize() if parte.lower() not in preposicoes else parte.lower() for parte in partes_do_nome])
        return nome_formatado

    
    @staticmethod
    def valida_cpf(cpf):
        # verifica se o CPF possui exatamente 11 dígitos e se todos são numéricos
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError('CPF inválido. Deve ter 11 dígitos numéricos...')

        # elimina CPFs invalidos conhecidos
        if cpf in ['0' * 11, '1' * 11, '2' * 11, '3' * 11, '4' * 11, '5' * 11, '6' * 11, '7' * 11, '8' * 11, '9' * 11]:
            raise ValueError('CPF inválido. Sequência repetida...')

        # Validação dos dígitos verificadores
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = soma % 11
        if resto < 2:
            digito1 = 0
        else:
            digito1 = 11 - resto

        if int(cpf[9]) != digito1:
            raise ValueError('CPF inválido. Dígito verificador 1 não confere...')

        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = soma % 11
        if resto < 2:
            digito2 = 0
        else:
            digito2 = 11 - resto

        if int(cpf[10]) != digito2:
            raise ValueError('CPF inválido. Dígito verificador 2 não confere...')

        return cpf  # retorna True se o CPF for válido

    @staticmethod
    def valida_email(email):
        
        # valida o email, garantindo que contenha um @
        if '@' not in email:
            raise ValueError('Email inválido.')
        return email

    @staticmethod
    
    def formata_texto(texto):
        # Capitaliza cada palavra corretamente, exceto preposições
        return ' '.join(word.capitalize() if word.lower() not in ['da', 'de', 'do', 'das', 
              'dos'] else word.lower() for word in regex.sub(r'\s+', ' ', texto).strip().split())

    @staticmethod
    def valida_endereco(logradouro, numero, complemento, bairro, cep, cidade, uf):
        # Aplica a formatação correta de texto
        logradouro = Validador.formata_texto(logradouro)
        bairro = Validador.formata_texto(bairro)
        cidade = Validador.formata_texto(cidade)

        # Verifica se os campos obrigatórios estão preenchidos
        if not all([logradouro, numero, bairro, cep, cidade, uf]):
            raise ValueError('Todos os campos de endereço, exceto complemento, são obrigatórios.')

        # Validação do CEP com formato específico (00000-000)
        if not regex.match(r'^\d{5}-\d{3}$', cep):
            raise ValueError('CEP inválido. Deve seguir o formato 00000-000.')

        # Validação do UF para garantir que sejam duas letras maiúsculas
        if not regex.match(r'^[A-Z]{2}$', uf):
            raise ValueError('UF inválido. Deve ser composto por duas letras maiúsculas.')

        return logradouro, numero, complemento, bairro, cep, cidade, uf


class Pessoas:
    def __init__(self, nome, cpf, logradouro, numero, complemento, bairro, cep, cidade, uf, telefone, email):
        self.nome = Validador.valida_nome(nome)
        self.cpf = Validador.valida_cpf(cpf)
        self.email = Validador.valida_email(email)
        self.telefone = telefone
        logradouro, numero, complemento, bairro, cep, cidade, uf = Validador.valida_endereco(logradouro, numero, complemento, bairro, cep, cidade, uf)
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep
        self.uf = uf

    @property
    def cpf(self):
        return self.cpf                                                               
    
   

class Clientes(Pessoas, db.Model):
    __tablename__ = 'clientes'
   
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String)
    cpf: Mapped[str] = mapped_column(String, unique=True)
    logradouro: Mapped[str] = mapped_column(String)
    numero: Mapped[str] = mapped_column(String)
    complemento: Mapped[str] = mapped_column(String)
    bairro: Mapped[str] = mapped_column(String)
    cep: Mapped[str] = mapped_column(String)
    cidade: Mapped[str] = mapped_column(String)
    uf: Mapped[str] = mapped_column(String)
    telefone: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

    def __init__(self, nome, cpf, logradouro, numero, complemento, bairro, cep, cidade, uf, telefone, email):
        super().__init__(nome, cpf, logradouro, numero, complemento, bairro, cep, cidade, uf, telefone, email)


    # Método para salvar um produto no banco de dados
    def salvar(self):
        db.session.add(self)  # Adicionando o produto na sessão do SQLAlchemy
        print('CPFA: ',self.cpf)
        db.session.commit()  # Salvando as alterações no banco de dados

    # Método para atualizar um produto no banco de dados
    def atualizar(self):
        db.session.commit()  # Salvando as alterações no banco de dados

    # Método para deletar um produto no banco de dados
    def deletar(self):
        db.session.delete(self)  # Removendo o produto da sessão do SQLAlchemy
        db.session.commit()  # Salvando as alterações no banco de dados

    @staticmethod
    def get_clientes():
        # Retorna todos os produtos
        return db.session.query(Clientes).all()

    @staticmethod
    def get_cliente(id):
        # Retorna um produto específico pelo ID
        return db.session.query(Clientes).get(id)
