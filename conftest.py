import requests
import pytest
from helpers.register_new_courier import generate_courier_data

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@pytest.fixture
def setup_courier():
    courier_data = generate_courier_data()
    response = requests.post(f"{BASE_URL}/courier", json=courier_data)
    return courier_data
