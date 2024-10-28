import requests
import pytest
import allure
from helpers.register_new_courier import generate_courier_data

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


@allure.epic("API тесты для курьеров")
@allure.suite("Создание курьера")
class TestCourierCreation:

    @allure.title("Создание курьера: успешный случай")
    def test_create_courier_success(self):
        courier_data = generate_courier_data()

        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(f"{BASE_URL}/courier", json=courier_data)

        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}. Ответ: {response.text}"
        assert response.json().get("ok") is True, "Ожидался ответ {'ok': true}"

    @allure.title("Создание курьера: попытка создать дубликат")
    def test_create_duplicate_courier(self):
        courier_data = generate_courier_data()

        requests.post(f"{BASE_URL}/courier", json=courier_data)  # Создаем первого курьера
        with allure.step("Отправка запроса на создание дубликата курьера"):
            response_second = requests.post(f"{BASE_URL}/courier", json=courier_data)

        assert response_second.status_code == 409, f"Ожидался код 409, получен {response_second.status_code}. Ответ: {response_second.text}"
        assert response_second.json().get(
            "message") == "Этот логин уже используется. Попробуйте другой.", "Ожидалось сообщение об ошибке дублирования логина"

    @pytest.mark.parametrize("field", ["login", "password"])
    @allure.title("Создание курьера: отсутствие обязательного поля")
    def test_create_courier_missing_field(self, field):
        courier_data = generate_courier_data()
        courier_data_dict = courier_data.copy()
        courier_data_dict.pop(field)

        with allure.step(f"Отправка запроса на создание курьера без поля: {field}"):
            response = requests.post(f"{BASE_URL}/courier", json=courier_data_dict)

        assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}. Ответ: {response.text}"
        assert response.json().get(
            "message") == "Недостаточно данных для создания учетной записи", "Ожидалось сообщение об ошибке отсутствия поля"
