from pydantic import BaseModel, Field, field_serializer


class ProductPlanResponseItem(BaseModel):
    name: str = Field(..., description='Name of the power plant')
    p: float = Field(..., ge=0.0, description='Power output in MWh')

    @field_serializer('p')
    def serialize_dt(self, p: float, _info):
        return float(f'{p:.1f}')
