from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
import time

# --- Clase con localizadores y métodos de la página ---
class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Localizadores de ejemplo — ajusta según los valores reales
        self.from_input = (By.ID, "from")
        self.to_input = (By.ID, "to")
        self.comfort_tariff = (By.XPATH, "//div[contains(text(), 'Comfort')]")
        self.phone_field = (By.CSS_SELECTOR, "input[name='phone']")
        self.next_button = (By.XPATH, "//button[contains(text(),'Siguiente')]")
        self.card_button = (By.XPATH, "//button[contains(text(),'Agregar tarjeta')]")
        self.card_number = (By.ID, "number")
        self.card_code = (By.ID, "code")
        self.card_add_button = (By.XPATH, "//button[contains(text(),'Link')]")
        self.message_field = (By.CSS_SELECTOR, "textarea[name='message']")
        self.blanket_checkbox = (By.XPATH, "//label[contains(text(),'Manta')]")
        self.tissues_checkbox = (By.XPATH, "//label[contains(text(),'Pañuelos')]")
        self.icecream_plus = (By.XPATH, "//button[@data-item='icecream']//following-sibling::button[contains(text(),'+')]")
        self.order_button = (By.XPATH, "//button[contains(text(),'Pedir taxi')]")
        self.search_modal = (By.ID, "searching-modal")
        self.driver_modal = (By.ID, "driver-info")

    def set_route(self, from_address, to_address):
        self.wait.until(EC.visibility_of_element_located(self.from_input)).send_keys(from_address)
        self.wait.until(EC.visibility_of_element_located(self.to_input)).send_keys(to_address + Keys.ENTER)

    def select_comfort(self):
        self.wait.until(EC.element_to_be_clickable(self.comfort_tariff)).click()

    def fill_phone(self, phone):
        field = self.wait.until(EC.visibility_of_element_located(self.phone_field))
        field.clear()
        field.send_keys(phone)
        self.wait.until(EC.element_to_be_clickable(self.next_button)).click()

    def add_card(self, number, cvv):
        self.wait.until(EC.element_to_be_clickable(self.card_button)).click()
        self.wait.until(EC.visibility_of_element_located(self.card_number)).send_keys(number)
        code_field = self.wait.until(EC.visibility_of_element_located(self.card_code))
        code_field.send_keys(cvv)
        # Simular pérdida de foco (importante para habilitar el botón 'link')
        code_field.send_keys(Keys.TAB)
        # Esperar y hacer clic en el botón de vincular
        self.wait.until(EC.element_to_be_clickable(self.card_add_button)).click()

    def write_message(self, text):
        self.wait.until(EC.visibility_of_element_located(self.message_field)).send_keys(text)

    def request_blanket_and_tissues(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_checkbox)).click()
        self.wait.until(EC.element_to_be_clickable(self.tissues_checkbox)).click()

    def request_icecreams(self, amount=2):
        plus_button = self.wait.until(EC.element_to_be_clickable(self.icecream_plus))
        for _ in range(amount):
            plus_button.click()

    def order_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.order_button)).click()

    def wait_for_driver(self):
        # Esperar a que el modal de búsqueda aparezca y luego cambie al del conductor
        self.wait.until(EC.visibility_of_element_located(self.search_modal))
        self.wait.until(EC.visibility_of_element_located(self.driver_modal))


# --- Clase de pruebas automatizadas ---
class TestUrbanRoutes:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.get(data.urban_routes_url)  # cambia por la URL real
        self.page = UrbanRoutesPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_request_taxi_flow(self):
        self.page.set_route("Av. Insurgentes 300", "Zócalo CDMX")

    def test_select_comfor(self):
        self.page.select_comfort()
        selected = self.driver.find_element(*self.page.comfort_tariff).get_attribute("class")
        assert "active" in selected, "No se seleccionó la tarifa de comfort correctamente."

    def test_fill_phone(self):
        self.page.fill_phone("5555555555")
        value = self.driver.find_element(*self.page.phone_field).get_attribute("value")
        assert value == "5555555555", "El número de teléfono no se ingresó correctamente."

    def test_add_credit_card(self):
        self.page.add_card("4111111111111111", "123")
        assert True, "Se agregó la tarjeta."

    def test_write_message(self):
        message = "Por favor, venga despacio, llevo equipaje."
        self.page.write_message(message)
        value = self.driver.find_element(*self.page.message_field).get_attribute("value")
        assert message in value, "El mensaje no se escribió correctamente."

    def 
        self.page.request_blanket_and_tissues()
        self.page.request_icecreams(2)
        self.page.order_taxi()
        self.page.wait_for_driver()  # opcional

        print("Prueba completada exitosamente: se simuló el flujo completo de pedir un taxi.")


