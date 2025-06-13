"""
Utility functions for solar calculations used by the carport configurator.
"""

from typing import List, Dict, Any
import httpx


async def fetch_solar_data(postal_code: str) -> Dict[str, Any]:
    """Fetch solar related weather data for a given postal code.

    This function first resolves the postal code to latitude and longitude using
    the free Zippopotam.us API. With these coordinates it queries the
    Open-Meteo API to obtain solar radiation data which can then be used for
    further calculations.
    """
    async with httpx.AsyncClient() as client:
        # Resolve postal code to coordinates
        geo_resp = await client.get(f"https://api.zippopotam.us/de/{postal_code}")
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()
        place = geo_data["places"][0]
        lat = float(place["latitude"])
        lon = float(place["longitude"])

        # Fetch hourly shortwave radiation data
        meteo_resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": "shortwave_radiation",
                "timezone": "UTC",
            },
        )
        meteo_resp.raise_for_status()
        meteo_data = meteo_resp.json()

    return {
        "latitude": lat,
        "longitude": lon,
        "radiation": meteo_data.get("hourly", {}).get("shortwave_radiation", []),
    }


def compute_optimal_tilt(solar_data: Dict[str, Any]) -> float:
    """Return a simple estimate for the optimal roof tilt.

    The calculation uses a very rough approximation derived from the
    geographical latitude which is sufficient for demonstration purposes.
    """
    latitude = float(solar_data.get("latitude", 0))
    # Simple empirical formula to approximate an all-year optimal tilt
    tilt = latitude * 0.76 + 3.1
    return max(0.0, min(90.0, tilt))


def compute_pv_yield(tilt: float, pv_modules: List[str], solar_data: Dict[str, Any]) -> float:
    """Estimate yearly PV yield in kWh based on solar radiation and module type."""
    radiation = solar_data.get("radiation", [])
    if radiation:
        # hourly radiation is given in Wh/m^2; convert to daily average kWh/m^2
        avg_rad = sum(radiation) / len(radiation) / 1000
    else:
        avg_rad = 0.0

    # Basic efficiencies for demonstration
    efficiencies = {
        "Mono": 0.20,
        "Poly": 0.17,
        "Glas-Glas": 0.18,
    }
    if pv_modules:
        eff = sum(efficiencies.get(m, 0.15) for m in pv_modules) / len(pv_modules)
    else:
        eff = 0.15

    # Tilt factor decreases output when deviating from the optimal tilt
    optimal = compute_optimal_tilt(solar_data)
    tilt_factor = max(0.0, 1 - abs(tilt - optimal) / 45)

    return avg_rad * eff * tilt_factor * 1000  # kWh estimate
