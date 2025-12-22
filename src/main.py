import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title="Smart Grid Fault Dashboard", layout="wide")
def load_etap_data():
    # Replace with your actual ETAP export path: pd.read_csv('data/your_file.csv')
    data = {
        'Bus_ID': ['Bus-1', 'Bus-2', 'Bus-3', 'Bus-4', 'Bus-5'],
        'Fault_Type': ['LLL', 'LG', 'LL', 'LLG', 'LLL'],
        'Fault_Current_kA': [25.4, 8.2, 12.5, 15.1, 32.8],
        'Fault_Power_MVA': [450, 120, 210, 240, 580],
        'Voltage_Dip_pu': [0.2, 0.85, 0.6, 0.55, 0.1], # 1.0 is healthy
        'Severity': ['Critical', 'Low', 'Medium', 'Medium', 'Critical']
    }
    return pd.DataFrame(data)
df = load_etap_data()
st.title(" Smart Grid Fault Detection & Rectification")
st.markdown("---")
st.sidebar.header("Real-time Alerts")
for _, row in df.iterrows():
    if row['Severity'] == 'Critical':
        st.sidebar.error(f"**Critical Fault at {row['Bus_ID']}**\n\nType: {row['Fault_Type']} | Current: {row['Fault_Current_kA']} kA")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Highest Fault Current", f"{df['Fault_Current_kA'].max()} kA")
col2.metric("Max Fault Power", f"{df['Fault_Power_MVA'].max()} MVA")
col3.metric("Critical Buses", len(df[df['Severity'] == 'Critical']))
col4.metric("Avg Voltage Dip", f"{df['Voltage_Dip_pu'].mean()} pu")
st.markdown("### Grid Analysis Visuals")
c1, c2 = st.columns(2)
with c1:
    fig_v = px.bar(df, x='Bus_ID', y='Voltage_Dip_pu', color='Severity',
                   title="Voltage Profile during Fault (pu)", color_discrete_map={'Critical':'red', 'Medium':'orange', 'Low':'green'})
    st.plotly_chart(fig_v, use_container_width=True)
with c2:
    fig_i = px.line(df, x='Bus_ID', y='Fault_Current_kA', markers=True, title="Fault Current Distribution (kA)")
    st.plotly_chart(fig_i, use_container_width=True)
st.markdown("---")
st.subheader("🛠️ Rectification & Protection Actions")
selected_bus = st.selectbox("Select a Bus to view Rectification Plan", df['Bus_ID'])
bus_info = df[df['Bus_ID'] == selected_bus].iloc[0]
f_type = bus_info['Fault_Type']
recs = {
    'LLL': ["Immediate Isolation via Circuit Breaker", "Check for busbar short-circuits", "Verify Relay Coordination (ANSI 50/51)"],
    'LG': ["Check Neutral Grounding Resistor (NGR)", "Inspect insulator health", "Verify Ground Fault Relay (ANSI 51N)"],
    'LL': ["Verify phase-to-phase clearances", "Adjust Time-Overcurrent settings"],
    'LLG': ["Check surge arresters", "Perform load shedding to stabilize voltage"]
}
r1, r2 = st.columns(2)
with r1:
    st.info(f"**Fault Type:** {f_type}")
    for item in recs.get(f_type, ["General Inspection Required"]):
        st.write(f" {item}")
with r2:
    st.success("### Reliability Impact\nImplementing these actions restores **System Stability** by preventing cascading failures and improves **SAIDI/SAIFI** indices.")
