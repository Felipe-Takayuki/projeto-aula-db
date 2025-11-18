import streamlit as st
import pandas as pd
import controllers.produto_controller as ProdutoController
import controllers.categoria_controller as CategoriaController
from models.produto_model import Produto

@st.dialog("Cadastro de cliente")
def modal_categoria():
    with st.form(key="form_cadastro", clear_on_submit=True):
        categoria = st.text_input("Nome da Categoria:", placeholder="Ex: Frios")
        submit_button = st.form_submit_button("Incluir")

        if submit_button:
            if categoria:
                novo_cliente = Categoria(id=None,nome=categoria)

                if CategoriaController.incluirCategoria(novo_cliente):
                    st.session_state.reload_clientes = True
                    st.success(f"Categoria '{categoria}' incluída com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao incluir categoria.")
            else:
                st.warning("O nome do categoria é obrigatória.")

def show_page():
    
    st.title("Cadastro de Produtos")
    
    tab_incluir, tab_consultar, tab_alterar, tab_excluir = st.tabs([
        "Incluir", "Consultar", "Alterar", "Excluir"
    ])

    with tab_incluir:
        st.header("Incluir Novo Produto")

        lista_categorias = CategoriaController.consultarCategorias()
        
        if not lista_categorias:
            st.warning("É necessário cadastrar pelo menos uma Categoria antes de incluir um Produto.")
            if st.button("Adicionar novo cliente"):
                modal_categoria()
        else:
            map_cat = {cat.get_nome(): cat.get_id() for cat in lista_categorias}
            
            with st.form(key="incluir_produto", clear_on_submit=True):
                nome = st.text_input("Nome do Produto:", placeholder="Ex: Leite Integral")
                descricao = st.text_input("Descrição:", placeholder="Ex: Caixa 1L")
                col1, col2 = st.columns(2)
                with col1:
                    quantidade = st.number_input("Quantidade em Estoque:", min_value=0, step=1)
                with col2:
                    preco = st.number_input("Preço Unitário (R$):", min_value=0.0, format="%.2f")
                cat_nome_selecionado = st.selectbox(
                    "Selecione a Categoria:", 
                    options=map_cat.keys()
                )
                
                submit_button = st.form_submit_button("Incluir Produto")

                if submit_button:
                    id_categoria_selecionada = map_cat[cat_nome_selecionado]
                    novo_produto = Produto(
                        id=None, 
                        nome=nome, 
                        descricao=descricao, 
                        quantidade=quantidade, 
                        preco=preco, 
                        id_categoria=id_categoria_selecionada
                    )

                    if ProdutoController.incluirProduto(novo_produto):
                        st.success(f"Produto '{nome}' incluído com sucesso!")
                    else:
                        st.error("Erro ao incluir produto.")

    with tab_consultar:
        st.header("Consultar Produtos")

        lista_produtos = ProdutoController.consultarProdutos()
        
        if not lista_produtos:
            st.info("Nenhum produto cadastrado.")
        else:
            df = pd.DataFrame(lista_produtos)

            df['Preço (R$)'] = df['Preço (R$)'].map("R$ {:,.2f}".format)

            df_display = df.drop(columns=["ID_Categoria"])
            
            st.dataframe(df_display.set_index("ID"), use_container_width=True)

    with tab_alterar:
        st.header("Alterar Produto")
        
        lista_produtos = ProdutoController.consultarProdutos()
        
        if not lista_produtos:
            st.info("Nenhum produto cadastrado para alterar.")
        else:
            map_prod = {f"{prod['ID']} - {prod['Nome']}": prod for prod in lista_produtos}
            prod_selecionado_str = st.selectbox(
                "Selecione o Produto:", 
                options=map_prod.keys()
            )
            prod_data = map_prod[prod_selecionado_str]
            with st.form(key="alterar_produto"):
                nome = st.text_input("Nome do Produto:", value=prod_data['Nome'])
                descricao = st.text_input("Descrição:", value=prod_data['Descrição'])
                
                col1, col2 = st.columns(2)
                with col1:
                    quantidade = st.number_input("Quantidade:", min_value=0, step=1, value=prod_data['Quantidade'])
                with col2:
                    preco = st.number_input("Preço Unitário (R$):", min_value=0.0, format="%.2f", value=prod_data['Preço (R$)'])
                lista_categorias = CategoriaController.consultarCategorias()
                map_cat = {cat.get_nome(): cat.get_id() for cat in lista_categorias}
                nomes_categorias = list(map_cat.keys())
            
                try:
                    index_cat = nomes_categorias.index(prod_data['Categoria'])
                except ValueError:
                    index_cat = 0 
                
                cat_nome_selecionado = st.selectbox(
                    "Categoria:", 
                    options=nomes_categorias, 
                    index=index_cat
                )
                
                alterar_button = st.form_submit_button("Salvar Alterações")
                
                if alterar_button:
                    id_categoria_nova = map_cat[cat_nome_selecionado]
                    
                    produto_alterado = Produto(
                        id=prod_data['ID'], 
                        nome=nome,
                        descricao=descricao,
                        quantidade=quantidade,
                        preco=preco,
                        id_categoria=id_categoria_nova
                    )
                    
                    if ProdutoController.alterarProduto(produto_alterado):
                        st.success("Produto alterado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao alterar produto.")
    with tab_excluir:
        st.header("Excluir Produto")
        
        lista_produtos = ProdutoController.consultarProdutos()
        
        if not lista_produtos:
            st.info("Nenhum produto cadastrado para excluir.")
        else:
            map_prod = {f"{prod['ID']} - {prod['Nome']}": prod['ID'] for prod in lista_produtos}
            prod_selecionado_str = st.selectbox(
                "Selecione o Produto para Excluir:", 
                options=map_prod.keys(), 
                key="select_excluir_prod"
            )
            
            id_para_excluir = map_prod[prod_selecionado_str]
            
            if st.button("Excluir Produto Selecionado", type="primary"):
                if ProdutoController.excluirProduto(id_para_excluir):
                    st.success("Produto excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao excluir produto. (Verifique se ele está em uso em uma Venda)")