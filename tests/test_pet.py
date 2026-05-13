import requests
import allure
BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:

    @allure.title("Попытка удаления несуществующего питомца")
    def test_delete_pet_which_not_exists(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/12345")

        with allure.step("Проверка статуса ответ"):
            assert response.status_code == 200, "Код не совпал с ожидаемым"

        with allure.step("Проверка текста в ответе"):
            assert response.text == "Pet deleted", "Текст отличается от ожидаемого"