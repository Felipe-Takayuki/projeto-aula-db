import sqlite3


def initCategoriaTB(conexao): 
    cursor = conexao.cursor()
    try: 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL UNIQUE
        );""")
        print("Tabela categoria criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela categoria: {e}")
