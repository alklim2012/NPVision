import streamlit as st
from input_ui import load_inputs
from models import generate_scenarios
from charts import show_table, capex_vs_production, life_vs_cutoff, render_3d_surface

st.set_page_config(page_title="NPVision", layout="wide")
st.title("⛏️ NPVision: Hill of Value Simulator")

params = load_inputs()

if params["run"]:
    df = generate_scenarios(params)
    show_table(df)
    capex_vs_production(df)
    life_vs_cutoff(df)
    render_3d_surface(df)
else:
    st.info("👈 Set parameters and press '🚀 Start Simulation' to see results.")
