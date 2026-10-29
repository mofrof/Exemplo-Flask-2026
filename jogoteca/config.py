import os

# Configurações sem uso de classes e sem variáveis de ambiente
SECRET_KEY = 'jogoteca_chave_secreta_lgpd_safe_2026'

# Configurações do Banco de Dados MySQL
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'pitang'
MYSQL_DB = 'jogoteca'

# Configuração do Flask-Session no Sistema de Arquivos (Filesystem)
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = False
SESSION_USE_SIGNER = True
SESSION_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')

# Configurações de Segurança para Cookies (LGPD)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Configurações para Upload de Capas de Jogos
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
