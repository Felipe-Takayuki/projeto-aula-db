


def initCategoriaTB(conexao): 
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL UNIQUE
    );""")

    cursor.close()

    print("Tabela categoria criada com sucesso!")