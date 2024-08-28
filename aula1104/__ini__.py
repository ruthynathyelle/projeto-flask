""" Claudinei de Oliveira - pt-BR - 19-06-2023
Adaptado de Giridhar, 2016
O arquivo init.py arquivo principal 
"""

# Importamos o módulo Flask
from flask import Flask

# Cria uma nova instância da aplicação Flask
# A variável __name__ é uma variável especial do Python, que retorna o nome do módulo
# Neste caso, será '__init__', pois esse script será o ponto de entrada do programa.
app = Flask(__name__)

# Importamos as views após criar a instância do app
# para evitar importações circulares
#from proj_mvc_flask import controllers

