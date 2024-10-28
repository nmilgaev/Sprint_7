import requests
import pytest
import allure

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@allure.epic("API тесты для заказов")
@allure.suite("Создание заказа")
class TestOrderCreation:

    @pytest.mark.parametrize("colors, expected_status, expected_response", [
        (["BLACK"], 201, "track"),  # Один цвет
        (["GREY"], 201, "track"),   # Другой цвет
        (["BLACK", "GREY"], 201, "track"),  # Оба цвета
        ([], 201, "track")  # Без указания цвета
    ])
    @allure.title("Создание заказа: разные варианты цветов")
    def test_create_order(self, colors, expected_status, expected_response):
        order_data = {
            "firstName": "Nikita",
            "lastName": "Milgaev",
            "address": "Test, 142 d.",
            "metroStation": 4,
            "phone": "+7 800 555 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-10-27",
            "comment": "Test",
            "color": colors
        }

        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(f"{BASE_URL}/orders", json=order_data)

        assert response.status_code == expected_status, f"Ожидался код {expected_status}, получен {response.status_code}. Ответ: {response.text}"
        assert expected_response in response.json(), f"Ожидалось наличие {expected_response} в ответе. Ответ: {response.json()}"
