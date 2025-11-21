import sqlite3
def initProdutoTB(conexao):    
    try: 
        cursor = conexao.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            descricao VARCHAR(100),
            quantidade_produto INT NOT NULL CHECK (quantidade_produto >= 0),
            preco DECIMAL(10, 2) NOT NULL CHECK (preco > 0),
            id_categoria INTEGER NOT NULL,
            id_fornecedor INTEGER NOT NULL,
            FOREIGN KEY (id_categoria) REFERENCES categoria(id),
            FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id) 
        );""")

        cursor.close()
        print("Tabela produto criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela produto: {e}")
