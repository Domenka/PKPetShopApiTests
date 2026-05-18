import requests
import allure
from .schemas.pet_schema import PET_SCHEMA
import jsonschema
import pytest

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


    @allure.title("Добавление нового питомца")
    def test_add_new_pet(self):
        with allure.step("Подготовка данных по отправке"):
            payload = {"id": 1,
                       "name": "Buddy",
                       "status": "available"}

        with allure.step("Отправка запроса на создание нового питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "name питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "status питомца не совпадает с ожидаемым"


    @allure.title("Добавление нового питомца c полными данными")
    def test_add_new_pet_with_full_data(self):
        with allure.step("Подготовка данных по отправке"):
            payload = {"id": 10,
                       "name": "doggie",
                       "category": {"id": 1, "name": "Dogs"},
                       "photoUrls": ["string"],
                       "tags": [{"id": 0, "name": "string"}],
                       "status": "available"}

        with allure.step("Отправка запроса на создание нового питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "name питомца не совпадает с ожидаемым"
            assert response_json["category"] == payload["category"], "category питомца не совпадает с ожидаемым"
            assert response_json["photoUrls"] == payload["photoUrls"], "photoUrls питомца не совпадает с ожидаемым"
            assert response_json["tags"] == payload["tags"], "tags питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "status питомца не совпадает с ожидаемым"


    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_info_by_id(self, create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение данных питомца по id"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код не совпал с ожидаемым"
            assert response.json()["id"] == pet_id


    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet["id"]

            with allure.step("Отправка запроса на удаление питомца по id"):
                response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
            with allure.step("Проверка статуса ответа"):
                assert response.status_code == 200, "Код не совпал с ожидаемым"

            with allure.step("Отправка запроса на получение данных питомца по id"):
                response2 = requests.get(f"{BASE_URL}/pet/{pet_id}")
            with allure.step("Проверка статуса ответа"):
                assert response2.status_code == 404, "Код не совпал с ожидаемым"


    @allure.title("Обновление информации о питомце")
    def test_update_pet_data_by_id(self, create_pet):
        with allure.step("Получение id созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления"):
            payload = {"id": pet_id,
                       "name": "Buddy Updated",
                       "status": "sold"}

        with allure.step("Отправка запроса на обновление данных питомца"):
            response = requests.put(f"{BASE_URL}/pet/", json=payload)
            response_json = response.json()

        with allure.step("Проверка статус кода после обновления"):
            assert response.status_code == 200, "Код не совпал с ожидаемым"

        with allure.step("Проверка обновленных данных"):
            assert response_json["id"] == payload["id"]
            assert response_json["name"] == payload["name"]
            assert response_json["status"] == payload["status"]


    @allure.title("Получение списка питомцев по существующему статусу")
    @pytest.mark.parametrize(
        "status, excpected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200)

        ]

    )
    def test_get_pet_list_by_exist_status(self, status, excpected_status_code):
        with allure.step(f"Отправка запроса на получение данных питомца по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса и формата данных"):
            assert response.status_code == excpected_status_code
        with allure.step("Проверка формата данных"):
            assert isinstance(response.json(), list)


    @allure.title("Получение списка питомцев по несуществующему статусу")
    @pytest.mark.parametrize(
        "status, excpected_status_code",
        [
            ("reserved", 400)
        ]
    )
    def test_get_pet_list_by_not_exist_status(self, status, excpected_status_code):
        with allure.step(f"Отправка запроса на получение данных питомца по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статус кода"):
            assert response.status_code == excpected_status_code
        with allure.step("Проверка текста ошибки"): #мне кажется в данном кейсе достаточно проверить текст ошибки в ответе
            assert response.text == '{"code":400,"message":"Input error: query parameter `status value `reserved` is not in the allowable values `[available, pending, sold]`"}'


    @allure.title("Получение списка питомцев по пустому статусу")
    @pytest.mark.parametrize(
        "status, excpected_status_code",
        [
            (None, 400)
        ]
    )
    def test_get_pet_list_by_empty_status(self, status, excpected_status_code):
        with allure.step(f"Отправка запроса на получение данных питомца по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статус кода"):
            assert response.status_code == excpected_status_code
        with allure.step("Проверка текста ошибки"): #мне кажется в данном кейсе достаточно проверить текст ошибки в ответе
            assert response.text == 'No status provided. Try again?'
