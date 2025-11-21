import sqlite3
def initClienteTB(conexao):
    cursor = conexao.cursor()

    try: 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL UNIQUE,
            cpf VARCHAR(11) NOT NULL UNIQUE,
            telefone VARCHAR(11) NOT NULL           
        );""")

        print("Tabela cliente criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela cliente: {e}")
