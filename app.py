import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(page_title="Workstyle Lens Calculator", layout="centered")

# Custom CSS for Professional Clinical Styling & A4 Portrait Printing
st.markdown("""
<style>
    /* Base typography and colors */
    html, body, [data-testid="stAppViewContainer"] {
        font-size: 18px !important;
        color: #334155 !important;
        background-color: #F8FAFC !important;
    }
    
    .stMarkdown p, .stWidgetLabel, label, span {
        font-size: 18px !important;
        color: #334155 !important;
    }

    /* Headings styling */
    h1 {
        color: #1E3A8A !important;
        font-weight: 700 !important;
        border-bottom: 2px solid #CBD5E1;
        padding-bottom: 10px;
    }
    
    h2, h3 {
        color: #1E3A8A !important;
        font-weight: 600 !important;
    }

    /* Input containers styling */
    [data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px;
    }

    /* Print-specific styling for A4 Portrait */
    @media print {
        @page {
            size: A4 portrait;
            margin: 20mm;
        }
        
        body, [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
        }

        header, [data-testid="stSidebar"], .stDownloadButton, iframe {
            display: none !important;
        }

        h1 {
            font-size: 22px !important;
            color: #000000 !important;
            border-bottom: 1px solid #000000 !important;
        }

        table {
            width: 100% !important;
            border-collapse: collapse !important;
            margin-top: 20px !important;
        }

        th, td {
            border: 1px solid #94A3B8 !important;
            padding: 10px !important;
            font-size: 14px !important;
            color: #000000 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Configuration ---
st.sidebar.header("📁 Patient & Order Details")
patient_name = st.sidebar.text_input("Patient Name / ID", value="")
clinical_notes = st.sidebar.text_area("Clinical Notes / Instructions", value="")
st.sidebar.markdown("---")
st.sidebar.info("Use this sidebar to record patient-specific info or clinical notes.")

# Restored user text choices
st.title("Workstyle Lens Calculator")
st.markdown("Enter the **Distance Rx** and **Near ADD** only to calculate the powers **at the fitting cross** and 8mm above the fitting cross.")

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

if patient_name:
    st.subheader(f"📋 Calculation Results for: {patient_name}")
else:
    st.subheader("📋 Calculation Results")

# Display clinical notes on screen if entered
if clinical_notes:
    st.markdown(f"**Notes:** {clinical_notes}")

st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Action Buttons Layout (Download & Print side by side)
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    # Convert DataFrame to CSV for the download button
    csv_data = df_display.to_csv(index=False).encode('utf-8')
    file_prefix = patient_name.strip().replace(' ', '_') if patient_name else "workstyle_lens"
    
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv_data,
        file_name=f"{file_prefix}_calculations.csv",
        mime="text/csv",
        use_container_width=True
    )

with btn_col2:
    # Print Button targeting the whole page
    print_html = """
    <div style="display: flex; align-items: center;">
        <button onclick="window.parent.print()" style="
            width: 100%;
            background-color: #ffffff;
            color: #1E3A8A;
            border: 1px solid #1E3A8A;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-align: center;
            font-family: 'Source Sans Pro', sans-serif;
            transition: all 0.2s;
        ">
            🖨️ Print Results
        </button>
    </div>
    <script>
        const btn = document.querySelector('button');
        btn.onmouseover = () => { btn.style.backgroundColor = '#1E3A8A'; btn.style.color = '#ffffff'; };
        btn.onmouseout = () => { btn.style.backgroundColor = '#ffffff'; btn.style.color = '#1E3A8A'; };
    </script>
    """
    components.html(print_html, height=50)
