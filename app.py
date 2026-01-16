import streamlit as st
import pandas as pd
import statistics
import random
import plotly.graph_objects as go
import plotly.express as px
from src.engine import ServiceCenterSimulation

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Workflow Optimization Engine", layout="wide", page_icon="⚡")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .big-font { font-size: 20px !important; font-weight: bold; }
    .success-box { padding: 15px; background-color: #d4edda; border-radius: 10px; color: #155724; }
    .stStatusWidget { border: 1px solid #4CAF50 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Stochastic Throughput Optimization Engine")
st.markdown("### Digital Twin: Automated Service Center Analysis")

# --- SIDEBAR: SETTINGS ---
st.sidebar.header("⚙️ Simulation Parameters")
arrival_rate = st.sidebar.slider("Arrival Rate (Cars/Hour)", 1, 20, 4)
service_time = st.sidebar.slider("Avg Service Time (Min)", 5, 30, 10)
sim_duration = st.sidebar.number_input("Sim Duration (Min)", value=50000, help="Higher duration = more accurate stochastic convergence.")

st.sidebar.markdown("---")
st.sidebar.subheader("🛑 Scenario A: Baseline")
servers_A = st.sidebar.number_input("Baseline Servers", 1, 5, 1)
cap_A = st.sidebar.number_input("Baseline Queue Cap", 1, 20, 5)

st.sidebar.markdown("---")
st.sidebar.subheader("✅ Scenario B: Optimized")
servers_B = st.sidebar.number_input("Optimized Servers", 1, 10, 2)
cap_B = st.sidebar.number_input("Optimized Queue Cap", 1, 50, 5)

# --- CACHING FOR PERFORMANCE ---
@st.cache_data
def run_simulation_cached(servers, arr_rate, serv_time, cap, dur):
    random.seed(42) # Ensure reproducibility
    sim = ServiceCenterSimulation(servers, arr_rate, serv_time, cap, dur)
    return sim.run()

# --- MAIN EXECUTION ---
if st.button("🚀 Run Comparative Analysis"):
    
    # 1. STATUS INDICATOR (Clean Presentation Mode)
    with st.status("Processing Digital Twin Model...", expanded=True) as status:
        
        st.write(f"1️⃣ Simulating {sim_duration} minutes (Baseline)...")
        res_A = run_simulation_cached(servers_A, arrival_rate, service_time, cap_A, sim_duration)
        
        st.write(f"2️⃣ Simulating {sim_duration} minutes (Optimized)...")
        res_B = run_simulation_cached(servers_B, arrival_rate, service_time, cap_B, sim_duration)
        
        st.write("3️⃣ Calculating Operational KPIs...")
        
        # Helper Metric Function
        def get_metrics(res):
            waits = res["wait_times"]
            total = res["total_arrivals"]
            lost = res["lost_customers"]
            avg_wait = statistics.mean(waits) if waits else 0
            churn = (lost / total * 100) if total > 0 else 0
            throughput = len(waits)
            return avg_wait, churn, throughput

        wait_A, churn_A, thru_A = get_metrics(res_A)
        wait_B, churn_B, thru_B = get_metrics(res_B)
        
        status.update(label="✅ Simulation Complete! Rendering Dashboard...", state="complete", expanded=False)

    # 2. KPI METRICS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.error(f"🛑 Baseline (M/M/{servers_A})")
        st.metric("Avg Wait Time", f"{wait_A:.2f} min")
        st.metric("Churn Rate", f"{churn_A:.2f}%")
        st.metric("Throughput", f"{thru_A}")

    with col2:
        st.success(f"✅ Optimized (M/M/{servers_B})")
        st.metric("Avg Wait Time", f"{wait_B:.2f} min", delta=f"{wait_A - wait_B:.2f} min")
        st.metric("Churn Rate", f"{churn_B:.2f}%", delta=f"{churn_A - churn_B:.2f}%")
        st.metric("Throughput", f"{thru_B}", delta=f"+{thru_B - thru_A}")

    with col3:
        st.info("💡 ROI Analysis")
        wait_imp = ((wait_A - wait_B) / wait_A * 100) if wait_A > 0 else 0
        st.write(f"**Efficiency Gain:** {wait_imp:.1f}%")
        if wait_imp > 90:
            st.markdown("<div class='success-box'>🚀 <b>Outstanding Result!</b><br>Optimization has effectively eliminated the bottleneck.</div>", unsafe_allow_html=True)

    # 3. VISUALIZATION (Downsampled for Speed)
    st.markdown("---")
    tab1, tab2 = st.tabs(["Wait Time Dynamics", "Throughput Volume"])

    with tab1:
        # Aggressive Downsampling: Max 500 points to keep browser fast
        def downsample_safe(df, target=500):
            if len(df) > target:
                return df.iloc[::len(df)//target, :]
            return df

        df_A = pd.DataFrame({"Time": res_A["timestamps"], "Wait": res_A["wait_times"], "Scenario": "Baseline"})
        df_B = pd.DataFrame({"Time": res_B["timestamps"], "Wait": res_B["wait_times"], "Scenario": "Optimized"})
        
        combined_df = pd.concat([downsample_safe(df_A), downsample_safe(df_B)])
        
        fig_wait = px.line(combined_df, x="Time", y="Wait", color="Scenario", 
                           title=f"Wait Time Dynamics ({sim_duration} min horizon)",
                           color_discrete_map={"Baseline": "#EF553B", "Optimized": "#00CC96"})
        st.plotly_chart(fig_wait, use_container_width=True)

    with tab2:
        fig_bar = go.Figure(data=[
            go.Bar(name='Baseline', x=['Volume'], y=[thru_A], marker_color='#EF553B'),
            go.Bar(name='Optimized', x=['Volume'], y=[thru_B], marker_color='#00CC96')
        ])
        fig_bar.update_layout(title="Total System Throughput Comparison")
        st.plotly_chart(fig_bar, use_container_width=True)

    # 4. QUEUE DISTRIBUTION
    st.markdown("### 🌡️ Queue Load Distribution")
    c1, c2 = st.columns(2)
    
    def get_dist(data_list):
        s = pd.Series(data_list)
        return s.value_counts().sort_index()

    with c1:
        st.write("**Baseline Distribution**")
        st.bar_chart(get_dist(res_A["queue_lengths"]))
    with c2:
        st.write("**Optimized Distribution**")
        st.bar_chart(get_dist(res_B["queue_lengths"]))

else:
    st.info("Adjust parameters in the sidebar and click 'Run Comparative Analysis' to start.")