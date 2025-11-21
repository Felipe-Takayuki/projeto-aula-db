# services/tabela_fornecedor.py
import sqlite3

def initFornecedorTB(conexao):
    
    try:
        cursor = conexao.cursor()
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS fornecedor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            cnpj VARCHAR(14) NOT NULL UNIQUE,
            telefone VARCHAR(11)
        );
        """)
        
        conexao.commit()
        print("Tabela fornecedor criada com sucesso!")
        
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela fornecedor: {e}")


