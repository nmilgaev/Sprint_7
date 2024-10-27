import requests
import pytest
import allure
from allure import suite

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@allure.epic("API тесты для заказов")
@suite("Список заказов")
class TestOrderList:

    @allure.title("Получение списка заказов")
    def test_get_orders(self):
        with allure.step("Отправка запроса на получение списка заказов"):
            response = requests.get(f"{BASE_URL}/orders")

        response_data = response.json()

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"
        assert "orders" in response_data, "Ответ должен содержать ключ 'orders'"
