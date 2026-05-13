from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    waste_type: str = Field(..., example="fruit_waste")
    sugar_content: float = Field(..., ge=0, example=18.5)
    nitrogen_content: float = Field(..., ge=0, example=2.1)
    moisture: float = Field(..., ge=0, le=100, example=72)
    ph: float = Field(..., ge=0, le=14, example=5.8)
    temperature: float = Field(..., example=32)
    fermentation_time: float = Field(..., ge=0, example=48)
    waste_volume_kg: float = Field(..., ge=0, example=100)
    location: str = Field(default="Unknown", example="Leeds")


class PredictionOutput(BaseModel):
    predicted_protein_yield: float
    uncertainty: float
    confidence_level: str
    model_version: str
