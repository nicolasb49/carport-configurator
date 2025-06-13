import streamlit as st
import httpx
from pathlib import Path

st.set_page_config(page_title="Carport Konfigurator")

# Load and apply Hornbach theme
style_path = Path(__file__).parent / "style.css"
st.markdown(f"<style>{style_path.read_text()}</style>", unsafe_allow_html=True)

# Header configuration
LOGO_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/"
    "Hornbach_Logo.svg/1200px-Hornbach_Logo.svg.png"
)

HEADER_STYLE = """
<style>
.hb-header {
    background-color: var(--color-primary);
    width: 100%;
    padding: 0.5rem 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
}
.hb-header h1 {
    color: white;
    margin: 0 0 0 1rem;
}
</style>
"""

st.markdown(HEADER_STYLE, unsafe_allow_html=True)
st.markdown("<div class='hb-header'>", unsafe_allow_html=True)
header_col1, header_col2 = st.columns([1, 5])
header_col1.image(LOGO_URL, width=120)
header_col2.markdown("<h1>Carport Konfigurator</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

MATERIAL_OPTIONS = ["Holz", "Aluminium", "Stahl"]
ROOF_OPTIONS = ["Flachdach", "Satteldach", "Walmdach"]
PV_OPTIONS = ["Mono", "Poly", "Glas-Glas"]

with st.sidebar:
    with st.form("config_form"):
        material = st.selectbox(
            "Material",
            MATERIAL_OPTIONS,
            key="material",
        )
        roof_shape = st.selectbox(
            "Dachform",
            ROOF_OPTIONS,
            key="roof_shape",
        )
        pv_modules = st.multiselect(
            "PV-Module",
            PV_OPTIONS,
            key="pv_modules",
        )
        postal_code = st.text_input(
            "Postleitzahl",
            key="postal_code",
        )
        submitted = st.form_submit_button("Berechnen", use_container_width=True)

if submitted:
    payload = {
        "material": material,
        "roof_shape": roof_shape,
        "pv_modules": pv_modules,
        "postal_code": postal_code,
    }
    try:
        response = httpx.post("http://localhost:8000/configure", json=payload)
        response.raise_for_status()
        st.session_state["result"] = response.json()
    except Exception as e:
        st.error(f"Fehler beim Abrufen: {e}")

if "result" in st.session_state:
    st.subheader("Ergebnis")
    result = st.session_state["result"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <h3>Optimale Neigung</h3>
                <p>{result['optimal_tilt']}°</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="card">
                <h3>Drainage-Optionen</h3>
                <p>{', '.join(result['drainage_options'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <h3>Ertrag</h3>
                <p>{result['estimated_yield']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="card">
                <h3>Fundament-Optionen</h3>
                <p>{', '.join(result['foundation_options'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    import urllib.parse

    query = urllib.parse.urlencode(
        {
            "material": result["material"],
            "roof_shape": result["roof_shape"],
            "pv_modules": result["pv_modules"],
            "postal_code": result["postal_code"],
        },
        doseq=True,
    )
    download_url = f"http://localhost:8000/download?{query}"
    st.markdown(
        f'<a href="{download_url}"><button>PDF herunterladen</button></a>',
        unsafe_allow_html=True,
    )
