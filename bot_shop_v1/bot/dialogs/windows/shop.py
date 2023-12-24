from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import (Back, Button, ScrollingGroup, Select,
                                        Start)
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format
from bot.states import ConfigSG, MenuSG, ShopSG
from database.models.product import Product


async def get_categories(dialog_manager: DialogManager, **kwargs):
    products = await Product.all()
    dialog_manager.start_data.clear() if dialog_manager.start_data else None
    dialog_manager.dialog_data.clear() if dialog_manager.start_data else None
    categories = set([product.category for product in products])
    return {
        'categories': categories,
    }


async def get_sub_categories(dialog_manager: DialogManager, **kwargs):
    products = await Product.filter(category=dialog_manager.dialog_data['category'])
    sub_categories = set(
        [sub_category.sub_category for sub_category in products]
    )
    return {
        'sub_categories': sub_categories,
    }


async def get_items(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data
    products = await Product.filter(category=data['category'], sub_category=data['sub_category'])
    names = set([product.name for product in products])
    return {
        'names': names
    }


async def get_description(dialog_manager: DialogManager, **kwargs) -> dict[str, str | float]:
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
    products = await Product.filter(name=dialog_manager.dialog_data['name'])
    memories = ','.join(set([str(product.memory) for product in products]))
    product = products[0]
    return {
        'description': product.description,
        'price': product.price,
        'name': product.name,
        'img': product.image,
        'memories': memories,

    }


async def on_category_selected(callback: CallbackQuery, widget: Any,
                               manager: DialogManager, item_id: str):
    manager.dialog_data['category'] = item_id
    await manager.switch_to(state=ShopSG.sub_category)


async def on_subcategory_selected(callback: CallbackQuery, widget: Any,
                                  manager: DialogManager, item_id: str):
    manager.dialog_data['sub_category'] = item_id
    await manager.switch_to(state=ShopSG.product)


async def on_product_selected(callback: CallbackQuery, widget: Any,
                              manager: DialogManager, item_id: str):
    manager.dialog_data['name'] = item_id
    await manager.switch_to(state=ShopSG.description)


async def start_config(callback: CallbackQuery, button: Button,
                       manager: DialogManager):
    await manager.start(state=ConfigSG.fields, data=manager.dialog_data)


def get_id(*args, **kwargs) -> str:
    return args[0]


category = Window(
    StaticMedia(url='https://i.imgur.com/GWrSh1F.jpg'),
    Select(
        text=Format('{item}'),
        id='select_category',
        item_id_getter=get_id,
        items='categories',
        on_click=on_category_selected,
    ),
    Start(text=Const('Back'), id='main_menu', state=MenuSG.main_menu),
    state=ShopSG.category,
    getter=get_categories,
)
sub_category = Window(
    StaticMedia(url='https://i.imgur.com/BhKu5uK.jpg'),
    Select(
        text=Format('{item}'),
        id='select_sub_category',
        item_id_getter=get_id,
        items='sub_categories',
        on_click=on_subcategory_selected,
    ),
    Back(text=Const('Back')),
    state=ShopSG.sub_category,
    getter=get_sub_categories,
)
product = Window(
    StaticMedia(url='https://i.imgur.com/s4ucm3H.jpg'),
    ScrollingGroup(
        Select(
            text=Format('{item}'),
            id='select_product',
            item_id_getter=get_id,
            items='names',
            on_click=on_product_selected,
        ),
        id='scrolling_products',
        height=5,
        width=1,
    ),
    Back(text=Const('Back')),
    state=ShopSG.product,
    getter=get_items,
)
description = Window(
    StaticMedia(url=Format(text='{img}')),
    Format(
        'Product: {name}\nDescription: {description}\nMemory: {memories}\nPrice: {price}'),
    Button(text=Const("Buy"), id='buy', on_click=start_config),
    Back(text=Const('Back')),
    state=ShopSG.description,
    getter=get_description,
)
ShopDLG = Dialog(category, sub_category, product, description)
