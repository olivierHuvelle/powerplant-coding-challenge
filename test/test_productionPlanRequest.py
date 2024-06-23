import pytest
from pydantic import ValidationError
from models.ProductionPlanRequest import ProductionPlanRequest


@pytest.fixture
def generate_valid_plan_request():
    return {
        "load": 910,
        "fuels":
            {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 60
            },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
            },
            {
                "name": "gasfiredbig2",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
            },
            {
                "name": "gasfiredsomewhatsmaller",
                "type": "gasfired",
                "efficiency": 0.37,
                "pmin": 40,
                "pmax": 210
            },
            {
                "name": "tj1",
                "type": "turbojet",
                "efficiency": 0.3,
                "pmin": 0,
                "pmax": 16
            },
            {
                "name": "windpark1",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 150
            },
            {
                "name": "windpark2",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 36
            }
        ]
    }


def test_production_plan_request_valid(generate_valid_plan_request):
    try:
        ProductionPlanRequest(**generate_valid_plan_request)
    except ValidationError as e:
        pytest.fail(f"Unexpected ValidationError: {e}")


def test_production_plan_request_invalid():
    """
        This is an incomplete way to check validation BUT
            - we do not need to test pydantic package
            - we just want to check if our validation rules are applied
        Thus I only check if number of errors is the number expected
    """
    invalid_data = {
        "load": -100,  # Invalid load value
        "fuels": {
            "gas(euro/MWh)": -2,  # invalid gaz value
            "kerosine(euro/MWh)": 'a',  # invalid kerosine value
            "wind(%)": 101  # invalid wind value
            # "co2(euro/ton)" missing value
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 1.1,  # invalid efficiency
                "pmin": 100,
                "pmax": 460
            },
            {
                "name": "gasfiredbig2",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 50  # Invalid pmax less than pmin
            },
            {
                "name": "",  # invalid name
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 200
            },
            {
                "name": "gasfiredbig1",
                "type": "invalid",  # invalid type
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
            }
        ]
    }

    with pytest.raises(ValidationError) as exc_info:
        ProductionPlanRequest(**invalid_data)

    errors = exc_info.value.errors()
    assert (len(errors) == 9)


if __name__ == "__main__":
    pytest.main()
