import streamlit as st
import pandas as pd
import controllers.produto_controller as ProdutoController
import controllers.categoria_controller as CategoriaController
import controllers.fornecedor_controller as FornecedorController
from models.produto_model import Produto
from models.categoria_model import Categoria
from models.fornecedor_model import Fornecedor


# ===========================
#   MODAL: CATEGORIA
# ===========================
@st.dialog("Cadastro de categoria")
def modal_categoria():
    with st.form(key="form_cadastro", clear_on_submit=True):
        categoria = st.text_input("Nome da Categoria:", placeholder="Ex: Frios")
        submit_button = st.form_submit_button("Incluir")

        if submit_button:
            if categoria:
                novo_cliente = Categoria(id=None, nome=categoria)

                if CategoriaController.incluirCategoria(novo_cliente):
                    st.success(f"Categoria '{categoria}' incluída com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao incluir categoria.")
            else:
                st.warning("O nome da categoria é obrigatório.")


# ===========================
#   MODAL: FORNECEDOR
# ===========================
@st.dialog("Cadastro de fornecedor")
def modal_fornecedor():
    with st.form(key="form_cadastro_fornecedor", clear_on_submit=True):
        fornecedor = st.text_input("Nome do Fornecedor:", placeholder="Ex: Shida Arroz Glutinoso")
        cnpj = st.text_input("CNPJ: ", placeholder="Ex: 11122233344455", max_chars=14)
        telefone = st.text_input("Telefone do Funcionário", placeholder="Ex: 14999999999", max_chars=11)
        submit_button = st.form_submit_button("Incluir")

        if submit_button:
            if fornecedor:
                novo_fornecedor = Fornecedor(id=None, nome=fornecedor, cnpj=cnpj, telefone=telefone)

                if FornecedorController.incluirFornecedor(novo_fornecedor):
                    st.success(f"Fornecedor '{fornecedor}' incluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao incluir fornecedor.")
            else:
                st.warning("O nome do fornecedor é obrigatório.")


# =====================================================
#                     MAIN PAGE
# =====================================================
def show_page():

    st.title("Cadastro de Produtos")

    tab_incluir, tab_consultar, tab_alterar, tab_excluir = st.tabs(
        ["Incluir", "Consultar", "Alterar", "Excluir"]
    )

    # =====================================================
    #                    INCLUIR PRODUTO
    # =====================================================
    with tab_incluir:
        st.header("Incluir Novo Produto")

        lista_categorias = CategoriaController.consultarCategorias()
        lista_fornecedores = FornecedorController.consultarFornecedores()

        if not lista_categorias:
            st.warning("É necessário cadastrar pelo menos uma Categoria antes de incluir um Produto.")
            if st.button("Adicionar nova categoria"):
                modal_categoria()

        elif not lista_fornecedores:
            st.warning("É necessário cadastrar pelo menos um Fornecedor antes de incluir um Produto.")
            if st.button("Adicionar novo fornecedor"):
                modal_fornecedor()

        else:
            map_cat = {cat.get_nome(): cat.get_id() for cat in lista_categorias}
            map_fornecedor = {forn.get_nome(): forn.get_id() for forn in lista_fornecedores}

            with st.form(key="incluir_produto", clear_on_submit=True):

                nome = st.text_input("Nome do Produto:", placeholder="Ex: Leite Integral")
                descricao = st.text_input("Descrição:", placeholder="Ex: Caixa 1L")

                col1, col2 = st.columns(2)
                with col1:
                    quantidade = st.number_input("Quantidade em Estoque:", min_value=0, step=1)
                with col2:
                    preco = st.number_input("Preço Unitário (R$):", min_value=0.0, format="%.2f")

                cat_nome_selecionado = st.selectbox("Selecione a Categoria:", options=map_cat.keys())
                cat_fornecedor_selecionado = st.selectbox("Selecione o Fornecedor:", options=map_fornecedor.keys())

                submit_button = st.form_submit_button("Incluir Produto")

                if submit_button:
                    novo_produto = Produto(
                        id=None,
                        nome=nome,
                        descricao=descricao,
                        quantidade=quantidade,
                        preco=preco,
                        id_categoria=map_cat[cat_nome_selecionado],
                        id_fornecedor=map_fornecedor[cat_fornecedor_selecionado]
                    )

                    if ProdutoController.incluirProduto(novo_produto):
                        st.success(f"Produto '{nome}' incluído com sucesso!")
                    else:
                        st.error("Erro ao incluir produto.")

    # =====================================================
    #                   CONSULTAR PRODUTOS
    # =====================================================
    with tab_consultar:
        st.header("Consultar Produtos")

        lista_produtos = ProdutoController.consultarProdutos()

        if not lista_produtos:
            st.info("Nenhum produto cadastrado.")
        else:
            df = pd.DataFrame(lista_produtos)

            df_display = df.copy()
            df_display["Preço (R$)"] = df_display["Preço (R$)"].map(lambda p: f"R$ {p:,.2f}")

            st.dataframe(df_display.set_index("ID"), use_container_width=True)

    # =====================================================
    #                   ALTERAR PRODUTO
    # =====================================================
    with tab_alterar:
        st.header("Alterar Produto")

        lista_produtos = ProdutoController.consultarProdutos()
        lista_fornecedores = FornecedorController.consultarFornecedores()

        if not lista_produtos:
            st.info("Nenhum produto cadastrado para alterar.")
        elif not lista_fornecedores:
            st.warning("É necessário cadastrar pelo menos um Fornecedor antes de incluir um Produto.")
            if st.button("Adicionar novo fornecedor"):
                modal_fornecedor()
        else:
            map_prod = {f"{prod['ID']} - {prod['Nome']}": prod for prod in lista_produtos}
            map_fornecedor = {forn.get_nome(): forn.get_id() for forn in lista_fornecedores}

            prod_key = st.selectbox("Selecione o Produto:", options=map_prod.keys())
            prod_data = map_prod[prod_key]

            preco_float = float(prod_data["Preço (R$)"])  

            with st.form(key="alterar_produto"):

                nome = st.text_input("Nome do Produto:", value=prod_data["Nome"])
                descricao = st.text_input("Descrição:", value=prod_data["Descrição"])

                col1, col2 = st.columns(2)
                with col1:
                    quantidade = st.number_input(
                        "Quantidade:",
                        min_value=0,
                        step=1,
                        value=prod_data["Quantidade"]
                    )
                with col2:
                    preco = st.number_input(
                        "Preço Unitário (R$):",
                        min_value=0.0,
                        format="%.2f",
                        value=preco_float
                    )

                # ----- Categorias -----
                lista_categorias = CategoriaController.consultarCategorias()
                map_cat = {cat.get_nome(): cat.get_id() for cat in lista_categorias}
                nomes_categorias = list(map_cat.keys())

                try:
                    index_cat = nomes_categorias.index(prod_data["Categoria"])
                except ValueError:
                    index_cat = 0

                cat_nome_selecionado = st.selectbox(
                    "Categoria:",
                    options=nomes_categorias,
                    index=index_cat
                )

                # ----- Fornecedores (NOVO) -----
                nomes_fornecedores = list(map_fornecedor.keys())

                try:
                    forn_atual = next(
                        nome for nome, id_f in map_fornecedor.items()
                        if id_f == prod_data["ID_Fornecedor"]
                    )
                    index_forn = nomes_fornecedores.index(forn_atual)
                except Exception:
                    index_forn = 0

                fornecedor_nome_selecionado = st.selectbox(
                    "Fornecedor:",
                    options=nomes_fornecedores,
                    index=index_forn
                )

                alterar_button = st.form_submit_button("Salvar Alterações")

                if alterar_button:

                    produto_alterado = Produto(
                        id=prod_data["ID"],
                        nome=nome,
                        descricao=descricao,
                        quantidade=quantidade,
                        preco=preco,
                        id_categoria=map_cat[cat_nome_selecionado],
                        id_fornecedor=map_fornecedor[fornecedor_nome_selecionado]  # atualizado!
                    )

                    if ProdutoController.alterarProduto(produto_alterado):
                        st.success("Produto alterado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao alterar produto.")
    # =====================================================
    #                   EXCLUIR PRODUTO
    # =====================================================
    with tab_excluir:
        st.header("Excluir Produto")

        lista_produtos = ProdutoController.consultarProdutos()

        if not lista_produtos:
            st.info("Nenhum produto cadastrado para excluir.")
        else:
            map_prod = {f"{prod['ID']} - {prod['Nome']}": prod["ID"] for prod in lista_produtos}

            prod_key = st.selectbox(
                "Selecione o Produto para Excluir:",
                options=map_prod.keys(),
                key="select_excluir_prod"
            )

            id_para_excluir = map_prod[prod_key]

            if st.button("Excluir Produto Selecionado", type="primary"):
                if ProdutoController.excluirProduto(id_para_excluir):
                    st.success("Produto excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao excluir produto. (Verifique se ele está em uso em uma Venda)")
