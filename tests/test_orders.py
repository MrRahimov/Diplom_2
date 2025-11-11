import pytest
import allure
from utils.helpers import post, get


@allure.suite("Orders API tests")
class TestOrders:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, user_token, ingredient_ids):
        r = post("/orders", json={"ingredients": ingredient_ids[:2]}, token=user_token)
        assert r.status_code in (200, 201), f"{r.status_code} {r.text}"
        body = r.json()
        assert body.get("success") is True
        assert body.get("order", {}).get("number")

    @allure.title("Получение заказов пользователя по токену")
    def test_get_user_orders(self, user_token, ingredient_ids):
        create = post("/orders", json={"ingredients": ingredient_ids[:2]}, token=user_token)
        assert create.status_code in (200, 201)

        r = get("/orders", token=user_token)
        assert r.status_code == 200, f"{r.status_code} {r.text}"
        body = r.json()
        assert body.get("success") is True
        assert len(body.get("orders", [])) > 0

    @allure.title("Создание заказа без ингредиентов (ошибка)")
    def test_create_order_with_auth_no_ingredients(self, user_token):
        r = post("/orders", json={"ingredients": []}, token=user_token)
        assert r.status_code in (400, 403), f"{r.status_code} {r.text}"
        assert r.json().get("success") is False

    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_without_auth_with_ingredients(self, ingredient_ids):
        r = post("/orders", json={"ingredients": ingredient_ids[:2]})
        if r.status_code in (200, 201):
            assert r.json().get("success") is True
        else:
            assert r.status_code in (401, 403)
            assert r.json().get("success") is False

    @allure.title("Создание заказа с невалидными ингредиентами")
    def test_create_order_with_invalid_ingredient_hash(self, user_token):
        bad = ["aaaaaaaaaaaaaaaaaaaaaaaa"]
        r = post("/orders", json={"ingredients": bad}, token=user_token)
        assert r.status_code in (400, 404, 500), f"{r.status_code} {r.text}"
        assert r.json().get("success") is False
