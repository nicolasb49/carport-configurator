from fastapi import FastAPI
from models.config import CarportConfig
from utils.calculation import (
    fetch_solar_data,
    compute_optimal_tilt,
    compute_pv_yield,
)

app = FastAPI()

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.post("/configure")
async def configure(config: CarportConfig):
    solar_data = await fetch_solar_data(config.postal_code)
    optimal_tilt = compute_optimal_tilt(solar_data)
    estimated_yield = compute_pv_yield(optimal_tilt, config.pv_modules, solar_data)

    return {
        "material": config.material,
        "roof_shape": config.roof_shape,
        "pv_modules": config.pv_modules,
        "postal_code": config.postal_code,
        "optimal_tilt": optimal_tilt,
        "estimated_yield": estimated_yield,
    }
