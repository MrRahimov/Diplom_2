import requests
import allure
from typing import Optional, Dict
from .data import BASE_URL


def _auth_headers(headers: Optional[Dict] = None, token: Optional[str] = None) -> Dict:
    h = headers.copy() if headers else {}
    if token:
        if not token.startswith("Bearer "):
            token = f"Bearer {token}"
        h["Authorization"] = token
    return h


@allure.step("POST {path}")
def post(path: str, json: Optional[Dict] = None,
         headers: Optional[Dict] = None, token: Optional[str] = None):
    h = _auth_headers(headers, token)
    return requests.post(f"{BASE_URL}{path}", json=json, headers=h)


@allure.step("GET {path}")
def get(path: str, params: Optional[Dict] = None,
        headers: Optional[Dict] = None, token: Optional[str] = None):
    h = _auth_headers(headers, token)
    return requests.get(f"{BASE_URL}{path}", params=params, headers=h)


@allure.step("PATCH {path}")
def patch(path: str, json: Optional[Dict] = None,
          headers: Optional[Dict] = None, token: Optional[str] = None):
    h = _auth_headers(headers, token)
    return requests.patch(f"{BASE_URL}{path}", json=json, headers=h)


@allure.step("DELETE {path}")
def delete(path: str, headers: Optional[Dict] = None, token: Optional[str] = None):
    h = _auth_headers(headers, token)
    return requests.delete(f"{BASE_URL}{path}", headers=h)
