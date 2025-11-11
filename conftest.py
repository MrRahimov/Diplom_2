import pytest
import allure

from utils.helpers import post, delete, get
from utils.data import default_user


@pytest.fixture
def created_user():
    with allure.step("Регистрация пользователя через API"):
        user_data = default_user()
        r = post("/auth/register", json=user_data)
        assert r.status_code in (200, 201), f"Register failed: {r.text}"
        body = r.json()
        access_token = body.get("accessToken", "")
        token = access_token.split("Bearer ")[-1] if access_token else ""

    user = {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "token": token,
    }

    yield user

    if token:
        with allure.step("Удаление пользователя после теста"):
            delete("/auth/user", token=token)


@pytest.fixture
def user_token(created_user):
    return created_user["token"]


@pytest.fixture(scope="session")
def ingredient_ids():
    with allure.step("Получение списка ингредиентов"):
        r = get("/ingredients")
        assert r.status_code == 200, f"Get ingredients failed: {r.text}"
        data = r.json().get("data") or []
        ids = [i.get("_id") for i in data if i.get("_id")]

        if len(ids) < 2:
            pytest.skip("Недостаточно ингредиентов для тестов")

        return ids
