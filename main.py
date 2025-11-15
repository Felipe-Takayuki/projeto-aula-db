import streamlit as st
import sys
from pathlib import Path
import importlib
from services.database import initDB
st.set_page_config(page_title="Mercadinho do Paul", layout="wide")

sys.path.append(str(Path(__file__).parent))

PAGES = {
    "Home": "views.home_view",          
    "Categorias": "views.categoria_view",
    "Produtos": "views.produto_view",
    "Cliente": "views.cliente_view",
    "Funcionário": "views.funcionario_view"
}

def load_page(page_name):
    try:
        module_path = PAGES[page_name] 
        module = importlib.import_module(module_path)
    
        return getattr(module, "show_page")
        
    except (ImportError, AttributeError, KeyError) as e:
        st.error(f"Erro ao carregar a página '{page_name}': {e}")
        st.warning("Verifique o nome do arquivo em /views e se a função 'show_page' existe nele.")
        return None

def main():
    if "db_initialized" not in st.session_state:
        initDB()
        st.session_state["db_initialized"] = True
    with st.sidebar:
        st.logo("assets/images/logo/logo.png", size='large')
        st.title("Menu Principal")
        
        page_selection = st.selectbox(
            "Selecione uma opção", 
            list(PAGES.keys()) 
        )
    
    show_page_function = load_page(page_selection)
    
    if show_page_function:
        show_page_function()

if __name__ == "__main__":
    main()