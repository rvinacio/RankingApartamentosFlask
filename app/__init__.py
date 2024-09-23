import os
from dotenv import load_dotenv
from flask import Flask

# Carregar as variáveis do arquivo .env
load_dotenv()

# Inicializa a aplicação Flask
app = Flask(__name__)

from app import views