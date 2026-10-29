import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db_connection

def buscar_usuario_por_login(login):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT uuid, login, password, nome FROM usuarios WHERE login = %s"
        cursor.execute(query, (login,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def criar_usuario(login, password, nome):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        novo_uuid = str(uuid.uuid4())
        # Proteção LGPD: Hash de senha seguro
        password_hash = generate_password_hash(password)
        query = "INSERT INTO usuarios (uuid, login, password, nome) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (novo_uuid, login, password_hash, nome))
        conn.commit()
        return novo_uuid
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

def verificar_senha(usuario_db, password_digitada):
    if not usuario_db or 'password' not in usuario_db:
        return False
    return check_password_hash(usuario_db['password'], password_digitada)
