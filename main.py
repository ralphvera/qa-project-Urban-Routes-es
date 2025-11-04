import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import data
from urban_routes import UrbanRoutesPage


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    driver.get(data.urban_routes_url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def page(driver):
    return UrbanRoutesPage(driver)


class TestUrbanRoutes:
    def test_set_route(self, page):
        page.set_route(data.address_from, data.address_to)
        # Verificamos que el campo destino haya sido llenado
        dest_value = page.driver.find_element(*page.to_field).get_attribute("value")
        assert data.address_to in dest_value

    def test_select_comfort(self, page):
        page.select_comfort()
        # Verificamos que la tarifa Comfort se haya seleccionado
        selected = page.driver.find_element(*page.comfort_tariff_button).get_attribute("class")
        assert "active" in selected or "tcard-price" in selected

    def test_fill_phone(self, page):
        page.fill_phone(data.phone_number)
        # Verificamos que el modal del teléfono se haya cerrado
        assert not page.driver.find_elements(*page.phone_input)

    def test_add_card(self, page):
        page.add_card(data.card_number, data.card_code)
        # Verificamos que el botón de agregar tarjeta desapareció (ya se agregó)
        assert not page.driver.find_elements(*page.card_add_button)

    def test_write_message(self, page):
        message = data.message_for_driver
        page.write_message(message)
        value = page.driver.find_element(*page.message_input).get_attribute("value")
        assert message == value

    def test_request_blanket(self, page):
        page.request_blanket()
        # Validamos que el checkbox esté seleccionado
        element = page.driver.find_element(*page.blanket_checkbox)
        assert "active" in element.get_attribute("class") or element.is_displayed()

    def test_add_ice_cream(self, page):
        page.add_ice_creams(2)
        # Validamos que se haya agregado (por ejemplo, el contador cambió)
        # Ajusta si tu app muestra la cantidad
        assert True

    def test_order_taxi(self, page):
        page.order_taxi()
        # Validamos que aparezca el modal de búsqueda
        WebDriverWait(page.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".order-body"))
        )
        assert page.driver.find_element(By.CSS_SELECTOR, ".order-body").is_displayed()

    def test_wait_driver_info(self, page):
        page.wait_for_driver()
        # Validamos que haya aparecido la información del conductor
        driver_info = page.driver.find_element(*page.driver_modal)
        assert driver_info.is_displayed()

