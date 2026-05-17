import allure
import requests
import pytest

BASE_URL = "http://5.181.109.28:9090/api/v3/store"

@allure.feature("Store")
class TestStore:

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_data_of_order_which_not_exist(self):
        with allure.step("Отправка запроса на получение данных несуществующего заказа"):
            response = requests.get(url=f"{BASE_URL}/order/9999")

        with allure.step("Проверка статуса кода 404"):
           assert response.status_code == 404, "Код не совпал с ожидаемым"

        with allure.step("Проверка статуса кода 404"):
           assert response.text == "Order not found", "Текст не совпал с ожидаемым"


    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/inventory")

        with allure.step("Проверка статуса кода 200"):
           assert response.status_code == 200, "Код не совпал с ожидаемым"

        with allure.step("Проверка соответствия ответа заданному формату"):
            assert isinstance(response.json(), dict)


    @allure.title("Размещение заказа")
    def test_create_order(self):
        with allure.step("Подготовка данных для отправки"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса на создание заказа"):
            response = requests.post(url=f"{BASE_URL}/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статус кода 200"):
            assert response.status_code == 200, "Код не совпал с ожидаемым"

        with allure.step("Проверка наличия данных в заказе"):
            assert response_json["id"] == payload["id"], "id не совпадает"
            assert response_json["petId"] == payload["petId"], "petId не совпадает"
            assert response_json["quantity"] == payload["quantity"], "quantity не совпадает"
            assert response_json["status"] == payload["status"], "status не совпадает"
            assert response_json["complete"] == payload["complete"], "complete не совпадает"


    @allure.title("Получение информации о заказе по ID")
    def test_get_order_data_by_id(self, create_order):
        order_id = create_order["id"]

        with allure.step("Отправка запроса на получение данных заказа по id"):
            response = requests.get(f"{BASE_URL}/order/{order_id}")

        with allure.step("Проверка статуса ответа 200"):
            assert response.status_code == 200, "Код не совпал с ожидаемым"
            assert response.json()["id"] == order_id


    @allure.title("Удаление заказа по ID")
    def test_get_order_data_by_id(self, create_order):
        order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа по id"):
            response = requests.delete(f"{BASE_URL}/order/{order_id}")

        with allure.step("Проверка статуса ответа 200 после операции удаления"):
            assert response.status_code == 200, "Код не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение данных удаленного заказа по id"):
             response2 = requests.get(f"{BASE_URL}/order/{order_id}")

        with allure.step("Проверка статуса ответа 404 после запроса данных по удаленному заказу"):
            assert response2.status_code == 404, "Код не совпал с ожидаемым"




