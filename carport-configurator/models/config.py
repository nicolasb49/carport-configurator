from typing import List
from pydantic import BaseModel

class CarportConfig(BaseModel):
    material: str
    roof_shape: str
    pv_modules: List[str]
    postal_code: str
