from fastapi import FastAPI
from models.config import CarportConfig, CarportResponse
from utils.calculation import (
    fetch_solar_data,
    compute_optimal_tilt,
    compute_pv_yield,
)
from utils.options import list_drainage_options, list_foundation_options

app = FastAPI()

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.post("/configure", response_model=CarportResponse)
async def configure(config: CarportConfig) -> CarportResponse:
    solar_data = await fetch_solar_data(config.postal_code)
    optimal_tilt = compute_optimal_tilt(solar_data)
    estimated_yield = compute_pv_yield(optimal_tilt, config.pv_modules, solar_data)
    drainage_options = list_drainage_options(config.material, config.roof_shape)
    foundation_options = list_foundation_options(config.material, config.roof_shape)

    return CarportResponse(
        material=config.material,
        roof_shape=config.roof_shape,
        pv_modules=config.pv_modules,
        postal_code=config.postal_code,
        optimal_tilt=optimal_tilt,
        estimated_yield=estimated_yield,
        drainage_options=drainage_options,
        foundation_options=foundation_options,
    )
