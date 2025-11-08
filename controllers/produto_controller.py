import sqlite3
from models.produto_model import Produto 
from services.database import conectaBD

def incluirProduto(produto):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO PRODUTO (NOME, DESCRICAO, Quantidade_Produto, PRECO, id_categoria)
            VALUES (?, ?, ?, ?, ?) """, (
            produto.get_nome(),
            produto.get_descricao(),
            produto.get_quantidade(),
            produto.get_preco(),
            produto.get_id_categoria()
        )) 
        
        conexao.commit()
        print("Produto inserido com sucesso!")
        return True
        
    except sqlite3.Error as e:
        print(f"Erro ao inserir produto: {e}")
        return False
        
    finally:
        conexao.close()

def consultarProdutos():
    conexao = conectaBD()
    cursor = conexao.cursor()
    
    lista_de_produtos = []
    
    try:
        cursor.execute("""
            SELECT 
                P.id, P.NOME, P.DESCRICAO, P.Quantidade_Produto, P.PRECO, 
                C.NOME as Categoria_Nome, P.id_categoria
            FROM PRODUTO P
            JOIN CATEGORIA C ON P.id_categoria = C.id
            ORDER BY P.NOME
        """)
        
        rows = cursor.fetchall()
        dados_para_tabela = []
        for row in rows:
            dados_para_tabela.append({
                "ID": row[0],
                "Nome": row[1],
                "Descrição": row[2],
                "Quantidade": row[3],
                "Preço (R$)": row[4],
                "Categoria": row[5],
                "ID_Categoria": row[6] 
            })
            
        return dados_para_tabela
    
    except sqlite3.Error as e:
        print(f"Erro ao consultar produtos: {e}")
        return []
    
    finally:
        conexao.close()
    
def excluirProduto(id):

    conexao = conectaBD()
    cursor = conexao.cursor()
    
    try:
        cursor.execute("DELETE FROM produto WHERE id = ?", (id,))
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Produto com id {id} excluído com sucesso!")
            return True
        else:
            print(f"Nenhum produto encontrado com o id {id}.")
            return False
            
    except sqlite3.Error as e:
        if "FOREIGN KEY constraint failed" in str(e):
             print(f"Erro: O produto com ID {id} está em uma Venda e não pode ser excluído.")
        else:
            print(f"Erro ao excluir produto: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()

def alterarProduto(produto):
    conexao = conectaBD()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE produto 
            SET nome = ?, descricao = ?, quantidade_produto = ?, preco = ?, id_categoria = ?
            WHERE id = ?
        """, (
            produto.get_nome(),
            produto.get_descricao(),
            produto.get_quantidade(),
            produto.get_preco(),
            produto.get_id_categoria(),
            produto.get_id()
        ))
        
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Produto com id {produto.get_id()} alterado com sucesso!")
            return True
        else:
            print(f"Nenhum produto encontrado com o id {produto.get_id()}.")
            return False
            
    except sqlite3.Error as e:
        print(f"Erro ao alterar produto: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()