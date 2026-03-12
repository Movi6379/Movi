import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title="Smart Grid Fault Dashboard", layout="wide")
def get_mock_data():
    data = {
        'Bus_ID': ['Bus 01', 'Bus 05', 'Bus 12', 'Bus 18'],
        'Fault_Type': ['LLL', 'LG', 'LLG', 'LL'],
        'Voltage_Dip_pu': [0.2, 0.85, 0.45, 0.6],
        'Current_kA': [45.2, 12.5, 28.1, 19.8],
        'Location_km': [1.2, 5.8, 12.4, 18.2]
    }
    df = pd.DataFrame(data)
    
    # NEW STABLE SEVERITY LOGIC
    def calculate_severity(voltage):
        if voltage < 0.3:
            return 'Critical'
        elif 0.3 <= voltage < 0.7:
            return 'Medium'
        else:
            return 'Low'
    df['Severity'] = df['Voltage_Dip_pu'].apply(calculate_severity)
    return df
df = get_mock_data()
st.sidebar.header("⚡ Grid Control Center")
selected_bus = st.sidebar.selectbox("Select Fault Location", df['Bus_ID'])
fault_info = df[df['Bus_ID'] == selected_bus].iloc[0]
st.title("🛡️ Smart Grid Fault Detection & Analysis")
st.markdown(f"**Real-time Status:** Monitoring ETAP Short Circuit Analysis")
st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Fault Type", fault_info['Fault_Type'])
col2.metric("Current (kA)", f"{fault_info['Current_kA']} kA", delta="High Load", delta_color="inverse")
col3.metric("Voltage (pu)", f"{fault_info['Voltage_Dip_pu']} pu")
sev_color = {"Critical": "red", "Medium": "orange", "Low": "green"}
col4.markdown(f"**Severity** \n# :{sev_color[fault_info['Severity']]}[{fault_info['Severity']}]")
st.subheader("📊 Analytical Profiles")
tab1, tab2 = st.tabs(["Voltage Dip Profile", "Current Magnitude"])
with tab1:
    fig_volt = px.line(df, x='Location_km', y='Voltage_Dip_pu', markers=True, 
                       title="Voltage Profile Across Grid Distance",
                       labels={'Voltage_Dip_pu': 'Voltage (p.u.)', 'Location_km': 'Distance (km)'})
    fig_volt.add_hline(y=0.3, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
    st.plotly_chart(fig_volt, use_container_width=True)
with tab2:
    fig_curr = px.bar(df, x='Bus_ID', y='Current_kA', color='Severity',
                      color_discrete_map=sev_color, title="Fault Current per Bus")
    st.plotly_chart(fig_curr, use_container_width=True)
st.divider()
st.subheader("🛠️ Engineering Rectification Recommendations")
with st.expander("View Automated Action Plan", expanded=True):
    if fault_info['Severity'] == 'Critical':
        st.error("🚨 **Immediate Action Required:**")
        st.write("* Isolation of Bus via Circuit Breaker Trip.")
        st.write("* Check for Three-Phase Symmetrical Fault at Transformer Primary.")
        st.write("* Divert load to redundant Substation B.")
    elif fault_info['Severity'] == 'Medium':
        st.warning("⚠️ **Preventative Maintenance:**")
        st.write("* Inspect line insulators at the specified distance.")
        st.write("* Adjust Relay Coordination settings on Bus Relay.")
    else:
        st.success("✅ **Status Stable:**")
        st.write("Transient fault detected. Monitor harmonics for 24 hours.")
