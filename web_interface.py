from message import Message


class WhatsAppWebInterface:
    def __init__(self, driver):
        self.driver = driver
        self.message_watchers = []

    def load_whatsappweb(self):
        self.driver.get('https://web.whatsapp.com/')

    def is_at_qr_code_dialog(self):
        try:
            self.driver.find_element_by_xpath('//div[@class="landing-window"]//canvas[@aria-label="Scan me!"]')
            return True
        except:
            return False

    def is_at_reload_qr_code_dialog(self):
        try:
            self.driver.find_element_by_xpath('//div[@class="landing-window"]//div[text() = "Click to reload QR code"]')
            return True
        except:
            return False

    def save_qr_code(self, filename):
        qr_elem = self.driver.find_element_by_xpath('//div[@class="landing-window"]//div[@class="landing-main"]')
        qr_elem.screenshot(filename)

    def select_chat_by_name(self, name):
        chat_elem = self.driver.find_element_by_xpath(f'//span[@title="{name}"]')
        chat_elem.click()

    def get_messages(self):
        msgs_xpath = "//div[contains(@class, 'message-in')]//div[@data-pre-plain-text]"
        for msg in self.driver.find_elements_by_xpath(msgs_xpath):
            yield Message(msg.get_attribute('data-pre-plain-text'), msg.text)

    def send_message(self, text):
        input_xpath = "//div[@id='main']//div[@contenteditable='true']"
        input_elem = self.driver.find_element_by_xpath(input_xpath)
        input_elem.clear()
        input_elem.send_keys(text)

        send_btn_xpath = "//div[@id='main']//span[@data-icon='send']"
        send_btn_elem = self.driver.find_element_by_xpath(send_btn_xpath)
        send_btn_elem.click()