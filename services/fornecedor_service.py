# services/tabela_fornecedor.py
import sqlite3

def criar_tabela_fornecedor():
    
    try:
        conexao = sqlite3.connect("mercadinho.db")
        cursor = conexao.cursor()
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS FORNECEDOR (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            NOME VARCHAR(100) NOT NULL,
            CNPJ VARCHAR(18) NOT NULL UNIQUE,
            TELEFONE VARCHAR(15)
        );
        """)
        
        conexao.commit()
        print("Tabela FORNECEDOR criada com sucesso!")
        
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela FORNECEDOR: {e}")
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    criar_tabela_fornecedor()