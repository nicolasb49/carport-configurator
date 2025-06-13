import streamlit as st
import httpx

st.set_page_config(page_title="Carport Konfigurator")

MATERIAL_OPTIONS = ["Holz", "Aluminium", "Stahl"]
ROOF_OPTIONS = ["Flachdach", "Satteldach", "Walmdach"]
PV_OPTIONS = ["Mono", "Poly", "Glas-Glas"]

st.title("Carport Konfigurator")

with st.form("config_form"):
    col1, col2 = st.columns(2)
    with col1:
        material = st.selectbox(
            "Material",
            MATERIAL_OPTIONS,
            key="material",
        )
    with col2:
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
    submitted = st.form_submit_button("Berechnen")

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
    st.json(st.session_state["result"])
