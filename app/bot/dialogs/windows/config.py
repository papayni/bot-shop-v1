from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Button, Group, Select
from aiogram_dialog.widgets.text import Const, Format
from bot.states import ConfigurationSG, ShopSG
from database.models.product import Product


async def get_fields(dialog_manager: DialogManager, **kwargs):
    products = await Product.filter(name=dialog_manager.start_data['name']).values()
    fields = list(products[0].keys())[7:]
    result = []
    for field in fields:
        if value := dialog_manager.dialog_data.get(field):
            result.append((field, value))
        else:
            result.append((field, 'x'))
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
    await manager.switch_to(state=ConfigurationSG.config)


async def on_value_selected(callback: CallbackQuery, widget: Any,
                            manager: DialogManager, item_id: str):
    field = manager.dialog_data['field']
    manager.dialog_data[field] = item_id
    await manager.switch_to(state=ConfigurationSG.fields)


async def back_shop(callback: CallbackQuery, button: Button,
                    manager: DialogManager):
    await manager.start(state=ShopSG.description, data=manager.start_data)


fields = Window(
    Format(text='Fields'),
    Group(
        Select(
            text=Format('{item[0]}: {item[1]}'),
            id='select_product',
            item_id_getter=get_id,
            items='fields',
            on_click=on_field_selected,
        ),
        Button(text=Const('Back'), on_click=back_shop, id='back_shop'),
        width=1,
    ),
    getter=get_fields,
    state=ConfigurationSG.fields
)

config_fields = Window(
    Format(text='Config fieled'),
    Group(
        Select(
            text=Format('{item[0]}'),
            id='select_product',
            item_id_getter=get_id,
            items='values',
            on_click=on_value_selected,
        ),
        Back(),
        width=1,
    ),
    getter=get_value,
    state=ConfigurationSG.config
)
ConfigDLG = Dialog(fields, config_fields)
