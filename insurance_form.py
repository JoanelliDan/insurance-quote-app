import streamlit as st
import pandas as pd
from datetime import date

# Load broker data
brokers_df = pd.read_csv("brokers.csv", sep=";")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.broker_name = ""
    st.session_state.max_commission = 0.0
    st.session_state.max_discount = 0.0
    st.session_state.min_equipment_year = 2000

# Show login form if not logged in
if not st.session_state.logged_in:
    st.title("Login do Corretor")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_button = st.button("Login")

    if login_button:
        user_row = brokers_df[(brokers_df["username"] == username) & (brokers_df["password"] == password)]
        if not user_row.empty:
            user_data = user_row.iloc[0]
            st.session_state.logged_in = True
            st.session_state.broker_name = user_data["broker_name"]
            st.session_state.max_commission = user_data["max_commission"]
            st.session_state.max_discount = user_data["max_discount"]
            st.session_state.min_equipment_year = user_data["min_equipment_year"]
        else:
            st.error("Usuário ou senha inválidos.")

# Show main app if logged in
if st.session_state.logged_in:
    st.success(f"Bem-vindo, {st.session_state.broker_name}!")
    # 👉 Here you include the rest of your form/app logic

