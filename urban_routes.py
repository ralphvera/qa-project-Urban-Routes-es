from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # --- Localizadores ---
        self.from_field = (By.ID, "from")
        self.to_field = (By.ID, "to")
        self.order_taxi = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
        self.comfort_tariff_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[3]')
        self.phone_button = (By.CSS_SELECTOR, ".np-button")
        self.phone_input = (By.ID, "phone")
        self.phone_submit = (By.CSS_SELECTOR, "#root > div > div.number-picker.open > div.modal > div.section.active > form > div.buttons > button")
        self.payment_method = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[1]')
        self.card_add_button = (By.CSS_SELECTOR, "#root > div > div.payment-picker.open > div.modal > div.section.active > div.pp-selector > div.pp-row.disabled > div.pp-title")
        self.card_number_input = (By.ID, "number")
        self.card_code_input = (By.ID, "code")
        self.card_link_button = (By.CSS_SELECTOR, "button.link")
        self.message_input = (By.ID, "comment")
        self.blanket_checkbox = (By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div:nth-child(1) > div > div.r-sw > div > span')
        self.ice_cream_plus_button = (By.CSS_SELECTOR, '#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.form > div.reqs.open > div.reqs-body > div.r.r-type-group > div > div.r-group-items > div:nth-child(1) > div > div.r-counter > div > div.counter-plus.disabled')
        self.order_button = (By.CSS_SELECTOR, "#root > div > div.workflow > div.smart-button-wrapper > button > span.smart-button-secondary")
        self.driver_modal = (By.CSS_SELECTOR, ".order-body .driver-info")

    # --- Métodos de acción ---
    def set_route(self, from_address, to_address):
        self.wait.until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)
        self.wait.until(EC.visibility_of_element_located(self.to_field)).send_keys(to_address + Keys.ENTER)

    def get_from(self):
        return self.wait.until(EC.visibility_of_element_located(self.from_field)).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_comfort(self):
        self.wait.until(EC.element_to_be_clickable(self.order_taxi)).click()
        self.wait.until(EC.element_to_be_clickable(self.comfort_tariff_button)).click()

    def get_confort_tariff_class(self):
        return self.driver.find_element(*self.comfort_tariff_button).get_attribute("class")

    def fill_phone(self, phone):
        self.wait.until(EC.element_to_be_clickable(self.phone_button)).click()
        field = self.wait.until(EC.visibility_of_element_located(self.phone_input))
        field.send_keys(phone)
        self.wait.until(EC.element_to_be_clickable(self.phone_submit)).click()

    def fill_sms_code(self, sms_code):
        self.wait.until(EC.element_to_be_clickable(self.phone_button)).click()

    def add_card(self, number, cvv):
        self.wait.until(EC.element_to_be_clickable(self.payment_method)).click()
        self.wait.until(EC.element_to_be_clickable(self.card_add_button)).click()
        self.wait.until(EC.visibility_of_element_located(self.card_number_input)).send_keys(number)
        code_field = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
        code_field.send_keys(cvv)
        code_field.send_keys(Keys.TAB)
        self.wait.until(EC.element_to_be_clickable(self.card_link_button)).click()

    def write_message(self, text):
        self.wait.until(EC.visibility_of_element_located(self.message_input)).send_keys(text)

    def request_blanket(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_checkbox)).click()

    def add_ice_creams(self, qty=2):
        plus = self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus_button))
        for _ in range(qty):
            plus.click()

    def order_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.order_button)).click()

    def wait_for_driver(self):
        self.wait.until(EC.visibility_of_element_located(self.driver_modal))
