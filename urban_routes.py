from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- Localizadores ---
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")
    comfort_tariff_button = (By.XPATH, "//div[@class='tariff-card' and text()='Comfort']")
    phone_button = (By.CSS_SELECTOR, ".np-button")
    phone_input = (By.ID, "phone")
    phone_submit = (By.CSS_SELECTOR, "button.submit")
    card_add_button = (By.CSS_SELECTOR, "button.add-card")
    card_number_input = (By.ID, "number")
    card_code_input = (By.ID, "code")
    card_link_button = (By.CSS_SELECTOR, "button.link")
    message_input = (By.ID, "comment")
    blanket_checkbox = (By.XPATH, "//div[text()='Blanket and handkerchiefs']")
    ice_cream_plus_button = (By.XPATH, "//div[text()='Ice cream']/following-sibling::div//button[contains(@class,'plus')]")
    order_button = (By.CSS_SELECTOR, "button.smart-button")
    driver_modal = (By.CSS_SELECTOR, ".order-body .driver-info")

    # --- Métodos ---
    def set_route(self, origin, destination):
        self.driver.find_element(*self.from_field).send_keys(origin)
        self.driver.find_element(*self.to_field).send_keys(destination)
        # Simula que presiona enter para confirmar
        self.driver.find_element(*self.to_field).send_keys(Keys.ENTER)

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff_button).click()

    def fill_phone_number(self, number):
        self.driver.find_element(*self.phone_button).click()
        self.driver.find_element(*self.phone_input).send_keys(number)
        self.driver.find_element(*self.phone_submit).click()

    def add_card(self, number, cvv):
        self.driver.find_element(*self.card_add_button).click()
        self.driver.find_element(*self.card_number_input).send_keys(number)
        code_field = self.driver.find_element(*self.card_code_input)
        code_field.send_keys(cvv)
        # Forzar pérdida de foco
        code_field.send_keys(Keys.TAB)
        self.driver.find_element(*self.card_link_button).click()

    def write_message(self, message):
        self.driver.find_element(*self.message_input).send_keys(message)

    def request_blanket(self):
        self.driver.find_element(*self.blanket_checkbox).click()

    def add_ice_creams(self, qty=2):
        btn = self.driver.find_element(*self.ice_cream_plus_button)
        for _ in range(qty):
            btn.click()

    def order_taxi(self):
        self.driver.find_element(*self.order_button).click()

    def wait_for_driver(self):
        self.wait.until(EC.visibility_of_element_located(self.driver_modal))
