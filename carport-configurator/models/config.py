from typing import List
from pydantic import BaseModel

class CarportConfig(BaseModel):
    material: str
    roof_shape: str
    pv_modules: List[str]
    postal_code: str


class CarportResponse(CarportConfig):
    optimal_tilt: float
    estimated_yield: float
    drainage_options: List[str]
    foundation_options: List[str]
