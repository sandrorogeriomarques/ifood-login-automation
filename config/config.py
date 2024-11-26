import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações base
BASE_URL = os.getenv('BASE_URL', 'https://gestordepedidos.ifood.com.br/#/login')

# Timeouts
IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))
