import pytest
import allure

from utils.helpers import post, patch
from utils.data import default_user


@allure.suite("Auth API tests")
class TestAuth:
    @allure.title("Регистрация нового уникального пользователя")
    def test_register_unique_user(self):
        user = default_user()
        r = post("/auth/register", json=user)
        assert r.status_code in (200, 201)
        assert r.json().get("success") is True

    @allure.title("Регистрация уже существующего пользователя")
    def test_register_existing_user(self, created_user):
        payload = {
            "email": created_user["email"],
            "password": created_user["password"],
            "name": created_user["name"],
        }
        r = post("/auth/register", json=payload)
        assert r.status_code == 403
        assert r.json().get("success") is False

    @allure.title("Регистрация с отсутствующими полями")
    @pytest.mark.parametrize("missing_key", ["email", "password", "name"])
    def test_register_missing_field(self, missing_key):
        data = default_user()
        data.pop(missing_key)
        r = post("/auth/register", json=data)
        assert r.status_code in (400, 403)
        assert r.json().get("success") is False

    @allure.title("Успешный логин")
    def test_login_ok(self, created_user):
        creds = {
            "email": created_user["email"],
            "password": created_user["password"],
        }
        r = post("/auth/login", json=creds)
        assert r.status_code == 200
        assert r.json().get("success") is True
        assert "accessToken" in r.json()

    @allure.title("Логин с неправильными данными")
    def test_login_wrong_creds(self):
        creds = {
            "email": "no_user@example.com",
            "password": "wrongpass",
        }
        r = post("/auth/login", json=creds)
        assert r.status_code in (401, 403)
        assert r.json().get("success") is False


@allure.suite("User profile API tests")
class TestUserProfile:
    @allure.title("Изменение имени авторизованного пользователя")
    def test_change_user_name_authorized(self, created_user):
        new_name = "Updated Tester"
        token = created_user["token"]

        r = patch("/auth/user", json={"name": new_name}, token=token)
        assert r.status_code == 200
        body = r.json()
        assert body.get("success") is True
        assert body.get("user", {}).get("name") == new_name

    @allure.title("Попытка изменить данные без авторизации")
    def test_change_user_data_unauthorized(self):
        r = patch("/auth/user", json={"name": "Hacker"})
        assert r.status_code in (401, 403)
        assert r.json().get("success") is False
