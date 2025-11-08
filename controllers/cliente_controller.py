import sqlite3
from models.pessoa_model import Pessoa
from services.database import conectaBD

def incluirCliente(pessoa: Pessoa):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO cliente (nome, cpf, telefone)
            VALUES (?, ?, ?)
        """, (
            pessoa.get_nome(), pessoa.get_cpf(), pessoa.get_telefone()
        )) 
        
        conexao.commit()
        print("Cliente inserido com sucesso!")
        return True
        
    except sqlite3.Error as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"Erro ao inserir cliente: O nome '{pessoa.get_nome()}' já existe.")
        else:
            print(f"Erro ao inserir cliente: {e}")
        return False 
        
    finally:
        conexao.close()

def consultarClientes():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    lista_de_clientes = [] 
    
    try:
        cursor.execute('SELECT id, nome, cpf, telefone FROM cliente ORDER BY nome')
        rows = cursor.fetchall()
        

        for row in rows:
            pessoa = Pessoa(id=row[0], nome=row[1], cpf=row[2], telefone=row[3])
            lista_de_clientes.append(pessoa)
            
        return lista_de_clientes
    
    except sqlite3.Error as e:
        print(f"Erro ao consultar clientes: {e}")
        return [] 
    
    finally:
        conexao.close()

def excluirCliente(id):

    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DELETE FROM cliente WHERE id = ?", (id,))
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Cliente com id {id} excluído com sucesso!")
            return True
        else:
            print(f"Nenhum cliente encontrado com o id {id}.")
            return False
            
    except sqlite3.Error as e:
        if "FOREIGN KEY constraint failed" in str(e):
             print(f"Erro: O cliente com ID {id} está em uma Venda e não pode ser excluído.")
        else:
            print(f"Erro ao excluir o cliente: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()

def alterarCliente(pessoa: Pessoa):
    conexao = conectaBD()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE cliente 
            SET nome = ?,
            SET cpf = ?,
            SET telefone = ? 
            WHERE id = ?
        """, (
            pessoa.get_nome(),
            pessoa.get_cpf(),
            pessoa.get_telefone(),
            pessoa.get_id()
        ))
        
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"cliente com id {pessoa.get_id()} alterada com sucesso!")
            return True
        else:
            print(f"Nenhum cliente encontrado com o id {pessoa.get_id()}.")
            return False
            
    except sqlite3.Error as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"Erro ao alterar cliente: O nome '{pessoa.get_nome()}' já existe.")
        else:
            print(f"Erro ao alterar cliente: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()