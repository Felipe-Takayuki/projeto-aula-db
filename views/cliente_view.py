import streamlit as st
import pandas as pd
import controllers.cliente_controller as ClienteController
from models.pessoa_model import Pessoa

@st.dialog("Confirmação")
def confirmar():
    with st.form(key="incluir_cliente", clear_on_submit=True):

            nome = st.text_input("Nome do Cliente:", placeholder="Ex: Paul")
            cpf = st.text_input("CPF do Cliente", placeholder="Ex: 444.444.444-20")
            telefone = st.text_input("Telefone do Cliente", placeholder="Ex: 14999999999")
            submit_button = st.form_submit_button("Incluir")

            if submit_button:
                if nome:
                    novo_cliente = Pessoa(id=None, nome=nome, cpf=cpf, telefone=telefone)

                    if ClienteController.incluirCliente(novo_cliente):
                            st.success(f"Cliente '{nome}' incluída com sucesso!")
                    else:
                            st.error("Erro ao incluir cliente. (Verifique se ele já existe)")
                else:
                    st.warning("O nome da categoria é obrigatório.")



def show_page():
    
    st.title("Clientes")

    if st.button("Adicionar novo cliente"):
        confirmar()

    if "confirmado" in st.session_state:
        st.write("Resultado:", st.session_state["confirmado"])
    
    lista_clientes = ClienteController.consultarClientes()
        
    if not lista_clientes:
            st.info("Nenhum cliente cadastrado.")
    else:
        df = pd.DataFrame([p.to_dict() for p in lista_clientes])
        st.dataframe(df.set_index("id"), use_container_width=True)
   