import time
import logging

from selenium import webdriver

from message_subscribers import ShabbatSubscriber, DiceRoller
from web_interface import WhatsAppWebInterface

logging.basicConfig(level=logging.INFO, format='%(asctime)s  %(levelname)-10s %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--user-data-dir=./User_Data')
    options.add_argument(f'--user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)

    web_interface = WhatsAppWebInterface(driver)

    subscribers = [
        ShabbatSubscriber(web_interface, logger),
        DiceRoller(web_interface, logger)
    ]

    logger.info('Loading interface')
    web_interface.load_whatsappweb()
    time.sleep(1)

    while web_interface.is_at_qr_code_dialog():
        if web_interface.is_at_reload_qr_code_dialog():
            logger.info('Reloading QR code')
            web_interface.load_whatsappweb()
            time.sleep(1)
        web_interface.save_qr_code('qr_service/static/qr.png')
        logger.info('Waiting for QR check')
        time.sleep(1)

    logger.info('QR check complete')

    interface = WhatsAppWebInterface(driver)
    interface.select_chat_by_name('Monday Club')

    time.sleep(0.5)

    # Don't trigger on old messages
    seen_messages = set()
    for message in interface.get_messages():
        seen_messages.add(message)

    while True:
        for message in interface.get_messages():
            if message not in seen_messages:
                logger.info(f'New message: {message}')
                seen_messages.add(message)
                for subscriber in subscribers:
                    subscriber.notify_new_message(message)
        time.sleep(2)
