from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import data


class UrbanRoutesPage:
    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.get(data.urban_routes_url)

        # --- Localizadores ---
        self.from_field = (By.ID, "from")
        self.to_field = (By.ID, "to")
        self.order_taxi = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
        self.comfort_tariff_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[3]')
        self.phone_button = (By.CSS_SELECTOR, ".np-button")
        self.phone_input = (By.ID, "phone")
        self.phone_submit = (By.CSS_SELECTOR, "#root > div > div.number-picker.open > div.modal > div.section.active > form > div.buttons > button")
        self.phone_sms_code = (By.XPATH, '/html/body/div/div/div[1]/div[2]/div[2]/form/div[1]/div[1]/input')
        self.phone_sms_code_submit = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
        self.payment_method = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]')
        self.card_add_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]')
        self.card_number_input = (By.ID, "number")
        self.card_code_input = (By.CSS_SELECTOR, "#root > div > div.payment-picker.open > div.modal.unusual > div.section.active.unusual > form > div.card-wrapper > div.card-second-row > div.card-code > div.card-code-input")
        self.card_link_button = (By.CSS_SELECTOR, "#root > div > div.payment-picker.open > div.modal.unusual > div.section.active.unusual > form > div.pp-buttons > button:nth-child(1)")
        self.card_exit_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
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

    #def fill_sms_code(self, sms_code):
        #self.wait.until(EC.element_to_be_clickable(self.phone_button)).click()

    def fill_sms_code(self, sms_code):
        self.sms_input = (By.XPATH, '/html/body/div/div/div[1]/div[2]/div[2]/form/div[1]/div[1]/input')
        sms_input = self.wait.until(
            EC.visibility_of_element_located(self.sms_input)
        )
        sms_input.send_keys(sms_code)
        self.wait.until(EC.element_to_be_clickable(self.phone_sms_code_submit)).click()

    def add_card(self, number, cvv):
        from selenium.webdriver.common.keys import Keys
        import time

        self.wait.until(EC.element_to_be_clickable(self.payment_method)).click()
        self.wait.until(EC.element_to_be_clickable(self.card_add_button)).click()

        # Wait for card modal to be visible
        time.sleep(0.5)

        # Fill card number
        card_number_field = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        card_number_field.click()
        card_number_field.clear()
        card_number_field.send_keys(number)

        # Wait and press TAB
        time.sleep(0.3)
        card_number_field.send_keys(Keys.TAB)

        # Wait for focus to move to CVV
        time.sleep(0.5)

        # Find the active element (should be CVV field after TAB)
        active_element = self.driver.switch_to.active_element
        active_element.send_keys(cvv)

        # Press TAB again to move away and trigger validation
        active_element.send_keys(Keys.TAB)

        # Wait for validation
        time.sleep(1)

        # Try clicking outside the modal first to close any dropdowns
        try:
            # Click on a neutral area
            self.driver.find_element(By.TAG_NAME, 'body').click()
        except:
            pass

        time.sleep(0.5)

        # Now try to click the link button
        # First check if button exists and get its state
        try:
            link_button = self.driver.find_element(*self.card_link_button)
            print(f"Button found. Enabled: {link_button.is_enabled()}, Displayed: {link_button.is_displayed()}")
            print(f"Button classes: {link_button.get_attribute('class')}")

            # Try clicking even if not "clickable"
            link_button.click()
        except Exception as e:
            print(f"Error clicking button: {e}")
            # Force click with JavaScript
            link_button = self.driver.find_element(*self.card_link_button)
            self.driver.execute_script("arguments[0].click();", link_button)
        self.wait.until(EC.element_to_be_clickable(self.card_exit_button)).click()


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
