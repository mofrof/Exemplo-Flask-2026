import mysql.connector
import config
from models import usuario_model, jogo_model

def inicializar_banco():
    print("Criando banco de dados e tabelas...")
    conn = mysql.connector.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD
    )
    cursor = conn.cursor()

    with open('schema.sql', 'r', encoding='utf-8') as f:
        statements = f.read().split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Banco de dados configurado!")

    # Inserir usuário de teste caso não exista
    user = usuario_model.buscar_usuario_por_login('admin')
    if not user:
        print("Criando usuário administrador inicial (login: admin / senha: admin123)...")
        usuario_model.criar_usuario('admin', 'admin123', 'Administrador Jogoteca')

    # Inserir jogos de teste
    if jogo_model.listar_jogos()['total_itens'] == 0:
        print("Inserindo jogos iniciais para demonstração...")
        jogo_model.criar_jogo('Super Mario World', 'Console', '1990-11-21', None)
        jogo_model.criar_jogo('The Witcher 3: Wild Hunt', 'PC', '2015-05-19', None)
        jogo_model.criar_jogo('Pokémon Red', 'Portatil', '1996-02-27', None)

    print("População inicial concluída com sucesso!")

if __name__ == '__main__':
    inicializar_banco()
