import sqlite3

def conectaBD():
    conexao = sqlite3.connect("mercadinho.db")
    return conexao