import streamlit as st
import pandas as pd
import controllers.cliente_controller as ClienteController
from models.cliente_model import Cliente
import re
# ===============================
# MODAL → CADASTRAR CLIENTE
# ===============================
@st.dialog("Cadastro de cliente")
def modal_cadastrar():
    with st.form(key="form_cadastro", clear_on_submit=True):
        nome = st.text_input("Nome do Cliente:", placeholder="Ex: Paul")
        cpf = st.text_input("CPF do Cliente", placeholder="Ex: 44444444420", max_chars=11)
        telefone = st.text_input("Telefone do Cliente", placeholder="Ex: 14999999999", max_chars=11)
        submit_button = st.form_submit_button("Incluir")

        if submit_button:
            if nome:
                novo_cliente = Cliente(id=None, nome=nome, cpf=cpf, telefone=telefone)

                if ClienteController.incluirCliente(novo_cliente):
                    st.session_state.reload_clientes = True
                    st.success(f"Cliente '{nome}' incluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao incluir cliente. (Verifique se ele já existe)")
            else:
                st.warning("O nome do cliente é obrigatório.")


# ===============================
# MODAL → EDITAR CLIENTE
# ===============================
@st.dialog("Editar Cliente")
def modal_editar(cliente: Cliente):
    with st.form(key="form_editar", clear_on_submit=True):
        cpf_edit = cliente.get_cpf()
        telefone_edit = cliente.get_telefone()
        cpf_edit = re.sub(r"\D", "", cpf_edit)
        telefone_edit = re.sub(r"\D", "", telefone_edit)
        nome = st.text_input("Nome do Cliente:", value=cliente.get_nome())
        cpf = st.text_input("CPF do Cliente", value=cpf_edit, max_chars=11)
        telefone = st.text_input("Telefone do Cliente", value=telefone_edit, max_chars=11)

        submit_button = st.form_submit_button("Salvar alterações")

        if submit_button:
            cliente.set_nome(nome)
            cliente.set_cpf(cpf)
            cliente.set_telefone(telefone)

            if ClienteController.alterarCliente(cliente):
                st.session_state.reload_clientes = True
                st.success("Cliente atualizado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao editar cliente.")


# ===============================
# MODAL → CONFIRMAR EXCLUSÃO
# ===============================
@st.dialog("Excluir Cliente")
def modal_excluir(cliente: Cliente):
    st.warning(f"Tem certeza que deseja excluir o cliente **{cliente.get_nome()}**?")

    if st.button("Sim, excluir", type="primary"):
        if ClienteController.excluirCliente(cliente.get_id()):
            st.session_state.reload_clientes = True
            st.success("Cliente excluído!")
            st.rerun()
        else:
            st.error("Erro ao excluir.")

    st.button("Cancelar")


# ===============================
# PÁGINA PRINCIPAL
# ===============================
def show_page():

    # força recarregar
    if st.session_state.get("reload_clientes"):
        lista_clientes = ClienteController.consultarClientes()
        st.session_state.reload_clientes = False
    else:
        lista_clientes = ClienteController.consultarClientes()

    st.title("Clientes")

    # botão adicionar
    if st.button("Adicionar novo cliente"):
        modal_cadastrar()

    # caso não haja registros
    if not lista_clientes:
        st.info("Nenhum cliente cadastrado.")
        return

    # dataframe
    df = pd.DataFrame([p.to_dict() for p in lista_clientes])

    st.subheader("Lista de Clientes")

def show_page():

    # força recarregar
    if st.session_state.get("reload_clientes"):
        lista_clientes = ClienteController.consultarClientes()
        st.session_state.reload_clientes = False
    else:
        lista_clientes = ClienteController.consultarClientes()

    st.title("Clientes")

    # botão adicionar
    if st.button("Adicionar novo cliente"):
        modal_cadastrar()

    # caso não haja registros
    if not lista_clientes:
        st.info("Nenhum cliente cadastrado.")
        return

    df = pd.DataFrame([p.to_dict() for p in lista_clientes])

    st.subheader("Lista de Clientes")

    # ===============================
    #  ESTILO DE TABELA
    # ===============================

    # Cabeçalho
    header = st.container()
    with header:
        col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 3, 3, 2, 2])
        col1.markdown("**ID**")
        col2.markdown("**Nome**")
        col3.markdown("**CPF**")
        col4.markdown("**Telefone**")


    st.divider()

    # Linhas da tabela
    for _, row in df.iterrows():
        cliente = next((p for p in lista_clientes if p.get_id() == row["id"]), None)

        linha = st.container()
        with linha:
            col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 3, 3, 2, 2])

            col1.write(f"{row['id']}")
            col2.write(row["nome"])
            col3.write(row["cpf"])
            col4.write(row["telefone"])

            if col5.button("Editar", key=f"editar_{row['id']}"):
                modal_editar(cliente)

            if col6.button("Excluir", key=f"del_{row['id']}"):
                modal_excluir(cliente)
            st.divider()



                