iimport streamlit as st
import pandas as pd
from datetime import date

# Load broker data from CSV
brokers_df = pd.read_csv("brokers.csv")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.broker_data = {}

# Login section
if not st.session_state.authenticated:
    st.title("Login do Corretor")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Entrar")

    if login_button:
        user_row = brokers_df[(brokers_df["username"] == username) & (brokers_df["password"] == password)]
        if not user_row.empty:
            st.success("Login realizado com sucesso!")
            st.session_state.authenticated = True
            st.session_state.broker_data = user_row.iloc[0].to_dict()
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# If authenticated, show the app content
if st.session_state.authenticated:
    st.sidebar.title("Informações do Corretor")
    broker = st.session_state.broker_data
    st.sidebar.markdown(f"**Corretor:** {broker['broker_name']}")
    st.sidebar.markdown(f"**Máx Comissão:** {broker['max_commission']}")
    st.sidebar.markdown(f"**Máx Desconto:** {broker['max_discount']}")
    st.sidebar.markdown(f"**Ano Mín Equipamento:** {broker['min_equipment_year']}")

    st.title("Formulário de Cotação de Seguro")

    # Example of form usage with login constraints
    for i in range(1):  # Use your actual loop or logic here
        min_year = int(broker['min_equipment_year'])
        equipment_year = st.number_input(
            "Ano de Fabricação", 
            min_value=min_year, 
            max_value=date.today().year, 
            value=date.today().year, 
            step=1, 
            key=f"year_{i}"
        )

