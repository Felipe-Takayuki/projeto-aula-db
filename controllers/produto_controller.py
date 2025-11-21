import sqlite3
from models.produto_model import Produto 
from services.database import conectaBD

def incluirProduto(produto: Produto):
    conexao = conectaBD()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            INSERT INTO produto(nome, descricao, quantidade_produto, preco, id_categoria, id_fornecedor)
            VALUES (?, ?, ?, ?, ?, ?) """, (
            produto.get_nome(),
            produto.get_descricao(),
            produto.get_quantidade(),
            produto.get_preco(),
            produto.get_id_categoria(),
            produto.get_id_fornecedor()
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
    
    try:
        cursor.execute("""
            SELECT 
                P.id, 
                P.nome, 
                P.descricao, 
                P.quantidade_produto, 
                P.preco, 
                C.nome AS categoria_nome,
                F.nome AS fornecedor_nome,
                P.id_categoria,
                P.id_fornecedor
            FROM produto P
            JOIN categoria C ON P.id_categoria = C.id
            JOIN fornecedor F ON P.id_fornecedor = F.id
            ORDER BY P.nome
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
                "Fornecedor": row[6],  # <-- AGORA VEM O NOME!
                "ID_Categoria": row[7],
                "ID_Fornecedor": row[8]
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
        cursor.execute("DELETE FROM compra WHERE id_produto = ?", id)
        cursor.execute("DELETE FROM produto WHERE id = ?", id)
        conexao.commit()
        
        if cursor.rowcount > 0:
            print(f"Produto com id {id} excluído com sucesso!")
            return True
        else:
            print(f"Nenhum produto encontrado com o id {id}.")
            return False
            
    except sqlite3.Error as e:
        print(f"Erro ao excluir produto: {e}")
        return False
        
    finally:
        if conexao:
            conexao.close()

def alterarProduto(produto: Produto):
    conexao = conectaBD()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE produto 
            SET nome = ?, descricao = ?, quantidade_produto = ?, preco = ?, id_categoria = ?, id_fornecedor = ?
            WHERE id = ?
        """, (
            produto.get_nome(),
            produto.get_descricao(),
            produto.get_quantidade(),
            produto.get_preco(),
            produto.get_id_categoria(),
            produto.get_id_fornecedor(),
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