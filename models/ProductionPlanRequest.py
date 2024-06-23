from pydantic import BaseModel, Field, conlist, model_validator
from enum import Enum


class Fuel(BaseModel):
    gas: float = Field(alias='gas(euro/MWh)', gt=0.0, description='Gas cost in euro per MWh')
    kerosine: float = Field(alias='kerosine(euro/MWh)', gt=0.0, description='Kerosine cost in euro per MWh')
    co2: float = Field(alias='co2(euro/ton)', gt=0.0, description='CO2 cost in euro per ton')
    wind: float = Field(alias='wind(%)', ge=0.0, le=100.0, description='Percentage (in percent) of wind')


class PlantTypeEnum(str, Enum):
    gasfired = "gasfired"
    turbojet = "turbojet"
    windturbine = "windturbine"


class PowerPlant(BaseModel):
    name: str = Field(min_length=1)
    type: PlantTypeEnum
    efficiency: float = Field(ge=0.0, le=1.0, description="Efficiency of the power plant from 0.0 to 1.0")
    pmin: int = Field(ge=0, description="Minimum power output of the plant in MWh")
    pmax: int = Field(ge=0, description="Maximum power output of the plant in MWh")
    fuels: Fuel = Field(None, exclude=True)

    @model_validator(mode='before')
    def pmax_must_be_greater_than_pmin(cls, values):
        if 'pmin' in values and values.get('pmax') < values['pmin']:
            raise ValueError('pmax must be greater than or equal to pmin')
        return values

    def set_fuels(self, fuel_data: Fuel):
        self.fuels = fuel_data


class ProductionPlanRequest(BaseModel):
    load: int = Field(gt=0, description='Load in MWh')
    fuels: Fuel = Field(..., description='Fuels data')
    power_plants: conlist(PowerPlant, min_length=1) = Field(..., alias='powerplants', description="List of power plants")

