# Diplom_2

## Как запустить тесты
1. Установить зависимости:
pip install -r requirements.txt
2. Запустить тесты с формированием Allure-отчёта:
pytest -s --alluredir=allure-results
3. Сгенерировать и открыть отчёт:
allure serve allure-results
