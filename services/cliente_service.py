from services.database import conectaBD

def initClienteTB(conexao):
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL UNIQUE,
        cpf VARCHAR(20) NOT NULL UNIQUE,
        telefone VARCHAR(15) NOT NULL           
    );""")

    cursor.close()
    print("Tabela cliente criada com sucesso!")
