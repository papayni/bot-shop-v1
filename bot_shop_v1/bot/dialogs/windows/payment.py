from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Group, Select
from aiogram_dialog.widgets.text import Const, Format
from bot.states import ConfigSG, PaymentSG


async def get_ways_payment(dialog_manager: DialogManager, **kwargs):
    return {'ways': ['BTC', 'Bank card', 'PayPal']}


def get_id(*args: tuple[str], **kwargs):
    return args[0][0]


async def on_way_payment_selected(callback: CallbackQuery, widget: Any,
                                  manager: DialogManager, item_id: str):
    field = manager.dialog_data['field']
    manager.dialog_data[field] = item_id
    await manager.switch_to(state=ConfigSG.fields)


async def back_config(callback: CallbackQuery, button: Button,
                      manager: DialogManager):
    await manager.start(state=ConfigSG.config, data=manager.start_data)


Payment = Window(
    Format(text='Payment:'),
    Group(
        Select(
            text=Format('{item}'),
            id='select_field',
            item_id_getter=get_id,
            items='ways',
            on_click=on_way_payment_selected,
        ),
        Button(text=Const('Back'), on_click=back_config, id='back_config'),
        width=1,
    ),
    getter=get_ways_payment,
    state=PaymentSG.way_payment
)
PaymentDLG = Dialog(Payment)
