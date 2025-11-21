import streamlit as st
import pandas as pd
import controllers.fornecedor_controller as FornecedorController
from models.fornecedor_model import Fornecedor
from utils.formatter import format_cnpj, format_celular
def show_page():
    st.title("Cadastro de Fornecedores")

    tab_incluir, tab_consultar, tab_alterar, tab_excluir = st.tabs([
        "Incluir", "Consultar", "Alterar", "Excluir"
    ])

    with tab_incluir:
        st.header("Incluir Novo Fornecedor")
        
        with st.form(key="incluir_fornecedor", clear_on_submit=True):
            nome = st.text_input("Nome do Fornecedor:", placeholder="Ex: Atacadão dos Doces")
            cnpj = st.text_input("CNPJ:", placeholder="Ex: 00000000000100", max_chars=14)
            telefone = st.text_input("Telefone:", placeholder="Ex: 11999999999", max_chars=11)
            
            submit_button = st.form_submit_button("Cadastrar")
            
            if submit_button:
                if nome and cnpj:
                    novo_fornecedor = Fornecedor(id=None, nome=nome, cnpj=cnpj, telefone=telefone)
                    
                    if FornecedorController.incluirFornecedor(novo_fornecedor):
                        st.success(f"Fornecedor '{nome}' cadastrado com sucesso!")
                    else:
                        st.error("Erro ao cadastrar. Verifique se o CNPJ já existe.")
                else:
                    st.warning("Nome e CNPJ são obrigatórios.")

    with tab_consultar:
        st.header("Consultar Fornecedores")
        
        lista_fornecedores = FornecedorController.consultarFornecedores()
        
        if not lista_fornecedores:
            st.info("Nenhum fornecedor cadastrado.")
        else:
            dados = []
            for f in lista_fornecedores:
                dados.append({
                    "ID": f.get_id(),
                    "Nome": f.get_nome(),
                    "CNPJ": format_cnpj(f.get_cnpj()),
                    "Telefone": format_celular(f.get_telefone())
                })
            
            df = pd.DataFrame(dados).set_index("ID")
            st.dataframe(df, use_container_width=True)

    with tab_alterar:
        st.header("Alterar Fornecedor")
        
        lista_fornecedores = FornecedorController.consultarFornecedores()
        
        if not lista_fornecedores:
            st.info("Nenhum fornecedor disponível para alterar.")
        else:
            map_fornecedores = {f"{f.get_id()} - {f.get_nome()}": f for f in lista_fornecedores}
            
            selecionado_str = st.selectbox("Selecione o Fornecedor:", options=map_fornecedores.keys())
            fornecedor_selecionado = map_fornecedores[selecionado_str]
            
            with st.form(key="alterar_fornecedor"):
                novo_nome = st.text_input("Nome:", value=fornecedor_selecionado.get_nome())
                novo_cnpj = st.text_input("CNPJ:", value=fornecedor_selecionado.get_cnpj())
                novo_telefone = st.text_input("Telefone:", value=fornecedor_selecionado.get_telefone())
                
                alterar_button = st.form_submit_button("Salvar Alterações")
                
                if alterar_button:
                    fornecedor_selecionado.set_nome(novo_nome)
                    fornecedor_selecionado.set_cnpj(novo_cnpj)
                    fornecedor_selecionado.set_telefone(novo_telefone)
                    
                    if FornecedorController.alterarFornecedor(fornecedor_selecionado):
                        st.success("Fornecedor atualizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao atualizar fornecedor.")

    with tab_excluir:
        st.header("Excluir Fornecedor")
        
        lista_fornecedores = FornecedorController.consultarFornecedores()
        
        if not lista_fornecedores:
            st.info("Nenhum fornecedor disponível para excluir.")
        else:
            map_fornecedores = {f"{f.get_id()} - {f.get_nome()}": f.get_id() for f in lista_fornecedores}
            
            selecionado_str = st.selectbox("Selecione para Excluir:", options=map_fornecedores.keys(), key="del_forn")
            id_excluir = map_fornecedores[selecionado_str]
            
            if st.button("Excluir Fornecedor", type="primary"):
                if FornecedorController.excluirFornecedor(id_excluir):
                    st.success("Fornecedor excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao excluir. Verifique se ele possui vínculos.")