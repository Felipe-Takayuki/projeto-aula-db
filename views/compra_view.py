import streamlit as st
import pandas as pd
import controllers.compra_controller as CompraController
import controllers.cliente_controller as ClienteController
import controllers.funcionario_controller as FuncionarioController
import controllers.produto_controller as ProdutoController
from models.compra_model import Compra

def show_page():
    st.title("Gestão de Compras")
    
    tab_nova, tab_historico, tab_cancelar = st.tabs(["Nova Compra", "Histórico", "Cancelar"])
    
    with tab_nova:
        st.header("Registrar Compra")

        try:
            clientes = ClienteController.consultarClientes() 
            funcionarios = FuncionarioController.consultarFuncionarios()
            produtos = ProdutoController.consultarProdutos()
            
            if not clientes or not funcionarios or not produtos:
                st.warning("Cadastre Clientes, Funcionários e Produtos antes de vender.")
            else:

                map_cli = {f"{c.get_nome()} (ID: {c.get_id()})": c.get_id() for c in clientes}
                map_func = {f"{f.get_nome()} (ID: {f.get_id()})": f.get_id() for f in funcionarios}
                map_prod = {f"{p['Nome']} (R$ {p['Preço (R$)']})": p['ID'] for p in produtos}

                with st.form(key="form_compra"):
                    col1, col2 = st.columns(2)
                    with col1:
                        cli_selecionado = st.selectbox("Cliente:", list(map_cli.keys()))
                    with col2:
                        func_selecionado = st.selectbox("Funcionário:", list(map_func.keys()))
                    
                    prod_selecionado = st.selectbox("Produto:", list(map_prod.keys()))
                    qtd = st.number_input("Quantidade:", min_value=1, step=1)
                    
                    btn_comprar = st.form_submit_button("Finalizar Compra")
                    
                    if btn_comprar:

                        id_cliente = map_cli[cli_selecionado]
                        id_funcionario = map_func[func_selecionado]
                        id_produto = map_prod[prod_selecionado]
                        nova_compra = Compra(0, id_cliente, id_funcionario, id_produto, qtd, 0)
                        
                        if CompraController.incluirCompra(nova_compra):
                            st.success("Compra realizada com sucesso!")
                        else:
                            st.error("Erro ao registrar. Verifique o estoque!")
                            
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")

    with tab_historico:
        st.header("Histórico de Compras")
        dados = CompraController.consultarCompras()
        
        if dados:
            df = pd.DataFrame(dados)
            df["Total (R$)"] = df["Total (R$)"].map("R$ {:,.2f}".format)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhuma compra registrada.")
    with tab_cancelar:
        st.header("Cancelar/Estornar Compra")
        dados = CompraController.consultarCompras()
        
        if dados:
            map_cancel = {f"#{d['ID']} - {d['Produto']} ({d['Data']})": d['ID'] for d in dados}
            
            selecao = st.selectbox("Selecione a compra:", list(map_cancel.keys()))
            
            if st.button("Cancelar Compra Selecionada", type="primary"):
                id_para_excluir = map_cancel[selecao]
                
                if CompraController.excluirCompra(id_para_excluir):
                    st.success("Compra cancelada e produto devolvido ao estoque.")
                    st.rerun()
                else:
                    st.error("Erro ao cancelar.")
        else:
            st.info("Nada para cancelar.")