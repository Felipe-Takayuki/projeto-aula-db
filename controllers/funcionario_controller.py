import sqlite3
from models.funcionario_model import Funcionario
from services.database import conectaBD

def incluirFuncionario(funcionario: Funcionario):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO funcionario (nome, cpf, telefone, salario)
            VALUES (?, ?, ?, ?)
        """, (
            funcionario.get_nome(), funcionario.get_cpf(), funcionario.get_telefone(), funcionario.get_salario()
        )) 
        
        conexao.commit()
        print("Cliente inserido com sucesso!")
        return True
        
    except sqlite3.Error as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"Erro ao inserir funcionario: O nome '{funcionario.get_nome()}' já existe.")
        else:
            print(f"Erro ao inserir funcionario: {e}")
        return False 
        
    finally:
        conexao.close()

def consultarFuncionarios():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    lista_de_funcionarios = [] 
    
    try:
        cursor.execute('SELECT id, nome, cpf, telefone, salario FROM funcionario ORDER BY nome')
        rows = cursor.fetchall()
        

        for row in rows:
            funcionario = Funcionario(id=row[0], nome=row[1], cpf=row[2], telefone=row[3], salario=row[4])
            lista_de_funcionarios.append(funcionario)
            
        return lista_de_funcionarios
    
    except sqlite3.Error as e:
        print(f"Erro ao consultar clientes: {e}")
        return [] 
    
    finally:
        conexao.close()

def excluirFuncionario(id):

    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DELETE FROM funcionario WHERE id = ?", (id,))
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Funcionário com id {id} excluído com sucesso!")
            return True
        else:
            print(f"Nenhum funcionario encontrado com o id {id}.")
            return False
            
    except sqlite3.Error as e:
        if "FOREIGN KEY constraint failed" in str(e):
             print(f"Erro: O funcionario com ID {id} está fazendo uma Venda e não pode ser excluído.")
        else:
            print(f"Erro ao excluir o funcionario: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()

def alterarFuncionario(funcionario: Funcionario):
    conexao = conectaBD()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE funcionario
            SET nome = ?,
                cpf = ?,
                telefone = ?,
                salario = ? 
            WHERE id = ?
        """, (
            funcionario.get_nome(),
            funcionario.get_cpf(),
            funcionario.get_telefone(),
            funcionario.get_salario(),
            funcionario.get_id()
        ))
        
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Cliente com id {funcionario.get_id()} alterado com sucesso!")
            return True
        else:
            print(f"Nenhum cliente encontrado com o id {funcionario.get_id()}.")
            return False
            
    except sqlite3.Error as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"Erro ao alterar cliente: O nome '{funcionario.get_nome()}' já existe.")
        else:
            print(f"Erro ao alterar cliente: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()
