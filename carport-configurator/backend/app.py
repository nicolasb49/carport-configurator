from fastapi import FastAPI
from models.config import CarportConfig

app = FastAPI()

@app.get("/health")
def read_health():
    return {"status": "ok"}

@app.post("/configure")
def configure(config: CarportConfig):
    # Placeholder response reflecting received data
    return {
        "material": config.material,
        "roof_shape": config.roof_shape,
        "pv_modules": config.pv_modules,
        "postal_code": config.postal_code,
    }
