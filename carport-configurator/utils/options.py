from typing import List


def list_drainage_options(material: str, roof_shape: str) -> List[str]:
    """Return drainage options based on material and roof shape."""
    options: List[str] = []
    material_l = material.lower()
    roof_l = roof_shape.lower()

    if roof_l == "flachdach":
        options.append("Innenliegende Dachrinne")
    else:
        options.append("Au\u00dfenliegende Dachrinne")

    if material_l == "holz":
        options.append("Kupferrinne")
    elif material_l == "aluminium":
        options.append("Alu-Rinne")
    else:
        options.append("Stahl-Rinne")

    return options


def list_foundation_options(material: str, roof_shape: str) -> List[str]:
    """Return foundation options based on material and roof shape."""
    options: List[str] = []
    material_l = material.lower()
    roof_l = roof_shape.lower()

    if material_l == "holz":
        options.extend(["Punktfundament", "Erdanker"])
    elif material_l == "aluminium":
        options.extend(["Schraubfundament", "Betonfundament"])
    else:
        options.extend(["Streifenfundament", "Betonfundament"])

    if roof_l == "flachdach":
        options.append("Bodenplatte")

    return options
