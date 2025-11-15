import sqlite3
from models.cliente_model import Cliente
from services.database import conectaBD

def incluirCliente(cliente: Cliente):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO cliente (nome, cpf, telefone)
            VALUES (?, ?, ?)
        """, (
            cliente.get_nome(), cliente.get_cpf(), cliente.get_telefone()
        )) 
        
        conexao.commit()
        print("Cliente inserido com sucesso!")
        return True
        
    except sqlite3.Error as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"Erro ao inserir cliente: O nome '{cliente.get_nome()}' já existe.")
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
            cliente = Cliente(id=row[0], nome=row[1], cpf=row[2], telefone=row[3])
            lista_de_clientes.append(cliente)
            
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
            cursor.execute("DELETE FROM compra WHERE id_cliente = ?", id)
            cursor.execute("DELETE FROM cliente WHERE id = ?", (id,))

        else:
            print(f"Erro ao excluir o cliente: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()

def alterarCliente(cliente: Cliente):
    conexao = conectaBD()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE cliente
            SET nome = ?,
                cpf = ?,
                telefone = ?
            WHERE id = ?
        """, (
            cliente.get_nome(),
            cliente.get_cpf(),
            cliente.get_telefone(),
            cliente.get_id()
        ))
        
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Cliente com id {cliente.get_id()} alterado com sucesso!")
            return True
        else:
            print(f"Nenhum cliente encontrado com o id {cliente.get_id()}.")
            return False
            
    except sqlite3.Error as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"Erro ao alterar cliente: O nome '{cliente.get_nome()}' já existe.")
        else:
            print(f"Erro ao alterar cliente: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()
