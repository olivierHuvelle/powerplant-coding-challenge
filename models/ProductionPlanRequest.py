from fastapi import HTTPException
from pydantic import BaseModel, Field, conlist, model_validator
from enum import Enum
from typing import Dict, Callable, List
from models.ProductionPlanResponse import ProductPlanResponseItem


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

    def calculate_cost_per_mwh(self) -> float:
        # [IMP] if CO2 taken into account : just edit this method or add another method to manage co2 costs
        cost_mapper: Dict[PlantTypeEnum, Callable[[Fuel], float]] = {
            PlantTypeEnum.gasfired: lambda f: f.gas,
            PlantTypeEnum.turbojet: lambda f: f.kerosine,
            PlantTypeEnum.windturbine: lambda _: 0
        }

        if self.type not in cost_mapper:
            raise ValueError("Invalid plant type")

        cost_of_energy = cost_mapper[self.type](self.fuels)
        return 1 / self.efficiency * cost_of_energy

    @property
    def cost_per_mwh_produced(self) -> float:
        return self.calculate_cost_per_mwh()

    def set_fuels(self, fuel_data: Fuel):
        self.fuels = fuel_data

    def calculate_potential_power(self) -> float:
        """Calculate the potential pmax produced by the power_plant according to its type"""
        potential_power = self.pmax * (self.fuels.wind / 100) if self.type == PlantTypeEnum.windturbine else self.pmax
        return round(potential_power, 1)


class ProductionPlanRequest(BaseModel):
    load: int = Field(gt=0, description='Load in MWh')
    fuels: Fuel = Field(..., description='Fuels data')
    power_plants: conlist(PowerPlant, min_length=1) = Field(..., alias='powerplants', description="List of power plants")

    def _calculate_merit_order(self) -> List[PowerPlant]:
        """  returns the list of power_plants ordered by merit_order descending """
        for power_plant in self.power_plants:
            power_plant.set_fuels(self.fuels)
        return sorted(self.power_plants, key=lambda plant: plant.cost_per_mwh_produced)

    def generate_response(self) -> List[ProductPlanResponseItem]:
        remaining_payload = self.load
        power_plants_by_merit_order_desc = self._calculate_merit_order()
        response_items: List[ProductPlanResponseItem] = []

        """
            loop on power_plant by merit_order (per cost_per_mwh ascending) i.e cheap -> extensive to produce
            on each power_plant : get potentiel_power (i.e pmax with some adjustement ex wind)
            if potential_power is < remaining_payload then take full power and process next, if < remaining_payload then check according to pmin constraint
            BEWARE if potential_power is 0.0 AND pmin > 0 AND  remaining_payload != 0.0 => we can have a suboptimal solution

            an alternative would be to "bruteforce" but the complexity is huge, even with numpy it's not guaranteed ... see commented code below
            another alternative would be to detect such cases (see condition supra) if condition is met 
                then reduce power of the last power_plant which p was its pmax and invest the difference to next power_plant to reach its pmin
                it would probably resolve some cases but not guaranteed to get the optimal solution 
            
            In practice, a larger dataset would be needed to know whether or not this problem is encountered frequently 
            AND if the impact of this problem is significant (financial, other). 
        """
        for power_plant in power_plants_by_merit_order_desc:
            potential_power = power_plant.calculate_potential_power()
            if potential_power > remaining_payload:
                potential_power = round(remaining_payload, 1) if potential_power >= power_plant.pmin else 0.0

            response_items.append(ProductPlanResponseItem(name=power_plant.name, p=potential_power))
            remaining_payload -= potential_power

        total_allocated_power = sum(item.p for item in response_items)
        if total_allocated_power != self.load:
            raise HTTPException(status_code=422,detail='No combinaison found')
        return response_items

        #BRUTEFORCE algo which complexity is way to high, just for example : use numpy for performances
        #     power_combinations = []
        #     for power_plant in power_plants_by_merit_order_desc:
        #         p_range = np.arange(power_plant.pmin, power_plant.pmax + 0.1, 0.1)
        #         power_combinations.append(p_range)
        #
        #     # Initialize the iterator for combinations
        #     combination_iterator = product(*power_combinations)
        #
        #     min_cost_combination = None
        #     min_cost = np.inf
        #
        #     for combination in combination_iterator:
        #         if np.round(np.sum(combination), 1) == self.load:
        #             total_cost = np.sum(
        #                 np.array(combination) * np.array(
        #                     [plant.cost_per_mwh_produced for plant in power_plants_by_merit_order_desc])
        #             )
        #             if total_cost < min_cost:
        #                 min_cost = total_cost
        #                 min_cost_combination = combination
        #
        #     response_items = []
        #     for power, plant in zip(min_cost_combination, power_plants_by_merit_order_desc):
        #         response_items.append(ProductPlanResponseItem(name=plant.name, p=power))

