def initFuncionarioTB(conexao):
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(100) NOT NULL UNIQUE,
        cpf VARCHAR(11) NOT NULL UNIQUE,
        telefone VARCHAR(11) NOT NULL,
        salario DECIMAL(10,2) NOT NULL         
    );""")

    cursor.close()
    print("Tabela cliente criada com sucesso!")
