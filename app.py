import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Workstyle Lens Calculator", layout="centered")

# Custom CSS to enlarge all text by ~2 points
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        font-size: 18px !important;
    }
    .stMarkdown p, .stWidgetLabel, label, span {
        font-size: 18px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("👓 Workstyle V+ Lens Calculator")
st.markdown("Enter your **Distance Rx** and **Near ADD** only to calculate the powers at the fitting cross and 8mm above the fitting cross.")

# Input Section
col1, col2 = st.columns(2)
with col1:
    distance_rx = st.number_input("Distance Rx (Sphere)", value=2.00, step=0.25, format="%.2f")
with col2:
    near_add = st.number_input("Near ADD", value=2.50, step=0.25, format="%.2f")

def calculate_lenses(c3, c9):
    results = {}
    
    # --- Workstyle Space (Column C) ---
    c_c3 = c3
    c_c9 = c9
    c_c11 = c_c9 * 0.43
    c_c6 = c_c11 + c_c3  # Fitting Cross
    c_c19 = c_c3
    c_c20 = c_c9 / 30 + c_c19
    c_c21 = c_c9 / 15 + c_c20
    c_c22 = c_c9 / 15 + c_c21  # 8mm Above
    results['Workstyle Space'] = {
        'RX AT FITTING CROSS': f"{c_c6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{c_c22:.2f}"
    }

    # --- Workstyle Screen (Column E) ---
    e_e3 = c_c3 + (0.22 * c_c9)
    e_e13 = c_c3 + c_c9
    e_e9 = e_e13 - e_e3
    e_e11 = e_e9 * 0.43
    e_e6 = e_e11 + e_e3
    e_e19 = e_e3
    e_e20 = e_e9 / 30 + e_e19
    e_e21 = e_e9 / 15 + e_e20
    e_e22 = e_e9 / 15 + e_e21
    results['Workstyle Screen'] = {
        'RX AT FITTING CROSS': f"{e_e6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{e_e22:.2f}"
    }

    # --- Workstyle Screen (Adds 2.50D & Over) (Column G) ---
    g_g3 = c_c3 + 0.54
    g_g9 = c_c9 - 0.54
    g_g11 = g_g9 * 0.43
    g_g6 = g_g11 + g_g3
    g_g19 = g_g3
    g_g20 = g_g9 / 30 + g_g19
    g_g21 = g_g9 / 15 + g_g20
    g_g22 = g_g9 / 15 + g_g21
    results['Workstyle Screen (Adds 2.50D & Over)'] = {
        'RX AT FITTING CROSS': f"{g_g6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{g_g22:.2f}"
    }

    # --- Workstyle Close (Column H) ---
    h_h3 = c_c3 + (0.4 * c_c9)
    h_h13 = c_c3 + c_c9
    h_h9 = h_h13 - h_h3
    h_h11 = h_h9 * 0.43
    h_h6 = h_h3 + h_h11
    h_h20 = h_h3
    h_h21 = (h_h9 / 14) + h_h20
    h_h22 = (h_h9 / 14) + h_h21
    results['Workstyle Close'] = {
        'RX AT FITTING CROSS': f"{h_h6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{h_h22:.2f}"
    }

    # --- Workstyle Close (Add 2.50D & Over) (Column J) ---
    j_j3 = c_c3 + 1.0
    j_j9 = c_c9 - 1.0
    j_j11 = j_j9 * 0.43
    j_j6 = j_j3 + j_j11
    j_j20 = j_j3
    j_j21 = (j_j9 / 14) + j_j20
    j_j22 = (j_j9 / 14) + j_j21
    results['Workstyle Close (Add 2.50D & Over)'] = {
        'RX AT FITTING CROSS': f"{j_j6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{j_j22:.2f}"
    }

    return results

# Run calculations
data = calculate_lenses(distance_rx, near_add)

# Convert to DataFrame and transpose
df_display = pd.DataFrame(data).T

# Reset index so lens type becomes a proper column named 'Lens Type'
df_display = df_display.reset_index().rename(columns={'index': 'Lens Type'})

# Style the DataFrame to make the 'Lens Type' column bold
styled_df = df_display.style.set_properties(
    subset=['Lens Type'], 
    **{'font-weight': 'bold'}
)

st.markdown("---")
st.subheader("📋 Calculation Results")
st.dataframe(styled_df, use_container_width=True, hide_index=True)
