import streamlit as st
import pandas as pd
import controllers.funcionario_controller as FuncionarioController
from models.funcionario_model import Funcionario
import re

def format_cpf(cpf: str) -> str:
    cpf = re.sub(r"\D", "", cpf)
    if len(cpf) >= 3:
        cpf = cpf[:3] + "." + cpf[3:]
    if len(cpf) >= 7:
        cpf = cpf[:7] + "." + cpf[7:]
    if len(cpf) >= 11:
        cpf = cpf[:11] + "-" + cpf[11:]
    return cpf[:14]


@st.dialog("Cadastro de funcionário")
def modal_cadastrar():
    with st.form(key="form_cadastro", clear_on_submit=True):
        nome = st.text_input("Nome do Funcionário:", placeholder="Ex: Paul")

        cpf_raw = st.text_input(
            "CPF do Funcionário",
            placeholder="Ex: 444.444.444-20",
            key="cpf_raw"
        )

        telefone = st.text_input("Telefone do Funcionário", placeholder="Ex: 14999999999")
        salario = st.number_input("Salário (R$):", min_value=0.0, format="%.2f")

        submit_button = st.form_submit_button("Incluir")

        if submit_button:
            if nome:
                cpf_formatado = format_cpf(cpf_raw)

                novo_funcionario = Funcionario(
                    id=None,
                    nome=nome,
                    cpf=cpf_formatado,
                    telefone=telefone,
                    salario=salario
                )

                if FuncionarioController.incluirFuncionario(novo_funcionario):
                    st.session_state.reload_funcionario = True
                    st.success(f"Funcionário '{nome}' incluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao incluir funcionário. (Verifique se ele já existe)")
            else:
                st.warning("O nome do funcionário é obrigatório.")


# ===============================
# MODAL → EDITAR CLIENTE
# ===============================
@st.dialog("Editar Funcionário")
def modal_editar(funcionario: Funcionario):
    with st.form(key="form_editar", clear_on_submit=True):
        nome = st.text_input("Nome do Funcionário:", value=funcionario.get_nome())
        cpf = st.text_input("CPF do Funcionário", value=funcionario.get_cpf())
        telefone = st.text_input("Telefone do Funcionário", value=funcionario.get_telefone())
        salario = st.number_input("Salário (R$):", min_value=0.0, format="%.2f", value=funcionario.get_salario())

        submit_button = st.form_submit_button("Salvar alterações")

        if submit_button:
            funcionario.set_nome(nome)
            funcionario.set_cpf(cpf)
            funcionario.set_telefone(telefone)
            funcionario.set_salario(salario) 
            if FuncionarioController.alterarFuncionario(funcionario):
                st.session_state.reload_funcionario = True
                st.success("Funcionário atualizado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao editar cliente.")


# ===============================
# MODAL → CONFIRMAR EXCLUSÃO
# ===============================
@st.dialog("Excluir Funcionário")
def modal_excluir(funcionario: Funcionario):
    st.warning(f"Tem certeza que deseja excluir o funcionario **{funcionario.get_nome()}**?")

    if st.button("Sim, excluir", type="primary"):
        if FuncionarioController.excluirFuncionario(funcionario.get_id()):
            st.session_state.reload_funcionario = True
            st.success("Funcionário excluído!")
            st.rerun()
        else:
            st.error("Erro ao excluir.")

    st.button("Cancelar")


# ===============================
# PÁGINA PRINCIPAL
# ===============================
def show_page():

    # força recarregar
    if st.session_state.get("reload_funcionario"):
        lista_funcionarios = FuncionarioController.consultarFuncionarios()
        st.session_state.reload_funcionario = False
    else:
        lista_funcionarios = FuncionarioController.consultarFuncionarios()

    st.title("Funcionários")

    # botão adicionar
    if st.button("Adicionar novo funcionario"):
        modal_cadastrar()

    # caso não haja registros
    if not lista_funcionarios:
        st.info("Nenhum funcionário cadastrado.")
        return

    # dataframe
    df = pd.DataFrame([p.to_dict() for p in lista_funcionarios])

    st.subheader("Lista de Funcionários")

def show_page():

    # força recarregar
    if st.session_state.get("reload_funcionario"):
        lista_funcionarios = FuncionarioController.consultarFuncionarios()
        st.session_state.reload_funcionario = False
    else:
        lista_funcionarios = FuncionarioController.consultarFuncionarios()

    st.title("Funcionários")

    # botão adicionar
    if st.button("Adicionar novo cliente"):
        modal_cadastrar()

    # caso não haja registros
    if not lista_funcionarios:
        st.info("Nenhum cliente cadastrado.")
        return

    df = pd.DataFrame([p.to_dict() for p in lista_funcionarios])

    st.subheader("Lista de Funcionários")

    # ===============================
    #  ESTILO DE TABELA
    # ===============================

    # Cabeçalho
    header = st.container()
    with header:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 3, 3, 3, 2, 2])
        col1.markdown("**ID**")
        col2.markdown("**Nome**")
        col3.markdown("**CPF**")
        col4.markdown("**Telefone**")
        col5.markdown("**Salário**")


    st.divider()

    for _, row in df.iterrows():
        funcionario = next((p for p in lista_funcionarios if p.get_id() == row["id"]), None)

        linha = st.container()
        with linha:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 3, 3, 3, 2, 2])

            col1.write(f"{row['id']}")
            col2.write(row["nome"])
            col3.write(row["cpf"])
            col4.write(row["telefone"])
            col5.write(f'R$ {row["salario"]}')

            if col6.button("Editar", key=f"editar_{row['id']}"):
                modal_editar(funcionario)

            if col7.button("Excluir", key=f"del_{row['id']}"):
                modal_excluir(funcionario)
            st.divider()



                