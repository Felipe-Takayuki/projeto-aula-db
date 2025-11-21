import sqlite3
from models.fornecedor_model import Fornecedor
from services.database import conectaBD

def incluirFornecedor(fornecedor):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO fornecedor (nome, cnpj, telefone)
            VALUES (?, ?, ?)
        """, (
            fornecedor.get_nome(),
            fornecedor.get_cnpj(),
            fornecedor.get_telefone()
        )) 
        
        conexao.commit()
        print("Fornecedor inserido com sucesso!")
        return True
        
    except sqlite3.Error as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"Erro: O CNPJ '{fornecedor.get_cnpj()}' já está cadastrado.")
        else:
            print(f"Erro ao inserir fornecedor: {e}")
        return False
        
    finally:
        conexao.close()

def consultarFornecedores():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    lista_fornecedores = []
    
    try:
        cursor.execute('SELECT * FROM fornecedor ORDER BY nome')
        rows = cursor.fetchall()
        
        for row in rows:
            fornecedor = Fornecedor(id=row[0], nome=row[1], cnpj=row[2], telefone=row[3])
            lista_fornecedores.append(fornecedor)
            
        return lista_fornecedores
    
    except sqlite3.Error as e:
        print(f"Erro ao consultar fornecedores: {e}")
        return []
    
    finally:
        conexao.close()

def alterarFornecedor(fornecedor):
    conexao = conectaBD()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE fornecedor 
            SET nome = ?, cnpj = ?, telefone = ?
            WHERE id = ?
        """, (
            fornecedor.get_nome(),
            fornecedor.get_cnpj(),
            fornecedor.get_telefone(),
            fornecedor.get_id()
        ))
        
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Fornecedor com ID {fornecedor.get_id()} alterado com sucesso!")
            return True
        else:
            print("Fornecedor não encontrado.")
            return False
            
    except sqlite3.Error as e:
        print(f"Erro ao alterar fornecedor: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()

def excluirFornecedor(id):
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DELETE FROM produto WHERE id_fornecedor = ?", (id,))
        cursor.execute("DELETE FROM fornecedor WHERE id = ?", (id,))
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Fornecedor com ID {id} excluído com sucesso!")
            return True
        else:
            print("Fornecedor não encontrado.")
            return False
            
    except sqlite3.Error as e:
        if "FOREIGN KEY constraint failed" in str(e):
             print(f"Erro: O fornecedor não pode ser excluído pois tem vínculos.")
        else:
            print(f"Erro ao excluir fornecedor: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()
