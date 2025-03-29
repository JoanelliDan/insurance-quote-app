import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Insurance Quote Platform", layout="wide")

# Custom Styles
st.markdown(
    """
    <style>
    .main {background-color: #F0F8FF;}
    .stButton>button {background-color: #004488; color: white; font-size: 18px; border-radius: 10px;}
    .stTextInput>div>div>input {border-radius: 5px;}
    .stSelectbox>div>div>select {border-radius: 5px;}
    .stNumberInput>div>div>input {border-radius: 5px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Add Logo
st.sidebar.image("https://worldvectorlogo.com/pt/logo/allianz-1", use_column_width=True)

st.title("Cotação (Facility) - RD Equipamentos")

# Sidebar for customer & policy info
with st.sidebar:
    st.header("Informações do Segurado:")
    customer_name = st.text_input("Nome do Segurado")
    customer_id = st.text_input("CPF/CNPJ do Segurado")
    customer_phone = st.text_input("Número de Telefone/Celular do Segurado")
    customer_email = st.text_input("Email do Segurado")
    
    st.header("Informações da Apólice:")
    start_date = st.date_input("Data de Início de Vigência", date.today())
    end_date = st.date_input("Data de Fim de Vigência", date.today())
    previous_policy = st.text_input("Número da Apólice Anterior (em caso de Renovação Interna)")
    
# Equipment Info Section
st.header("Informações dos Equipamentos:")

# Equipment Type & Usage Options for Basic Coverage
basic_equipment_types = {"Trator": 1.2, "Escavadeira": 1.5, "Retroescavadeira": 1.8, "Notebook": 1.1, "Placa Solar": 1.3}
basic_equipment_usages = {"Indústria": 1.1, "Construção": 1.4, "Comércio": 1.2, "Demais": 1.6}

# Equipment Type & Usage Options for Theft Coverage
theft_equipment_types = {"Trator": 1.1, "Escavadeira": 1.6, "Retroescavadeira": 1.3, "Notebook": 1.9, "Placa Solar": 1.9}
theft_equipment_usages = {"Indústria": 0.6, "Construção": 1.7, "Comércio": 1.1, "Demais": 1.4}

# Equipment Type & Usage Options for Electrical Coverage
electrical_equipment_types = {"Trator": 0.8, "Escavadeira": 1.2, "Retroescavadeira": 1.2, "Notebook": 2.1, "Placa Solar": 0.9}
electrical_equipment_usages = {"Indústria": 0.9, "Construção": 0.7, "Comércio": 1.2, "Demais": 1.5}

# Fake coverage factors
coverage_factors = {
    "Basic": 1.0,
    "Theft": 0.5,
    "Electrical": 0.3
}

# Dynamic Equipment Input
num_equipments = st.number_input("Número de Equipamentos", min_value=1, max_value=50, value=1)

# Equipment data storage
equipments = []
total_price = 0.0

for i in range(num_equipments):
    st.subheader(f"Equipamento {i+1}")
    col1, col2 = st.columns(2)
    with col1:
        equipment_type = st.selectbox("Tipo", list(basic_equipment_types.keys()), key=f"type_{i}")
        equipment_usage = st.selectbox("Utilização", list(basic_equipment_usages.keys()), key=f"usage_{i}")
    with col2:
        equipment_year = st.number_input("Ano de Fabricação", min_value=1900, max_value=2050, step=1, key=f"year_{i}")
        equipment_value = st.number_input("Valor do Equipamento", min_value=0.0, step=100.0, key=f"value_{i}")
    equipment_rented = st.radio("Equipamento Alugado?", ("Yes", "No"), key=f"rented_{i}")
    
    # Coverage Inputs
    st.subheader("Coberturas:")
    basic_si = st.number_input("Cobertura Básica", min_value=0.0, max_value=equipment_value, step=100.0, key=f"basic_{i}")
    theft_si = st.number_input("Cobertura Roubo", min_value=0.0, max_value=basic_si, step=100.0, key=f"theft_{i}")
    electrical_si = st.number_input("Cobertura Danos Elétricos", min_value=0.0, max_value=basic_si, step=100.0, key=f"electrical_{i}")
    
    # Equipment Type & Usage Options for Coverages
    basic_type_factor = basic_equipment_types[equipment_type]
    basic_usage_factor = basic_equipment_usages[equipment_usage]
    
    theft_type_factor = theft_equipment_types[equipment_type]
    theft_usage_factor = theft_equipment_usages[equipment_usage]
    
    electrical_type_factor = electrical_equipment_types[equipment_type]
    electrical_usage_factor = electrical_equipment_usages[equipment_usage]
    
    # Calculate Pricing
    age_factor = 1 + (2025 - equipment_year) * 0.01
    rented_factor = 1.2 if equipment_rented == "Yes" else 1.0
    
    basic_price = basic_type_factor * basic_usage_factor * age_factor * rented_factor * basic_si * coverage_factors["Basic"]
    theft_price = theft_type_factor * theft_usage_factor * age_factor * rented_factor * theft_si * coverage_factors["Theft"]
    electrical_price = electrical_type_factor * electrical_usage_factor * age_factor * rented_factor * electrical_si * coverage_factors["Electrical"]
    
    total_equipment_price = basic_price + theft_price + electrical_price
    total_price += total_equipment_price
    
    equipments.append({
        "Tipo": equipment_type,
        "Utilização": equipment_usage,
        "Ano": equipment_year,
        "Valor": equipment_value,
        "Alugado": equipment_rented,
        "Cobertura Básica": basic_si,
        "Cobertura Roubo": theft_si,
        "Cobertura Danos Elétricos": electrical_si,
        "Preço Total": total_equipment_price
    })

if st.button("Realizar Cotação"):
    df = pd.DataFrame(equipments)
    st.write("### Resumo")
    st.write(df)
    st.write(f"## Preço Total: R${total_price:,.2f}")
    st.success("Cotação Gerada com Sucesso!")
