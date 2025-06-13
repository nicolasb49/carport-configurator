import streamlit as st
import httpx
from pathlib import Path
import base64

st.set_page_config(page_title="Carport Konfigurator")

# Load and apply Hornbach theme
style_path = Path(__file__).parent / "style.css"
st.markdown(f"<style>{style_path.read_text()}</style>", unsafe_allow_html=True)

# Load icons as base64 strings
icon_dir = Path(__file__).parent / "assets" / "icons"

def load_icon(name: str) -> str:
    return base64.b64encode((icon_dir / name).read_bytes()).decode()

ICON_MATERIAL = load_icon("material.svg")
ICON_ROOF = load_icon("roof.svg")
ICON_PV = load_icon("pv.svg")
ICON_POSTAL = load_icon("postal_code.svg")

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
        st.markdown(
            f"<label class='icon-label'><img src='data:image/svg+xml;base64,{ICON_MATERIAL}' width='20'> Material</label>",
            unsafe_allow_html=True,
        )
        material = st.selectbox(
            "",
            MATERIAL_OPTIONS,
            key="material",
            label_visibility="collapsed",
        )
        st.markdown(
            f"<label class='icon-label'><img src='data:image/svg+xml;base64,{ICON_ROOF}' width='20'> Dachform</label>",
            unsafe_allow_html=True,
        )
        roof_shape = st.selectbox(
            "",
            ROOF_OPTIONS,
            key="roof_shape",
            label_visibility="collapsed",
        )
        st.markdown(
            f"<label class='icon-label'><img src='data:image/svg+xml;base64,{ICON_PV}' width='20'> PV-Module</label>",
            unsafe_allow_html=True,
        )
        pv_modules = st.multiselect(
            "",
            PV_OPTIONS,
            key="pv_modules",
            label_visibility="collapsed",
        )
        st.markdown(
            f"<label class='icon-label'><img src='data:image/svg+xml;base64,{ICON_POSTAL}' width='20'> Postleitzahl</label>",
            unsafe_allow_html=True,
        )
        postal_code = st.text_input(
            "",
            key="postal_code",
            label_visibility="collapsed",
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
