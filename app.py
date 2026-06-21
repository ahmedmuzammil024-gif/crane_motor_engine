import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import fsolve

# 1. Page Configuration
st.set_page_config(page_title="Crane Motor Telemetry", layout="wide", initial_sidebar_state="collapsed")

# 2. Ultra-Modern UI/UX Overhaul (Deep Dark Mode & Neon Accents)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Global App Background */
    .stApp { background-color: #0B0F19; }
    .block-container { padding-top: 2rem; max-width: 98%; }
    
    /* Clean up default Streamlit elements */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Typography */
    .dash-title {
        font-size: 2.5rem; font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #A0AEC0 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem; letter-spacing: -1px;
    }
    .dash-subtitle { color: #718096; font-size: 1rem; margin-bottom: 2rem; font-weight: 400; }

    /* Minimalist Glass Cards */
    .param-card {
        background: rgba(15, 23, 42, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px; padding: 20px; height: 100%;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }
    .card-header {
        color: #A0AEC0; font-size: 0.8rem; text-transform: uppercase;
        letter-spacing: 1.5px; font-weight: 700; margin-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 10px;
    }
    .card-list { color: #E2E8F0; font-size: 0.95rem; line-height: 1.8; }
    .highlight-cyan { color: #00C9FF; font-weight: 700; text-shadow: 0 0 10px rgba(0, 201, 255, 0.3); }
    .highlight-emerald { color: #34D399; font-weight: 700; text-shadow: 0 0 10px rgba(52, 211, 153, 0.3); }
    
    /* Section Labels */
    .section-label {
        font-size: 1.05rem; color: #F7FAFC; font-weight: 600;
        margin-top: 1.8rem; margin-bottom: 1rem; letter-spacing: -0.2px;
    }
    
    /* Override Streamlit Inputs for a Sleek Look */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div {
        background-color: #1A202C !important;
        border: 1px solid #2D3748 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"]:focus-within > div,
    div[data-baseweb="select"]:focus-within > div {
        border-color: #00C9FF !important;
        box-shadow: 0 0 0 1px #00C9FF !important;
    }
    
    /* Live Equation Box */
    .live-eq-box {
        background: linear-gradient(180deg, #1A202C 0%, #0F172A 100%);
        padding: 15px; border-radius: 12px;
        text-align: center; margin-top: 15px; 
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Modernize Primary Button */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00C9FF 0%, #0088FF 100%);
        color: white; border: none; border-radius: 8px;
        font-weight: 600; padding: 0.6rem 0; font-size: 1rem;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-top: 15px;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 201, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown('<div class="dash-title">Crane Motor Configuration Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="dash-subtitle">Real-time load line intersection analysis and motor performance telemetry.</div>', unsafe_allow_html=True)

# --- ARCHITECTURE ---
left_pane, right_pane = st.columns([1, 1.6], gap="large")

with left_pane:
    # Specifications Layout
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="param-card">
            <div class="card-header">Operational Goals</div>
            <div class="card-list">
                • <b>Starting:</b> > <span class="highlight-cyan">160 Nm</span><br>
                • <b>Heavy (48 Nm):</b> Decelerate<br>
                • <b>Light (12 Nm):</b> Accelerate
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="param-card">
            <div class="card-header">System Specs</div>
            <div class="card-list">
                • <b>Limit:</b> <span class="highlight-emerald">80 A</span> max<br>
                • <b>Motor 1:</b> k&Phi; = 1.5<br>
                • <b>Motor 2:</b> k&Phi; = 0.03 I<sub>a</sub>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- PART 1: Starting Torques ---
    st.markdown('<div class="section-label">1. Output Constraints (Nm)</div>', unsafe_allow_html=True)
    t_col1, t_col2 = st.columns(2)
    with t_col1: t1_input = st.number_input("Motor 1 Start Torque", min_value=0.0, step=1.0, format="%.1f")
    with t_col2: t2_input = st.number_input("Motor 2 Start Torque", min_value=0.0, step=1.0, format="%.1f")

    # --- PART 2: Motor Selection (Moved) ---
    st.markdown('<div class="section-label">2. Which motor is suitable for the application:</div>', unsafe_allow_html=True)
    mcq_selection = st.selectbox("Motor Selection", ["Pending...", "Motor 1", "Motor 2", "None"], label_visibility="collapsed")

    # --- PART 3: Derivations & Dynamic Equations ---
    st.markdown('<div class="section-label">3. Mathematical Derivations</div>', unsafe_allow_html=True)
    
    eq1_c1, eq1_c2 = st.columns(2)
    with eq1_c1:
        st.caption("Motor 1: $\omega = A - B \cdot T$")
        blank_a = st.number_input("Value A", min_value=0.0, step=1.0, format="%.1f")
        blank_b = st.number_input("Value B", min_value=0.0, step=0.0001, format="%.4f")
    with eq1_c2:
        st.caption("Motor 2: $\omega = \\frac{C}{\sqrt{0.03 \cdot T}} - D$")
        blank_c = st.number_input("Value C", min_value=0.0, step=1.0, format="%.1f")
        blank_d = st.number_input("Value D", min_value=0.0, step=0.01, format="%.2f")

    st.markdown('<div class="live-eq-box">', unsafe_allow_html=True)
    st.caption("Live Equation Preview")
    m1_display = f"\\omega = {blank_a} - {blank_b} \\cdot T" if blank_a or blank_b else r"\omega = A - B \cdot T"
    m2_display = f"\\omega = \\frac{{{blank_c}}}{{\\sqrt{{0.03 \\cdot T}}}} - {blank_d}" if blank_c or blank_d else r"\omega = \frac{C}{\sqrt{0.03 \cdot T}} - D"
    st.latex(m1_display)
    st.latex(m2_display)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PART 4: Load Profiling ---
    st.markdown('<div class="section-label">4. Speed at Specific Loads (rad/s)</div>', unsafe_allow_html=True)
    st.caption("Type 'None' if the motor is unsuitable or cannot adapt to the profile.")
    
    sp_c1, sp_c2 = st.columns(2)
    with sp_c1:
        m1_48 = st.text_input("Motor 1 Speed @ 48 Nm", "")
        m1_12 = st.text_input("Motor 1 Speed @ 12 Nm", "")
    with sp_c2:
        m2_48 = st.number_input("Motor 2 Speed @ 48 Nm", min_value=0.0, step=1.0, format="%.1f")
        m2_12 = st.number_input("Motor 2 Speed @ 12 Nm", min_value=0.0, step=1.0, format="%.1f")

    # --- Submit Trigger ---
    st.write("")
    submit_btn = st.button("Initialize Telemetry & Plot Trajectory", type="primary", use_container_width=True)

with right_pane:
    if submit_btn:
        correct_t1, correct_t2 = 120.0, 192.0
        correct_a, correct_b = 160.0, 0.1778
        correct_c, correct_d = 240.0, 13.33
        
        math_correct = (t1_input == correct_t1) and (t2_input == correct_t2)
        eq1_correct = (blank_a == correct_a) and (abs(blank_b - correct_b) < 0.001)
        eq2_correct = (blank_c == correct_c) and (abs(blank_d - correct_d) < 0.05)
        m1_spd_correct = (m1_48.strip().lower() == "none") and (m1_12.strip().lower() == "none")
        m2_spd_correct = (abs(m2_48 - 187) < 2.0) and (abs(m2_12 - 387) < 2.0)
        
        if math_correct and eq1_correct and eq2_correct and m1_spd_correct and m2_spd_correct and mcq_selection == "Motor 2":
            
            def load_curve(T): return 516.45 * np.exp(-0.01829 * T) - 27.69
            def motor1_curve(T): return blank_a - blank_b * T
            def motor2_curve(T): return blank_c / np.sqrt(0.03 * np.maximum(T, 0.001)) - blank_d

            def find_intersections(func1, func2, guesses):
                roots = []
                for guess in guesses:
                    root, _, ier, _ = fsolve(lambda x: func1(x) - func2(x), guess, full_output=True)
                    if ier == 1 and 0 < root[0] < 200:
                        if not any(abs(root[0] - r) < 2.0 for r in roots): roots.append(root[0])
                return roots

            m1_load_roots = find_intersections(motor1_curve, load_curve, [10, 60, 150])
            m2_load_roots = find_intersections(motor2_curve, load_curve, [5, 40, 100])

            T_vals = np.linspace(1, 200, 600)
            m2_plot_vals = np.minimum(motor2_curve(T_vals), 500)
            
            fig = go.Figure()

            # Add Traces (Lines)
            fig.add_trace(go.Scatter(x=T_vals, y=motor1_curve(T_vals), mode='lines', name='Motor 1', line=dict(color='#00C9FF', width=3)))
            fig.add_trace(go.Scatter(x=T_vals, y=m2_plot_vals, mode='lines', name='Motor 2', line=dict(color='#34D399', width=3)))
            fig.add_trace(go.Scatter(x=T_vals, y=load_curve(T_vals), mode='lines', name='Ideal Load Line', line=dict(color='#FB923C', width=2, dash='dash')))

            # Add Intersections with ALWAYS-ON TEXT
            for r in m1_load_roots:
                fig.add_trace(go.Scatter(
                    x=[r], y=[motor1_curve(r)], mode='markers+text', showlegend=False,
                    marker=dict(color='#0B0F19', size=10, line=dict(color='#00C9FF', width=2.5)),
                    text=[f"M1: ({r:.1f}, {motor1_curve(r):.0f})"],
                    textposition="bottom left",
                    textfont=dict(color='#00C9FF', size=12, family="Inter", weight="bold"),
                    hovertemplate=f"Torque: {r:.1f} Nm<br>Speed: {motor1_curve(r):.1f} rad/s<extra></extra>"
                ))
                
            for r in m2_load_roots:
                t_pos = "top right" if r < 20 else "top right"
                fig.add_trace(go.Scatter(
                    x=[r], y=[motor2_curve(r)], mode='markers+text', showlegend=False,
                    marker=dict(color='#0B0F19', size=10, line=dict(color='#34D399', width=2.5)),
                    text=[f"M2: ({r:.1f}, {motor2_curve(r):.0f})"],
                    textposition=t_pos,
                    textfont=dict(color='#34D399', size=12, family="Inter", weight="bold"),
                    hovertemplate=f"Torque: {r:.1f} Nm<br>Speed: {motor2_curve(r):.1f} rad/s<extra></extra>"
                ))

            # Modern Layout Styling (Deep Dark Minimalist)
            fig.update_layout(
                plot_bgcolor='#0B0F19',
                paper_bgcolor='#0B0F19',
                font=dict(family="Inter", color="#718096"),
                xaxis=dict(
                    title="<b>Torque (Nm)</b>", range=[0, 200], 
                    gridcolor='#1A202C', zerolinecolor='#2D3748', zerolinewidth=2
                ),
                yaxis=dict(
                    title="<b>Speed (rad/s)</b>", range=[0, 450], 
                    gridcolor='#1A202C', zerolinecolor='#2D3748', zerolinewidth=2
                ),
                legend=dict(
                    yanchor="top", y=0.95, xanchor="right", x=0.95, 
                    bgcolor="rgba(11, 15, 25, 0.8)", bordercolor="#2D3748", borderwidth=1,
                    font=dict(color="#E2E8F0")
                ),
                margin=dict(l=20, r=20, t=40, b=20),
                hovermode="x unified",
                height=650 
            )

            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.error("Diagnostic Error: Invalid Parameters Detected. Please verify constraints.")
            if not math_correct: st.info("- Torques: Recalculate using Ia = 80 A.")
            if mcq_selection != "Motor 2": st.info("- Selection: Which motor fulfills the load constraints?")
            if not eq1_correct: st.info("- Motor 1 Eq: Verify algebraic reduction.")
            if not eq2_correct: st.info("- Motor 2 Eq: Check inverse-root substitution.")
            if not m1_spd_correct: st.info("- Motor 1 Speeds: Does Motor 1 naturally adapt to these profiles? Use 'None'.")
            if not m2_spd_correct: st.info("- Motor 2 Speeds: Re-calculate speed at exactly 48 Nm and 12 Nm.")
    else:
        st.markdown("""
        <div style="display: flex; height: 100%; min-height: 650px; align-items: center; justify-content: center; background: radial-gradient(circle at center, #1A202C 0%, #0B0F19 100%); border: 1px dashed #2D3748; border-radius: 16px;">
            <div style="text-align: center; color: #4A5568;">
                <h2 style="margin-bottom: 5px; color: #718096;">Visualization Canvas Offline</h2>
                <p>Input valid parameters on the left to render the telemetry plot.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)