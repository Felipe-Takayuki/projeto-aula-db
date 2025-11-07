import sqlite3

conexao = sqlite3.connect("mercadinho.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS PRODUTO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME VARCHAR(100) NOT NULL,
    DESCRICAO VARCHAR(100),
    Quantidade_Produto INT NOT NULL CHECK (Quantidade_Produto >= 0),
    PRECO DECIMAL(10, 2) NOT NULL CHECK (PRECO > 0),
    id_categoria INTEGER NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES CATEGORIA (id) 
);""")

cursor.close()
print("Tabela PRODUTO criada com sucesso!")