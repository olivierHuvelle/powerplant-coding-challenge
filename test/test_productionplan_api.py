import os
import json
from fastapi.testclient import TestClient
from main import app

IN_DOCKER = os.getenv('IN_DOCKER', 'false').lower() == 'true'

if IN_DOCKER:
    PAYLOAD_FILE = '/app/example/payload3.json'
    EXPECTED_RESPONSE_FILE = '/app/example/response3.json'
else:
    PAYLOAD_FILE = os.path.join(os.path.dirname(__file__), '../example/payload3.json')
    EXPECTED_RESPONSE_FILE = os.path.join(os.path.dirname(__file__), '../example/response3.json')


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def test_production_plan_endpoint():
    client = TestClient(app)

    payload = read_json_file(PAYLOAD_FILE)
    expected_response = read_json_file(EXPECTED_RESPONSE_FILE)

    response = client.post('/productionplan', json=payload)

    assert response.status_code == 200
    assert response.json() == expected_response
