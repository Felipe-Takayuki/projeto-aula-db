import sqlite3

def criar_tabela_compra():
    try:
        conexao = sqlite3.connect("mercadinho.db")
        cursor = conexao.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS COMPRA (
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
        print("Tabela COMPRA criada com sucesso!")
        
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela COMPRA: {e}")
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    criar_tabela_compra()