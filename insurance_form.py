import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Insurance Quote Platform", layout="wide")

st.title("Insurance Quote Platform")

# Sidebar for customer & policy info
with st.sidebar:
    st.header("Customer Information")
    customer_name = st.text_input("Customer Name")
    customer_id = st.text_input("Customer ID (CPF/CNPJ)")
    customer_phone = st.text_input("Cell Number")
    customer_email = st.text_input("Email")
    
    st.header("Policy Information")
    start_date = st.date_input("Start Date of Insurance", date.today())
    end_date = st.date_input("End Date of Insurance", date.today())
    previous_policy = st.text_input("Previous Policy Number (if renewal)")
    
# Equipment Info Section
st.header("Equipment Information")

# Equipment Type & Usage Options
equipment_types = ["Tractor", "Excavator", "Crane", "Forklift", "Harvester"]
equipment_usages = ["Agriculture", "Construction", "Logistics", "Mining"]

# Dynamic Equipment Input
num_equipments = st.number_input("Number of Equipments", min_value=1, max_value=50, value=1)

# Equipment data storage
equipments = []

for i in range(num_equipments):
    st.subheader(f"Equipment {i+1}")
    equipment_type = st.selectbox(f"Equipment Type", equipment_types, key=f"type_{i}")
    equipment_usage = st.selectbox(f"Equipment Usage", equipment_usages, key=f"usage_{i}")
    equipment_year = st.number_input(f"Equipment Year", min_value=1900, max_value=2050, step=1, key=f"year_{i}")
    equipment_value = st.number_input(f"Equipment Value", min_value=0.0, step=100.0, key=f"value_{i}")
    equipment_rented = st.radio(f"Is the Equipment Rented?", ("Yes", "No"), key=f"rented_{i}")
    
    # Coverage Inputs
    st.subheader("Coverage (Sum Insured)")
    basic_si = st.number_input(f"Basic Coverage S.I. (FLExA)", min_value=0.0, max_value=equipment_value, step=100.0, key=f"basic_{i}")
    theft_si = st.number_input(f"Theft Coverage S.I.", min_value=0.0, max_value=basic_si, step=100.0, key=f"theft_{i}")
    electrical_si = st.number_input(f"Electrical Damage Coverage S.I. (FLExA)", min_value=0.0, max_value=basic_si, step=100.0, key=f"electrical_{i}")
    
    equipments.append({
        "Type": equipment_type,
        "Usage": equipment_usage,
        "Year": equipment_year,
        "Value": equipment_value,
        "Rented": equipment_rented,
        "Basic SI": basic_si,
        "Theft SI": theft_si,
        "Electrical SI": electrical_si
    })

# Submit Button
if st.button("Generate Quote"):
    df = pd.DataFrame(equipments)
    st.write("### Quote Summary")
    st.write(df)
    # Here, we'd call the backend API for pricing
    st.success("Quote generated successfully!")
