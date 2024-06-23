# Problem description 
[source](https://github.com/gem-spaas/powerplant-coding-challenge/tree/master)

# Acceptance criteria
## FROM RH email
Il est important que tu respectes les bonnes pratiques de développement (notamment basé sur les principes SOLID) dans l'implémentation de ton coding challenge:
- Un code fonctionnel et testé (unit testing et test fonctionnel)
- Un code lisible et commenté
- Un naming intelligent et cohérent des variables et méthodes
- Un code où le code n'est pas dupliqué
- etc....

## FROM challenge itself 
- For calculating the unit-commitment, we prefer you not to rely on an existing (linear-programming) solver
- Implementations can be submitted in either C# (on .Net 5 or higher) or Python (3.8 or higher)
- Python implementations should contain a requirements.txt or a pyproject.toml (for use with poetry) to install all needed dependencies.
- The power produced by each powerplant has to be a multiple of 0.1 Mw and the sum of the power produced by all the powerplants together should equal the load.
- contain a README.md explaining how to build and launch the API
- expose the API on port 8888
- manage error logs 

- BONUS
  - Provide a Dockerfile along with the implementation to allow deploying your solution quickly.
  - Taken into account that a gas-fired powerplant also emits CO2,


# Problem analysis 
Build a REST API exposing an endpoint /productionplan that accepts a POST of which the body contains a payload as you can find in the example_payloads directory and that returns a json with the same structure as in example_response.json and that manages and logs run-time errors.
The payload contains 3 types of data:

**INPUT**

- load: 
  - The load is the amount of energy (MWh) that need to be generated during one hour.
  fuels: 
  - based on the cost of the fuels of each powerplant
    - the merit-order can be determined which is the starting point for deciding which powerplants should be switched on and how much power they will deliver. Wind-turbine are either switched-on, and in that case generate a certain amount of energy depending on the % of wind, or can be switched off.
        - gas(euro/MWh): the price of gas per MWh. Thus if gas is at 6 euro/MWh and if the efficiency of the powerplant is 50% (i.e. 2 units of gas will generate one unit of electricity), the cost of generating 1 MWh is 12 euro.
        - kerosine(euro/Mwh): the price of kerosine per MWh.
        - co2(euro/ton): the price of emission allowances (optionally to be taken into account).
        - wind(%): percentage of wind. Example: if there is on average 25% wind during an hour, a wind-turbine with a Pmax of 4 MW will generate 1MWh of energy.
    - powerplants: describes the powerplants at disposal to generate the demanded load. For each powerplant is specified:
        - name:
        - type: gasfired, turbojet or windturbine.
        - efficiency: the efficiency at which they convert a MWh of fuel into a MWh of electrical energy. Wind-turbines do not consume 'fuel' and thus are considered to generate power at zero price.
        - pmax: the maximum amount of power the powerplant can generate.
        - pmin: the minimum amount of power the powerplant generates when switched on.

**OUTPUT**

The response should be a json as in example_payloads/response3.json, which is the expected answer for example_payloads/payload3.json, specifying for each powerplant how much power each powerplant should deliver. The power produced by each powerplant has to be a multiple of 0.1 Mw and the sum of the power produced by all the powerplants together should equal the load.

# TODOS 
    - project setup (requirements.txt, instructions, README, port, error log management, gitignore)
      - gitgnore: ok 
      - context.md : ok (problem analysis)
      - requirements.txt : ok : some packages will be added later such as pytest
      - port : ok 
      - README.md regarding installation : ok 
      - error log management : Logger - Error handler fastapi : ok   
    - input validation (pydantic model) + testing 
      - pydantic model definitions : ok 
      - log the validation errors : ok 
      - test validation rules : ok 
      - update requirements.txt and context.md : ok   
    - classes management 
        - Fuel  : ok 
        - PowerPlant : ok 
        - ProductionPlanRequest : ok  
        - ProductPlanResponseItem : ok 
        - Test solution based on provided example (json file)  
    - extra (if time) 
        - dockerize (as it is the fastest to implement) : dont forget to update README.md 
        - add CO2 to processor and model as optional parameter in input  

# IMPROVEMENTS 
  - Logger : create an env (arg) -> dedicated class -> dependency injection , then test Logger in test mode + pretty print 
  - Add a git hook to check formatting PEP (pre-commit) and run all tests (pre-push)
  - Add a uniqueness constraint check on powerplants and other subfields from the payload 
