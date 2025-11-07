import streamlit as st
import pandas as pd
import controllers.categoria_controller as CategoriaController
from models.categoria_model import Categoria

def show_page():
    
    st.title("Cadastro de Categorias")

    tab_incluir, tab_consultar, tab_alterar, tab_excluir = st.tabs([
        "Incluir", 
        "Consultar", 
        "Alterar", 
        "Excluir"
    ])

    with tab_incluir:
        st.header("Incluir Nova Categoria")
  
        with st.form(key="incluir_categoria", clear_on_submit=True):
            nome = st.text_input("Nome da Categoria:", placeholder="Ex: Frios e Laticínios")
            submit_button = st.form_submit_button("Incluir")

            if submit_button:
                if nome:
                    nova_categoria = Categoria(id=None, nome=nome)

                    if CategoriaController.incluirCategoria(nova_categoria):
                        st.success(f"Categoria '{nome}' incluída com sucesso!")
                    else:
                        st.error("Erro ao incluir categoria. (Verifique se ela já existe)")
                else:
                    st.warning("O nome da categoria é obrigatório.")

    with tab_consultar:
        st.header("Consultar Categorias")

        lista_categorias = CategoriaController.consultarCategorias()
        
        if not lista_categorias:
            st.info("Nenhuma categoria cadastrada.")
        else:
            data_para_tabela = []
            for cat in lista_categorias:
                data_para_tabela.append({
                    "ID": cat.get_id(),
                    "Nome": cat.get_nome()
                })
            
            df = pd.DataFrame(data_para_tabela).set_index("ID")
            st.dataframe(df, use_container_width=True)

    with tab_alterar:
        st.header("Alterar Categoria")

        lista_categorias = CategoriaController.consultarCategorias()
        
        if not lista_categorias:
            st.info("Nenhuma categoria cadastrada para alterar.")
        else:
            lista_nomes_categorias = [cat.get_nome() for cat in lista_categorias]
            
            cat_nome_selecionado = st.selectbox(
                "Selecione a Categoria:", 
                options=lista_nomes_categorias
            )
            
            id_para_alterar = None
            for cat in lista_categorias:
                if cat.get_nome() == cat_nome_selecionado:
                    id_para_alterar = cat.get_id()
                    break
            
            if id_para_alterar:
                with st.form(key="alterar_categoria"):
                    novo_nome = st.text_input("Novo Nome:", value=cat_nome_selecionado)
                    alterar_button = st.form_submit_button("Alterar")
                    
                    if alterar_button:
                        if novo_nome:
                            cat_alterada = Categoria(id=id_para_alterar, nome=novo_nome)
                            if CategoriaController.alterarCategoria(cat_alterada):
                                st.success("Categoria alterada com sucesso!")
                                st.rerun() 
                            else:
                                st.error("Erro ao alterar categoria. (Verifique se o nome já existe)")
                        else:
                            st.warning("O novo nome é obrigatório.")

    with tab_excluir:
        st.header("Excluir Categoria")
        
        lista_categorias = CategoriaController.consultarCategorias()
        
        if not lista_categorias:
            st.info("Nenhuma categoria cadastrada para excluir.")
        else:
            lista_nomes_categorias = [cat.get_nome() for cat in lista_categorias]
            
            cat_nome_selecionado = st.selectbox(
                "Selecione a Categoria para Excluir:", 
                options=lista_nomes_categorias, 
                key="select_excluir" 
            )

            id_para_excluir = None
            for cat in lista_categorias:
                if cat.get_nome() == cat_nome_selecionado:
                    id_para_excluir = cat.get_id()
                    break
            
            if id_para_excluir:
                if st.button("Excluir Categoria Selecionada", type="primary"):
                    if CategoriaController.excluirCategoria(id_para_excluir):
                        st.success("Categoria excluída com sucesso!")
                        st.rerun() 
                    else:
                        st.error("Erro ao excluir categoria. (Verifique se ela está em uso por um Produto)")