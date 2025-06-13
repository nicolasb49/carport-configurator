from io import BytesIO
from typing import Any, Dict

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def generate_material_list_pdf(config_data: Dict[str, Any], calculation_results: Dict[str, Any], options: Dict[str, Any]) -> bytes:
    """Generate a simple material list PDF.

    Parameters
    ----------
    config_data: Dict[str, Any]
        Original configuration values.
    calculation_results: Dict[str, Any]
        Calculated results such as tilt or PV yield.
    options: Dict[str, Any]
        Additional options lists.
    Returns
    -------
    bytes
        The generated PDF as bytes.
    """

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Materialliste", styles["Title"]))
    elements.append(Spacer(1, 12))

    def section(title: str, data: Dict[str, Any]):
        elements.append(Paragraph(title, styles["Heading2"]))
        table_data = [["Schlüssel", "Wert"]]
        for key, value in data.items():
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            table_data.append([str(key), str(value)])
        table = Table(table_data, hAlign="LEFT")
        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        elements.append(table)
        elements.append(Spacer(1, 12))

    section("Konfiguration", config_data)
    section("Berechnung", calculation_results)
    section("Optionen", options)

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
