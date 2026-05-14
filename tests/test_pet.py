import requests
import allure
BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:


    @allure.title("Попытка удаления несуществующего питомца")
    def test_delete_pet_which_not_exists(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/12345")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код не совпал с ожидаемым"

        with allure.step("Проверка текста в ответе"):
            assert response.text == "Pet deleted", "Текст отличается от ожидаемого"


    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_pet_which_exists(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"}

            with allure.step("Отправка запроса на обновление несуществующего питомца"):
                response = requests.put(f"{BASE_URL}/pet/", json=payload)

            with allure.step("Проверка статуса ответ"):
                assert response.status_code == 404, "Код не совпал с ожидаемым"

            with allure.step("Проверка текста в ответе"):
                assert response.text == "Pet not found"


    @allure.title("Попытка получить данные по несуществующему питомцу")
    def test_get_data_of_pet_which_not_exists(self):

        with allure.step("Отправка запроса на получение данных несуществующего питомца"):
            response = requests.get(f"{BASE_URL}/pet/09876")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код не совпал с ожидаемым"

        with allure.step("Проверка текста в ответе"):
            assert response.text == "Pet not found", "Текст отличается от ожидаемого"
