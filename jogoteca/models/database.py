import mysql.connector
import config

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD,
            database=config.MYSQL_DB
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro na conexão com o banco de dados MySQL: {err}")
        raise err
