import sqlite3

conexao = sqlite3.connect("mercadinho.db")

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS CATEGORIA (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME VARCHAR(100) NOT NULL UNIQUE
);""")

cursor.close()

print("Tabela CATEGORIA criada com sucesso!")