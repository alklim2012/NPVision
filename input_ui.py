import streamlit as st
import pandas as pd

def load_inputs():
    st.sidebar.header("Input Parameters")
    cutoff = st.sidebar.slider("Cut-off Grade (%)", 0.1, 1.5, (0.2, 1.0), 0.1)
    prod = st.sidebar.slider("Production (Mtpa)", 1.0, 10.0, (2.0, 6.0), 0.5)
    price = st.sidebar.number_input("Metal Price ($/t)", 1000, 10000, 4000)
    price_std = st.sidebar.number_input("Price Std Dev", 0, 5000, 500)
    rec = st.sidebar.slider("Recovery (%)", 50, 95, 85)
    rec_std = st.sidebar.slider("Recovery Std Dev (%)", 0, 15, 5)
    discount = st.sidebar.slider("Discount Rate (%)", 5.0, 15.0, 8.0)
    opex = st.sidebar.number_input("OPEX ($/t)", 10, 150, 40)
    uploaded_file = st.sidebar.file_uploader("📥 Upload Grade-Tonnage CSV", type=["csv"])

    run = st.sidebar.button("🚀 Start Simulation")
    curve = pd.read_csv(uploaded_file) if uploaded_file else None

    return {
        "cutoff_range": cutoff,
        "prod_range": prod,
        "price": price,
        "price_std": price_std,
        "recovery": rec,
        "recovery_std": rec_std,
        "discount_rate": discount,
        "opex": opex,
        "user_curve": curve,
        "run": run
    }
