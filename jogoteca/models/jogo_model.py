import uuid
from models.database import get_db_connection

def listar_jogos(filtro_nome="", filtro_ano="", ordem_campo="nome", ordem_direcao="ASC", pagina=1, itens_por_pagina=6):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        where_clauses = []
        params = []

        if filtro_nome:
            where_clauses.append("nome LIKE %s")
            params.append(f"%{filtro_nome}%")

        if filtro_ano:
            where_clauses.append("YEAR(anoLancamento) = %s")
            params.append(filtro_ano)

        where_str = ""
        if where_clauses:
            where_str = "WHERE " + " AND ".join(where_clauses)

        # Sanitização de ordenação (evita SQL Injection)
        campos_validos = {'nome': 'nome', 'ano': 'anoLancamento', 'plataforma': 'plataforma'}
        campo_sql = campos_validos.get(ordem_campo, 'nome')
        direcao_sql = 'DESC' if str(ordem_direcao).upper() == 'DESC' else 'ASC'

        count_query = f"SELECT COUNT(*) AS total FROM jogos {where_str}"
        cursor.execute(count_query, params)
        res = cursor.fetchone()
        total_itens = res['total'] if res else 0

        offset = (pagina - 1) * itens_por_pagina
        data_query = f"""
            SELECT uuid, nome, plataforma, anoLancamento, localImagemCapaJogo 
            FROM jogos 
            {where_str} 
            ORDER BY {campo_sql} {direcao_sql} 
            LIMIT %s OFFSET %s
        """
        cursor.execute(data_query, params + [itens_por_pagina, offset])
        jogos = cursor.fetchall()

        total_paginas = (total_itens + itens_por_pagina - 1) // itens_por_pagina if total_itens > 0 else 1

        return {
            'jogos': jogos,
            'total_itens': total_itens,
            'total_paginas': total_paginas,
            'pagina_atual': pagina
        }
    finally:
        cursor.close()
        conn.close()

def buscar_jogo_por_uuid(jogo_uuid):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT uuid, nome, plataforma, anoLancamento, localImagemCapaJogo FROM jogos WHERE uuid = %s"
        cursor.execute(query, (jogo_uuid,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def buscar_jogo_por_nome(nome):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT uuid, nome FROM jogos WHERE nome = %s"
        cursor.execute(query, (nome,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def criar_jogo(nome, plataforma, ano_lancamento, local_imagem):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        novo_uuid = str(uuid.uuid4())
        query = """
            INSERT INTO jogos (uuid, nome, plataforma, anoLancamento, localImagemCapaJogo) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (novo_uuid, nome, plataforma, ano_lancamento, local_imagem))
        conn.commit()
        return novo_uuid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def atualizar_jogo(jogo_uuid, nome, plataforma, ano_lancamento, local_imagem=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if local_imagem:
            query = """
                UPDATE jogos 
                SET nome = %s, plataforma = %s, anoLancamento = %s, localImagemCapaJogo = %s 
                WHERE uuid = %s
            """
            cursor.execute(query, (nome, plataforma, ano_lancamento, local_imagem, jogo_uuid))
        else:
            query = """
                UPDATE jogos 
                SET nome = %s, plataforma = %s, anoLancamento = %s 
                WHERE uuid = %s
            """
            cursor.execute(query, (nome, plataforma, ano_lancamento, jogo_uuid))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def deletar_jogo(jogo_uuid):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM jogos WHERE uuid = %s"
        cursor.execute(query, (jogo_uuid,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
