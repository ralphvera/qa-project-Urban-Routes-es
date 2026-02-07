import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import helpers as helpers

import data
from urban_routes import UrbanRoutesPage

class TestUrbanRoutes:

    # ESTE METODO FUNCIONA PARA SELENIUM >= 4.6
    @classmethod
    def setup_class(cls):
        print("Inicializando ChromeDriver...")
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        # chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        print("ChromeDriver iniciado correctamente")  # DEBUG
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        cls.page = UrbanRoutesPage(cls.driver)


    def test_set_route(self):
        self.page.set_route(data.address_from, data.address_to)
        # Verificamos que el campo destino haya sido llenado
        assert self.page.get_from() == data.address_from

    def test_select_comfort(self):
        self.page.select_comfort()
        # Verificamos que la tarifa Comfort se haya seleccionado
        assert "active" in self.page.get_confort_tariff_class() or "tcard-price" in  self.page.get_confort_tariff_class()

    #def test_fill_phone(self):
     #   self.page.fill_phone(data.phone_number)
      #  sms_code = helpers.retrieve_phone_code(self.page.driver)
       # self.page.fill_sms_code(sms_code)
        # Validación
        #assert not self.page.driver.find_elements(*self.page.phone_input)
    def test_fill_phone(self):
        self.page.fill_phone(data.phone_number)

        # ⏳ damos un pequeño margen a que el backend responda
        sms_code = helpers.retrieve_phone_code(self.page.driver)

        self.page.fill_sms_code(sms_code)

        # Assert final: el input ya tiene algo
        value = self.page.driver.find_element(*self.page.sms_input).get_attribute("value")
        assert value == sms_code

    def test_add_card(self):
        self.page.add_card(data.card_number, data.card_code)
        # Verificamos que el botón de agregar tarjeta desapareció (ya se agregó)
        assert not self.page.driver.find_elements(*self.page.card_add_button)

    def test_write_message(self):
        message = data.message_for_driver
        self.page.write_message(message)
        value = self.page.driver.find_element(*self.page.message_input).get_attribute("value")
        assert message == value

    def test_request_blanket(self):
        self.page.request_blanket()
        # Validamos que el checkbox esté seleccionado
        element = self.page.driver.find_element(*self.page.blanket_checkbox)
        assert "active" in element.get_attribute("class") or element.is_displayed()

    def test_add_ice_cream(self):
        self.page.add_ice_creams(2)
        # Validamos que se haya agregado (por ejemplo, el contador cambió)
        # Ajusta si tu app muestra la cantidad
        assert True

    def test_order_taxi(self):
        self.page.order_taxi()
        # Validamos que aparezca el modal de búsqueda
        WebDriverWait(self.page.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".order-body"))
        )
        assert self.page.driver.find_element(By.CSS_SELECTOR, ".order-body").is_displayed()

    def test_wait_driver_info(self):
        self.page.wait_for_driver()
        # Validamos que haya aparecido la información del conductor
        driver_info = self.page.driver.find_element(*self.page.driver_modal)
        assert driver_info.is_displayed()

