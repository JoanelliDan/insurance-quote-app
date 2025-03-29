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

# Equipment Type & Usage Options for Basic Coverage
basic_equipment_types = {"Tractor": 1.2, "Excavator": 1.5, "Crane": 1.8, "Forklift": 1.1, "Harvester": 1.3}
basic_equipment_usages = {"Agriculture": 1.1, "Construction": 1.4, "Logistics": 1.2, "Mining": 1.6}

# Equipment Type & Usage Options for Theft Coverage
theft_equipment_types = {"Tractor": 1.3, "Excavator": 1.6, "Crane": 1.9, "Forklift": 1.2, "Harvester": 1.4}
theft_equipment_usages = {"Agriculture": 1.2, "Construction": 1.5, "Logistics": 1.3, "Mining": 1.7}

# Equipment Type & Usage Options for Electrical Coverage
electrical_equipment_types = {"Tractor": 1.1, "Excavator": 1.4, "Crane": 1.7, "Forklift": 1.0, "Harvester": 1.2}
electrical_equipment_usages = {"Agriculture": 1.0, "Construction": 1.3, "Logistics": 1.1, "Mining": 1.5}

base_factor = 0.005  # Fake base factor

# Fake coverage factors
coverage_factors = {
    "Basic": 1.0,
    "Theft": 1.2,
    "Electrical": 1.1
}

# Dynamic Equipment Input
num_equipments = st.number_input("Number of Equipments", min_value=1, max_value=50, value=1)

# Equipment data storage
equipments = []
total_price = 0.0

for i in range(num_equipments):
    st.subheader(f"Equipment {i+1}")
    equipment_type = st.selectbox(f"Equipment Type", list(basic_equipment_types.keys()), key=f"type_{i}")
    equipment_usage = st.selectbox(f"Equipment Usage", list(basic_equipment_usages.keys()), key=f"usage_{i}")
    equipment_year = st.number_input(f"Equipment Year", min_value=1900, max_value=2050, step=1, key=f"year_{i}")
    equipment_value = st.number_input(f"Equipment Value", min_value=0.0, step=100.0, key=f"value_{i}")
    equipment_rented = st.radio(f"Is the Equipment Rented?", ("Yes", "No"), key=f"rented_{i}")
    
    # Coverage Inputs
    st.subheader("Coverage (Sum Insured)")
    basic_si = st.number_input(f"Basic Coverage S.I. (FLExA)", min_value=0.0, max_value=equipment_value, step=100.0, key=f"basic_{i}")
    theft_si = st.number_input(f"Theft Coverage S.I.", min_value=0.0, max_value=basic_si, step=100.0, key=f"theft_{i}")
    electrical_si = st.number_input(f"Electrical Damage Coverage S.I. (FLExA)", min_value=0.0, max_value=basic_si, step=100.0, key=f"electrical_{i}")
    
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
    
    basic_price = base_factor * basic_type_factor * basic_usage_factor * age_factor * rented_factor * basic_si * coverage_factors["Basic"]
    theft_price = base_factor * theft_type_factor * theft_usage_factor * age_factor * rented_factor * theft_si * coverage_factors["Theft"]
    electrical_price = base_factor * electrical_type_factor * electrical_usage_factor * age_factor * rented_factor * electrical_si * coverage_factors["Electrical"]
    
    total_equipment_price = basic_price + theft_price + electrical_price
    total_price += total_equipment_price
    
    equipments.append({
        "Type": equipment_type,
        "Usage": equipment_usage,
        "Year": equipment_year,
        "Value": equipment_value,
        "Rented": equipment_rented,
        "Basic SI": basic_si,
        "Theft SI": theft_si,
        "Electrical SI": electrical_si,
        "Total Price": total_equipment_price
    })

# Submit Button
if st.button("Generate Quote"):
    df = pd.DataFrame(equipments)
    st.write("### Quote Summary")
    st.write(df)
    st.write(f"## Total Insurance Quote Price: ${total_price:,.2f}")
    st.success("Quote generated successfully!")
