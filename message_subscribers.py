import re
import random
import datetime

from message import Message

from astral import LocationInfo
from astral.sun import sun
from web_interface import WhatsAppWebInterface


class MessageSubscriber:
    def __init__(self, interface: WhatsAppWebInterface, logger):
        self.logger = logger
        self.interface = interface

    def notify_new_message(self, message: Message):
        return NotImplementedError()


class ShabbatSubscriber(MessageSubscriber):
    def __init__(self, interface: WhatsAppWebInterface, logger):
        super().__init__(interface, logger)
        self.location = LocationInfo("London", "England", "Europe/London", 51.511449, -0.072739)

    def notify_new_message(self, message: Message):
        triggered = any([
            'what time is shabbat' in message.content.lower(),
            'when is shabbat' in message.content.lower(),
        ])
        self.logger.info(f'ShabbatSubscriber triggered: {triggered}')
        if not triggered:
            return

        today = datetime.datetime.now()
        friday = today + datetime.timedelta((4 - today.weekday()) % 7)

        sunset = sun(self.location.observer, date=friday)['sunset']
        shabbat = sunset - datetime.timedelta(minutes=18)

        reply = f'Shabbat begins at {shabbat.isoformat()}'
        self.interface.send_message(reply)


class DiceRoller(MessageSubscriber):
    def __init__(self, interface: WhatsAppWebInterface, logger):
        super().__init__(interface, logger)

    def notify_new_message(self, message: Message):
        triggered = message.content.lower().startswith('/roll')
        self.logger.info(f'DiceRoller triggered: {triggered}')
        if not triggered:
            return

        try:
            nums = [int(match) for match in re.findall(r'\d+', message.content)]

            if len(nums) == 1:
                low, high = 0, nums[0]
            elif len(nums) == 2:
                low, high = nums[0], nums[1]
            else:
                return

            print(low, high, str(random.randrange(low, high)))
            self.logger.info(f'Rolling dice between {low} and {high}')
            self.interface.send_message(str(random.randrange(low, high)))
        except:
            pass
