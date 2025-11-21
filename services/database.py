import sqlite3

def conectaBD():
    conexao = sqlite3.connect("mercadinho.db")
    return conexao

def initDB(): 
    from services.categoria_service import initCategoriaTB
    from services.cliente_service import initClienteTB
    from services.produto_service import initProdutoTB
    from services.funcionario_service import initFuncionarioTB
    from services.compra_service import initCompraTB
    from services.fornecedor_service import initFornecedorTB
    conexao = conectaBD()
    initCategoriaTB(conexao=conexao)
    initClienteTB(conexao=conexao)
    initProdutoTB(conexao=conexao)
    initFuncionarioTB(conexao=conexao)
    initFornecedorTB(conexao=conexao)
    initCompraTB(conexao=conexao)
