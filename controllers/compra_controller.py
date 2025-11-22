import sqlite3
from models.compra_model import Compra

def conectaBD():
    return sqlite3.connect("mercadinho.db")

def incluirCompra(compra):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT PRECO, Quantidade_Produto FROM PRODUTO WHERE id = ?", (compra.get_id_produto(),))
        dados_produto = cursor.fetchone()
        
        if not dados_produto:
            print("Produto não encontrado!")
            return False
            
        preco_unitario = dados_produto[0]
        estoque_atual = dados_produto[1]
        
        qtd_comprada = compra.get_quantidade()
        if estoque_atual < qtd_comprada:
            print(f"Estoque insuficiente! Disponível: {estoque_atual}")
            return False
        valor_total = preco_unitario * qtd_comprada

        cursor.execute("""
            INSERT INTO COMPRA (id_cliente, id_funcionario, id_produto, quantidade_produto, valor_total)
            VALUES (?, ?, ?, ?, ?)
        """, (
            compra.get_id_cliente(),
            compra.get_id_funcionario(),
            compra.get_id_produto(),
            qtd_comprada,
            valor_total
        ))

        novo_estoque = estoque_atual - qtd_comprada
        cursor.execute("UPDATE PRODUTO SET Quantidade_Produto = ? WHERE id = ?", (novo_estoque, compra.get_id_produto()))
        
        conexao.commit()
        print("Compra registrada com sucesso!")
        return True
        
    except sqlite3.Error as e:
        print(f"Erro ao registrar compra: {e}")
        return False
    finally:
        conexao.close()

def consultarCompras():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    lista_compras = []
    
    try:
        sql = """
        SELECT 
            Cp.id, 
            Cl.NOME as Cliente, 
            F.NOME as Funcionario, 
            P.NOME as Produto, 
            Cp.quantidade_produto, 
            Cp.valor_total,
            Cp.data_venda
        FROM COMPRA Cp
        JOIN CLIENTE Cl ON Cp.id_cliente = Cl.id
        JOIN FUNCIONARIO F ON Cp.id_funcionario = F.id
        JOIN PRODUTO P ON Cp.id_produto = P.id
        ORDER BY Cp.id DESC
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        for row in rows:
            lista_compras.append({
                "ID": row[0],
                "Cliente": row[1],
                "Funcionário": row[2],
                "Produto": row[3],
                "Qtd": row[4],
                "Total (R$)": row[5],
                "Data": row[6]
            })
            
        return lista_compras
    
    except sqlite3.Error as e:
        print(f"Erro ao consultar compras: {e}")
        return []
    finally:
        conexao.close()

def excluirCompra(id_compra):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT id_produto, quantidade_produto FROM COMPRA WHERE id = ?", (id_compra,))
        dados = cursor.fetchone()
        
        if not dados:
            return False    
        id_produto = dados[0]
        qtd_comprada = dados[1]

        cursor.execute("DELETE FROM COMPRA WHERE id = ?", (id_compra,))
        cursor.execute("UPDATE PRODUTO SET Quantidade_Produto = Quantidade_Produto + ? WHERE id = ?", (qtd_comprada, id_produto))
        conexao.commit()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao excluir compra: {e}")
        return False
    finally:
        conexao.close()