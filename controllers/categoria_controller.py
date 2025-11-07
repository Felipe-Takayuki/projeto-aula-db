import sqlite3
from models.categoria_model import Categoria 
from services.database import conectaBD

def incluirCategoria(categoria):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO CATEGORIA (NOME)
            VALUES (?)
        """, (
            categoria.get_nome(), 
        )) 
        
        conexao.commit()
        print("Categoria inserida com sucesso!")
        return True
        
    except sqlite3.Error as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"Erro ao inserir categoria: O nome '{categoria.get_nome()}' já existe.")
        else:
            print(f"Erro ao inserir categoria: {e}")
        return False 
        
    finally:
        conexao.close()

def consultarCategorias():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    lista_de_categorias = [] 
    
    try:
        cursor.execute('SELECT * FROM CATEGORIA ORDER BY NOME')
        rows = cursor.fetchall()
        

        for row in rows:
            categoria = Categoria(id=row[0], nome=row[1])
            lista_de_categorias.append(categoria)
            
        return lista_de_categorias
    
    except sqlite3.Error as e:
        print(f"Erro ao consultar categorias: {e}")
        return [] 
    
    finally:
        conexao.close()
    

def excluirCategoria(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DELETE FROM CATEGORIA WHERE id = ?", (id,))
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Categoria com id {id} excluída com sucesso!")
            return True
        else:
            print(f"Nenhuma categoria encontrada com o id {id}.")
            return False
            
    except sqlite3.Error as e:
        if "FOREIGN KEY constraint failed" in str(e):
             print(f"Erro: A categoria com ID {id} está em uso por um Produto e não pode ser excluída.")
        else:
            print(f"Erro ao excluir categoria: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()

def alterarCategoria(categoria):
    conexao = conectaBD()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE CATEGORIA 
            SET NOME = ?
            WHERE id = ?
        """, (
            categoria.get_nome(),
            categoria.get_id()
        ))
        
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Categoria com id {categoria.get_id()} alterada com sucesso!")
            return True
        else:
            print(f"Nenhuma categoria encontrada com o id {categoria.get_id()}.")
            return False
            
    except sqlite3.Error as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"Erro ao alterar categoria: O nome '{categoria.get_nome()}' já existe.")
        else:
            print(f"Erro ao alterar categoria: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()