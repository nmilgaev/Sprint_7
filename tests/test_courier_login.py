import requests
import allure
import pytest

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@allure.epic("API тесты для курьеров")
@allure.suite("Логин курьера")
class TestCourierLogin:

    @allure.title("Логин курьера: успешный случай")
    def test_login_success(self, setup_courier):
        login_data = {
            "login": setup_courier["login"],
            "password": setup_courier["password"]
        }

        with allure.step("Отправка запроса на авторизацию курьера"):
            response = requests.post(f"{BASE_URL}/courier/login", json=login_data)

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"
        assert "id" in response.json(), "Ожидался ответ с id курьера"

    @pytest.mark.parametrize("field", ["login", "password"])
    @allure.title("Логин курьера: отсутствие обязательного поля")
    def test_login_missing_field(self, setup_courier, field):
        login_data = {
            "login": setup_courier["login"],
            "password": setup_courier["password"]
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
