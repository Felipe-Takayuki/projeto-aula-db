import streamlit as st
import pandas as pd

import controllers.produto_controller as ProdutoController
import controllers.cliente_controller as ClienteController
import controllers.funcionario_controller as FuncionarioController
import controllers.compra_controller as CompraController 

def show_page():
    try:
        st.image("assets/images/banner.png", use_container_width=True)
    except:
        st.warning("Banner não encontrado em assets/images/banner.png")
        
    st.title("Mercadinho do Paul")
    
    st.markdown("""
    O Mercadinho do Paul é um estabelecimento comercial de bairro que oferece uma variedade de produtos 
    para atender às necessidades do dia a dia. Com um ambiente acolhedor e atendimento personalizado, 
    o mercadinho se destaca pela praticidade e pela proximidade com seus clientes.
    """)
    
    st.divider()

    try:
        produtos = ProdutoController.consultarProdutos()
        clientes = ClienteController.consultarClientes()
        funcionarios = FuncionarioController.consultarFuncionarios()
        compras = CompraController.consultarCompras()
        qtd_produtos = len(produtos) if produtos else 0
        qtd_clientes = len(clientes) if clientes else 0
        qtd_funcionarios = len(funcionarios) if funcionarios else 0
        qtd_vendas = len(compras) if compras else 0

    except Exception as e:
        st.error(f"Não foi possível carregar os dados do painel: {e}")
        qtd_produtos = 0
        qtd_clientes = 0
        qtd_funcionarios = 0
        qtd_vendas = 0

    st.subheader("Resumo do Negócio")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(" Produtos", qtd_produtos)
        
    with col2:
        st.metric(" Clientes", qtd_clientes)
        
    with col3:
        st.metric(" Funcionários", qtd_funcionarios)
        
    with col4:
        st.metric(" Vendas Totais", qtd_vendas)

    st.divider()

    if produtos:
        estoque_baixo = [p for p in produtos if p['Quantidade'] < 5]
        
        if estoque_baixo:
            st.warning(f" Atenção! Existem {len(estoque_baixo)} produtos com estoque baixo.")
            
            df_baixo = pd.DataFrame(estoque_baixo)
            st.dataframe(
                df_baixo[['Nome', 'Quantidade', 'Preço (R$)']], 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success(" O estoque está saudável (todos os produtos acima de 5 unidades).")