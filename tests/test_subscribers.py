from message import Message
from message_subscribers import DiceRoller, ShabbatSubscriber
from unittest.mock import MagicMock


def test_dice_roller():
    interface = MagicMock()
    dice_roller = DiceRoller(interface=interface, logger=MagicMock())
    dice_roller.notify_new_message(Message('', '/roll 10'))
    interface.send_message.assert_called()


def test_shabbat_time():
    interface = MagicMock()
    dice_roller = ShabbatSubscriber(interface=interface, logger=MagicMock())
    dice_roller.notify_new_message(Message('', 'when is shabbat'))
    interface.send_message.assert_called()
