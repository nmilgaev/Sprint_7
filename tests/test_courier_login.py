import requests
import pytest
import allure
from helpers.register_new_courier import generate_courier_data

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@allure.epic("API тесты для курьеров")
@allure.suite("Логин курьера")
class TestCourierLogin:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.courier_data = generate_courier_data()
        response = requests.post(f"{BASE_URL}/courier", json=self.courier_data)
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}. Ответ: {response.text}"

    @allure.title("Логин курьера: успешный случай")
    def test_login_success(self):
        login_data = {
            "login": self.courier_data["login"],
            "password": self.courier_data["password"]
        }

        with allure.step("Отправка запроса на авторизацию курьера"):
            response = requests.post(f"{BASE_URL}/courier/login", json=login_data)

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"
        assert "id" in response.json(), "Ожидался ответ с id курьера"

    @pytest.mark.parametrize("field", ["login", "password"])
    @allure.title("Логин курьера: отсутствие обязательного поля")
    def test_login_missing_field(self, field):
        login_data = {
            "login": self.courier_data["login"],
            "password": self.courier_data["password"]
        }
        login_data.pop(field)

        with allure.step(f"Отправка запроса на авторизацию без поля: {field}"):
            response = requests.post(f"{BASE_URL}/courier/login", json=login_data)

        assert response.status_code in {400, 504}, f"Ожидался код 400 или 504, получен {response.status_code}. Ответ: {response.text}"

    @allure.title("Логин курьера: неверные учетные данные")
    def test_login_with_invalid_credentials(self):
        invalid_login_data = {
            "login": "logintest22",
            "password": "invalid_password"
        }
        with allure.step("Отправка запроса на авторизацию с неверными учетными данными"):
            response = requests.post(f"{BASE_URL}/courier/login", json=invalid_login_data)

        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}. Ответ: {response.text}"
        assert response.json().get("message") == "Учетная запись не найдена", "Ожидалось сообщение об ошибке, что учетная запись не найдена"

    @allure.title("Логин курьера: несуществующий пользователь")
    def test_login_nonexistent_user(self):
        nonexistent_user_data = {
            "login": "nonexistent_login",
            "password": "some_password"
        }
        with allure.step("Отправка запроса на авторизацию несуществующего пользователя"):
            response = requests.post(f"{BASE_URL}/courier/login", json=nonexistent_user_data)

        assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}. Ответ: {response.text}"
        assert response.json().get("message") == "Учетная запись не найдена", "Ожидалось сообщение об ошибке, что учетная запись не найдена"