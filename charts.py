import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def show_table(df):
    st.subheader("📊 Scenario Table")
    st.dataframe(df.round(2), use_container_width=True)

def capex_vs_production(df):
    st.subheader("📈 CAPEX vs Production")
    fig = px.scatter(df, x="Production", y="CAPEX", color="Cutoff", size=df["Avg NPV"].abs())
    st.plotly_chart(fig, use_container_width=True)

def life_vs_cutoff(df):
    st.subheader("📉 Life vs Cut-off")
    fig = px.scatter(df, x="Cutoff", y="Avg Life", color="Production", size=df["Avg NPV"].abs())
    st.plotly_chart(fig, use_container_width=True)

def render_3d_surface(df):
    st.subheader("🗻 3D Hill of Value")
    try:
        pivot = df.pivot(index='Cutoff', columns='Production', values='Avg NPV')
        fig = go.Figure(data=[go.Surface(z=pivot.values, x=pivot.columns, y=pivot.index)])
        fig.update_layout(scene=dict(
            xaxis_title='Production (Mtpa)',
            yaxis_title='Cut-off (%)',
            zaxis_title='Avg NPV ($M)'
        ), height=700)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error rendering 3D plot: {e}")
