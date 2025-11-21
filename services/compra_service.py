import sqlite3

def initCompraTB(conexao):
    try:
        cursor = conexao.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS compra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_funcionario INTEGER NOT NULL,
            id_produto INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            valor_total DECIMAL(10, 2) NOT NULL,
            data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (id_cliente) REFERENCES CLIENTE (id),
            FOREIGN KEY (id_funcionario) REFERENCES FUNCIONARIO (id),
            FOREIGN KEY (id_produto) REFERENCES PRODUTO (id)
        );
        """)
        
        conexao.commit()
        print("Tabela compra criada com sucesso!")
        
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela compra: {e}")
    finally:
        if conexao:
            conexao.close()

