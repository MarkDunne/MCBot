import re
import pytz
import random
import datetime
import humanize

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

        now = datetime.datetime.now(pytz.timezone(self.location.timezone))
        friday = now + datetime.timedelta(4 - now.weekday())
        saturday = now + datetime.timedelta(5 - now.weekday())

        shabbat_start = sun(self.location.observer, date=friday)['sunset'] - datetime.timedelta(minutes=18)
        shabbat_end = sun(self.location.observer, date=saturday)['sunset'] + datetime.timedelta(minutes=49)

        if now < shabbat_start:
            reply = f'Time to Shabbat: {humanize.precisedelta(shabbat_start - now)} (Friday {humanize.naturaltime(shabbat_start.time().replace(microsecond=0))})'
        elif shabbat_start < now < shabbat_end:
            reply = f'Enjoy Shabbat. Shabbat ends in {humanize.precisedelta(shabbat_end - now)} (Saturday {humanize.naturaltime(shabbat_end.time().replace(microsecond=0))})'
        else:
            friday = friday + datetime.timedelta(weeks=1)
            shabbat_start = sun(self.location.observer, date=friday)['sunset'] - datetime.timedelta(minutes=18)
            reply = f'Time to Shabbat: {humanize.precisedelta(shabbat_start - now)} (Friday {humanize.naturaltime(shabbat_start.time().replace(microsecond=0))})'

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
                low, high = 1, nums[0] + 1
            elif len(nums) == 2:
                low, high = nums[0], nums[1] + 1
            else:
                return

            print(low, high, str(random.randrange(low, high)))
            self.logger.info(f'Rolling dice between {low} and {high}')
            self.interface.send_message(str(random.randrange(low, high)))
        except:
            pass


class Chooser(MessageSubscriber):
    def __init__(self, interface: WhatsAppWebInterface, logger):
        super().__init__(interface, logger)

    def notify_new_message(self, message: Message):
        triggered = message.content.lower().startswith('/choose')
        self.logger.info(f'Chooser triggered: {triggered}')
        if not triggered:
            return

        try:
            opts = message.content.replace("/choose ", "").split(",")
            opts = [opt.strip() for opt in opts]
            choice = random.choice(opts)

            self.logger.info(f'Chosen option {choice} from {opts}')
            self.interface.send_message(choice)
        except:
            pass
