import sqlite3

DB_NAME = "ativos.db"
TABLE_NAME = "ativos"

COLUNAS = [
    "ids_dispositivos", "tipo_dispositivo", "marca_modelo", "status_propriedade",
    "usuario_responsavel", "possui_celular", "email", "linhas_telefonicas",
    "situacao_equipamento", "situacao_linha", "empresa_alugados", "imei1", "imei2"
]

def conectar_banco():
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criar_tabela():
    
    conn = conectar_banco()
    if not conn: return
    try:
        cursor = conn.cursor()
        comando_sql = f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                ids_dispositivos TEXT PRIMARY KEY NOT NULL,
                tipo_dispositivo TEXT,
                marca_modelo TEXT,
                status_propriedade TEXT,
                usuario_responsavel TEXT,
                possui_celular TEXT,
                email TEXT,
                linhas_telefonicas TEXT,
                situacao_equipamento TEXT,
                situacao_linha TEXT,
                empresa_alugados TEXT,
                imei1 TEXT,
                imei2 TEXT
            )
        '''
        cursor.execute(comando_sql)
        conn.commit()
    finally:
        if conn:
            conn.close()

def inserir_dados_iniciais():
    conn = conectar_banco()
    if not conn: return "Erro: Não foi possível conectar ao banco de dados."

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        if cursor.fetchone()[0] > 0:
            return "Aviso: O banco de dados já contém dados."

        dados_iniciais = [
            
        ]
        
        placeholders = ', '.join(['?'] * len(COLUNAS))
        colunas_str = ', '.join(COLUNAS)
        
        cursor.executemany(f"INSERT INTO {TABLE_NAME} ({colunas_str}) VALUES ({placeholders})", dados_iniciais)
        conn.commit()
        
        return "Sucesso: Banco de dados inicializado com os dados fornecidos."

    except sqlite3.Error as e:
        return f"Erro ao inserir dados iniciais: {e}"
    finally:
        if conn:
            conn.close()

def listar_ativos(coluna_ordenacao="usuario_responsavel", ordem="ASC"):
    if coluna_ordenacao not in COLUNAS:
        coluna_ordenacao = "usuario_responsavel"
    if ordem.upper() not in ["ASC", "DESC"]:
        ordem = "ASC"

    conn = conectar_banco()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY {coluna_ordenacao} {ordem}")
        return cursor.fetchall()
    finally:
        conn.close()

def buscar_ativos(termo, coluna_ordenacao="usuario_responsavel", ordem="ASC"):
    if coluna_ordenacao not in COLUNAS:
        coluna_ordenacao = "usuario_responsavel"
    if ordem.upper() not in ["ASC", "DESC"]:
        ordem = "ASC"

    conn = conectar_banco()
    if not conn: return []
    try:
        cursor = conn.cursor()
        where_clause = " OR ".join([f"{col} LIKE ?" for col in COLUNAS])
        search_term = f"%{termo}%"
        params = [search_term] * len(COLUNAS)

        query = f"SELECT * FROM {TABLE_NAME} WHERE {where_clause} ORDER BY {coluna_ordenacao} {ordem}"
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        conn.close()

def adicionar_ativo(dados):
    conn = conectar_banco()
    if not conn: return
    try:
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * len(COLUNAS))
        colunas_str = ', '.join(COLUNAS)
        valores = [dados.get(col, '') for col in COLUNAS]

        cursor.execute(f"INSERT INTO {TABLE_NAME} ({colunas_str}) VALUES ({placeholders})", valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise e
    finally:
        if conn:
            conn.close()

def atualizar_ativo(id_original, novos_dados):
    conn = conectar_banco()
    if not conn: return
    try:
        cursor = conn.cursor()
        
        set_clause = ', '.join([f"{col} = ?" for col in COLUNAS])
        valores = [novos_dados.get(col, '') for col in COLUNAS]
        valores.append(id_original) # Adiciona o ID original para a cláusula WHERE

        cursor.execute(f"UPDATE {TABLE_NAME} SET {set_clause} WHERE ids_dispositivos = ?", valores)
        conn.commit()
    except sqlite3.IntegrityError as e:
        raise e
    finally:
        if conn:
            conn.close()

def remover_ativo(id_dispositivo):
    conn = conectar_banco()
    if not conn: return
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE ids_dispositivos = ?", (id_dispositivo,))
        conn.commit()
    finally:
        if conn:
            conn.close()