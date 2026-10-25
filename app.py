import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(page_title="Workstyle Lens Calculator", layout="centered")

# Custom CSS for Professional Clinical Styling, A4 Printing, Mobile Responsiveness, and Header Wrapping
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        font-size: 18px !important;
        color: #334155 !important;
        background-color: #F8FAFC !important;
    }
    .stMarkdown p, .stWidgetLabel, label, span {
        font-size: 18px !important;
        color: #334155 !important;
    }
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
    [data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px;
    }
    
    /* True HTML Table Header Styling (Works with st.table) */
    table {
        width: 100% !important;
        border-collapse: collapse !important;
    }
    table th {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.3 !important;
        height: 60px !important;
        padding: 8px 12px !important;
        vertical-align: middle !important;
        text-align: center !important;
        font-weight: 600 !important;
    }
    table td {
        padding: 10px 12px !important;
        text-align: center !important;
        vertical-align: middle !important;
    }
    
    @media (max-width: 768px) {
        html, body, [data-testid="stAppViewContainer"] {
            font-size: 15px !important;
        }
        .stMarkdown p, .stWidgetLabel, label, span {
            font-size: 15px !important;
        }
        h1 {
            font-size: 20px !important;
        }
    }
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
        table th {
            background-color: #E2E8F0 !important;
            color: #000000 !important;
            border: 1px solid #94A3B8 !important;
        }
        table td {
            border: 1px solid #94A3B8 !important;
            color: #000000 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.header("📁 Patient & Order Details")
patient_name = st.sidebar.text_input("Patient Name / ID", value="")
clinical_notes = st.sidebar.text_area("Clinical Notes / Instructions", value="")
st.sidebar.markdown("---")
st.sidebar.info("Use this sidebar to record patient-specific info or clinical notes.")

st.title("Workstyle Lens Calculator")
st.markdown("Enter the **Distance Rx** and **Near ADD** only to calculate the powers **at the fitting cross**, 8mm above the fitting cross, and the **Full Near Rx**.")

# Input Section
col1, col2 = st.columns(2)
with col1:
    distance_rx = st.number_input("Distance Rx (Sphere)", value=2.00, step=0.25, format="%.2f")
with col2:
    near_add = st.number_input("Near ADD", value=2.50, step=0.25, format="%.2f")

def calculate_lenses(c3, c9):
    results = {}
    full_near_rx = c3 + c9
    
    # Workstyle Space (Column C)
    c_c3, c_c9 = c3, c9
    c_c11 = c_c9 * 0.43
    c_c6 = c_c11 + c_c3
    c_c22 = (c_c9 / 30 + c_c3) + (c_c9 / 15) * 2
    results['Workstyle Space'] = {
        'RX AT FITTING CROSS': f"{c_c6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{c_c22:.2f}",
        'Full Near Rx': f"{full_near_rx:.2f}"
    }

    # Workstyle Screen (Column E)
    e_e3 = c_c3 + (0.22 * c_c9)
    e_e13 = c_c3 + c_c9
    e_e9 = e_e13 - e_e3
    e_e6 = (e_e9 * 0.43) + e_e3
    e_e22 = e_e3 + (e_e9 / 30) + (e_e9 / 15) * 2
    results['Workstyle Screen'] = {
        'RX AT FITTING CROSS': f"{e_e6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{e_e22:.2f}",
        'Full Near Rx': f"{full_near_rx:.2f}"
    }

    # Workstyle Screen (Adds 2.50D & Over) (Column G)
    g_g3 = c_c3 + 0.54
    g_g9 = c_c9 - 0.54
    g_g6 = (g_g9 * 0.43) + g_g3
    g_g22 = g_g3 + (g_g9 / 30) + (g_g9 / 15) * 2
    results['Workstyle Screen (Adds 2.50D & Over)'] = {
        'RX AT FITTING CROSS': f"{g_g6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{g_g22:.2f}",
        'Full Near Rx': f"{full_near_rx:.2f}"
    }

    # Workstyle Close (Column H)
    h_h3 = c_c3 + (0.4 * c_c9)
    h_h13 = c_c3 + c_c9
    h_h9 = h_h13 - h_h3
    h_h6 = h_h3 + (h_h9 * 0.43)
    h_h22 = h_h3 + (h_h9 / 14) * 2
    results['Workstyle Close'] = {
        'RX AT FITTING CROSS': f"{h_h6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{h_h22:.2f}",
        'Full Near Rx': f"{full_near_rx:.2f}"
    }

    # Workstyle Close (Add 2.50D & Over) (Column J)
    j_j3 = c_c3 + 1.0
    j_j9 = c_c9 - 1.0
    j_j6 = j_j3 + (j_j9 * 0.43)
    j_j22 = j_j3 + (j_j9 / 14) * 2
    results['Workstyle Close (Add 2.50D & Over)'] = {
        'RX AT FITTING CROSS': f"{j_j6:.2f}", 
        'RX 8MM ABOVE FITTING CROSS': f"{j_j22:.2f}",
        'Full Near Rx': f"{full_near_rx:.2f}"
    }

    return results

# Run calculations
data = calculate_lenses(distance_rx, near_add)
df_display = pd.DataFrame(data).T.reset_index().rename(columns={'index': 'Lens Type'})

styled_df = df_display.style.set_properties(subset=['Lens Type'], **{'font-weight': 'bold', 'text-align': 'left'})

st.markdown("---")
if patient_name:
    st.subheader(f"📋 Calculation Results for: {patient_name}")
else:
    st.subheader("📋 Calculation Results")

if clinical_notes:
    st.markdown(f"**Notes:** {clinical_notes}")

# Using st.table to allow full CSS header wrapping, height, and custom styling
st.table(styled_df)

# Action Buttons Layout
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
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
