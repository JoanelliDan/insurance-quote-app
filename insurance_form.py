import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Insurance Quote Platform", layout="wide")

# Initialize/reset form state
if "clear_form" not in st.session_state:
    st.session_state.clear_form = False
if "test_data" not in st.session_state:
    st.session_state.test_data = False

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

# Sidebar
with st.sidebar:
    st.image("https://cdn.iconscout.com/icon/free/png-512/free-allianz-logo-icon-download-in-svg-png-gif-file-formats--company-brand-world-logos-vol-6-pack-icons-282695.png?f=webp&w=256", use_container_width=True)
    st.header("Ajustes:")
    commission = st.slider("Comissão (%)", min_value=5, max_value=25, value=15)
    discount = st.slider("Desconto (%)", min_value=0, max_value=15, value=0)
    surcharge = st.slider("Agravo (%)", min_value=0, max_value=100, value=0)

# Main Title & Logo
st.image("https://cdn.iconscout.com/icon/free/png-512/free-allianz-logo-icon-download-in-svg-png-gif-file-formats--company-brand-world-logos-vol-6-pack-icons-282695.png?f=webp&w=256", use_column_width=False)
st.title("Cotação (Facility) - RD Equipamentos")

# Clear/Test Buttons
col_a, col_b = st.columns(2)
with col_a:
    if st.button("🧹 Limpar Campos"):
        st.session_state.clear_form = True
        st.experimental_rerun()
with col_b:
    if st.button("🧪 Preencher com Dados de Teste"):
        st.session_state.test_data = True
        st.experimental_rerun()

# Test data values
test_values = {
    "name": "João Silva",
    "id": "123.456.789-00",
    "phone": "(11) 91234-5678",
    "email": "joao@teste.com",
    "start_date": date(2025, 5, 1),
    "end_date": date(2026, 5, 1),
    "previous_policy": "ABC1234567",
}

# Clear/test logic
def get_value(field):
    if st.session_state.clear_form:
        return "" if isinstance(test_values[field], str) else date.today()
    elif st.session_state.test_data:
        return test_values[field]
    return "" if isinstance(test_values[field], str) else date.today()

# Customer and Policy Information
st.header("Informações do Segurado:")
col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input("Nome do Segurado")
    customer_id = st.text_input("CPF/CNPJ do Segurado")
with col2:
    customer_phone = st.text_input("Número de Telefone/Celular do Segurado")
    customer_email = st.text_input("Email do Segurado")

st.header("Informações da Apólice:")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Data de Início de Vigência", date.today())
with col2:
    end_date = st.date_input("Data de Fim de Vigência", date.today())

previous_policy = st.text_input("Número da Apólice Anterior (em caso de Renovação Interna)")

if end_date <= start_date:
    st.error("A data de fim deve ser posterior à data de início.")

# Equipment Information
st.header("Informações dos Equipamentos:")

# Equipment Type & Usage Options for Basic Coverage
basic_equipment_types = {"Trator": 1.2, "Escavadeira": 1.5, "Retroescavadeira": 1.8, "Notebook": 1.1, "Placa Solar": 1.3}
basic_equipment_usages = {"Indústria": 1.1, "Construção": 1.4, "Comércio": 1.2, "Demais": 1.6}

theft_equipment_types = {"Trator": 1.1, "Escavadeira": 1.6, "Retroescavadeira": 1.3, "Notebook": 1.9, "Placa Solar": 1.9}
theft_equipment_usages = {"Indústria": 0.6, "Construção": 1.7, "Comércio": 1.1, "Demais": 1.4}

electrical_equipment_types = {"Trator": 0.8, "Escavadeira": 1.2, "Retroescavadeira": 1.2, "Notebook": 2.1, "Placa Solar": 0.9}
electrical_equipment_usages = {"Indústria": 0.9, "Construção": 0.7, "Comércio": 1.2, "Demais": 1.5}

coverage_factors = {
    "Basic": 1.0,
    "Theft": 0.5,
    "Electrical": 0.3
}

num_equipments = st.number_input("Número de Equipamentos", min_value=1, max_value=50, value=1)
equipments = []
total_price = 0.0

for i in range(num_equipments):
    st.subheader(f"Equipamento {i+1}")
    col1, col2 = st.columns(2)
    with col1:
        equipment_type = st.selectbox("Tipo", list(basic_equipment_types.keys()), key=f"type_{i}")
        equipment_usage = st.selectbox("Utilização", list(basic_equipment_usages.keys()), key=f"usage_{i}")
    with col2:
        equipment_year = st.number_input("Ano de Fabricação", min_value=2000, max_value=2050, step=1, key=f"year_{i}")
        equipment_value = st.number_input("Valor do Equipamento", min_value=0.0, step=100.0, key=f"value_{i}")
    
    equipment_rented = st.radio("Equipamento Alugado?", ("Yes", "No"), key=f"rented_{i}")
    
    st.subheader("Coberturas:")
    basic_si = st.number_input("Cobertura Básica", min_value=0.0, max_value=equipment_value, step=100.0, key=f"basic_{i}")
    theft_si = st.number_input("Cobertura Roubo", min_value=0.0, max_value=basic_si, step=100.0, key=f"theft_{i}")
    electrical_si = st.number_input("Cobertura Danos Elétricos", min_value=0.0, max_value=basic_si, step=100.0, key=f"electrical_{i}")
    
    # Calculate pricing
    age_factor = 1 + (2025 - equipment_year) * 0.01
    rented_factor = 1.2 if equipment_rented == "Yes" else 1.0

    basic_price = basic_equipment_types[equipment_type] * basic_equipment_usages[equipment_usage] * age_factor * rented_factor * basic_si * coverage_factors["Basic"]
    theft_price = theft_equipment_types[equipment_type] * theft_equipment_usages[equipment_usage] * age_factor * rented_factor * theft_si * coverage_factors["Theft"]
    electrical_price = electrical_equipment_types[equipment_type] * electrical_equipment_usages[equipment_usage] * age_factor * rented_factor * electrical_si * coverage_factors["Electrical"]
    
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

# Final Quotation Button
if st.button("Realizar Cotação"):
    if not customer_name or not customer_id or not customer_phone or not customer_email:
        st.error("Todos os campos do segurado devem ser preenchidos.")
    elif total_price <= 0:
        st.error("O preço total deve ser maior que zero.")
    else:
        adjusted_price = total_price * (1 + surcharge / 100) * (1 - discount / 100)
        final_price = adjusted_price * (1 - commission / 100)
        
        df = pd.DataFrame(equipments)
        st.write("### Resumo da Cotação")
        st.dataframe(df)
        st.metric("Preço Base Total", f"R${total_price:,.2f}")
        st.metric("Preço Ajustado (com desconto/agravo)", f"R${adjusted_price:,.2f}")
        st.metric("Preço Final (com comissão)", f"R${final_price:,.2f}")
        st.success("Cotação Gerada com Sucesso!")
