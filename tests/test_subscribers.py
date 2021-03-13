from message import Message
from message_subscribers import DiceRoller
from unittest.mock import MagicMock


def test_dice_roller():
    interface = MagicMock()
    dice_roller = DiceRoller(interface=interface, logger=MagicMock())
    dice_roller.notify_new_message(Message('', '/roll 10'))
    interface.send_message.assert_called()
