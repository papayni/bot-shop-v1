from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button, Group, Select
from aiogram_dialog.widgets.text import Const, Format
from bot.states import ConfigSG, PaymentSG, ShopSG
from database.models.product import Product


async def get_fields(dialog_manager: DialogManager, **kwargs):
    products = await Product.filter(name=dialog_manager.start_data['name']).values()
    fields = list(products[0].keys())[7:]
    result = []
    for field in fields:
        if products[0][field] is not None:
            if value := dialog_manager.dialog_data.get(field):
                result.append((field, value))
            else:
                result.append((field, '-'))
    return {'fields': result}


async def get_value(dialog_manager: DialogManager, **kwargs):
    products = await Product.filter(name=dialog_manager.start_data['name']).values()
    values = []
    for product in products:
        if value := product.get(dialog_manager.dialog_data['field']):
            values.append((value, ))
    return {'values': set(values)}


def get_id(*args: tuple[str], **kwargs):
    return args[0][0]


async def on_field_selected(callback: CallbackQuery, widget: Any,
                            manager: DialogManager, item_id: str):
    manager.dialog_data['field'] = item_id
    await manager.switch_to(state=ConfigSG.config)


async def on_value_selected(callback: CallbackQuery, widget: Any,
                            manager: DialogManager, item_id: str):
    field = manager.dialog_data['field']
    manager.dialog_data[field] = item_id
    await manager.switch_to(state=ConfigSG.fields)


async def back_shop(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    print(manager.start_data)
    await manager.start(state=ShopSG.description, data=manager.start_data)


async def start_payment(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(state=PaymentSG.way_payment, data=manager.dialog_data)

fields = Window(
    Format(text='Fields'),
    Group(
        Select(
            text=Format('{item[0]}: {item[1]}'),
            id='select_field',
            item_id_getter=get_id,
            items='fields',
            on_click=on_field_selected,
        ),
        Button(text=Const('Payment'), id='payment', on_click=start_payment),
        Button(text=Const('Back'), on_click=back_shop, id='back_shop'),
        width=1,
    ),
    getter=get_fields,
    state=ConfigSG.fields
)

config_fields = Window(
    Format(text='Config fieled'),
    Group(
        Select(
            text=Format('{item[0]}'),
            id='select_config',
            item_id_getter=get_id,
            items='values',
            on_click=on_value_selected,
        ),
        Back(),
        width=1,
    ),
    getter=get_value,
    state=ConfigSG.config
)
ConfigDLG = Dialog(fields, config_fields)
