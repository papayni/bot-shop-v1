from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format
from bot.states import MenuSG, ShopSG
from database.models.user import User


async def get_user_info(dialog_manager: DialogManager, event_from_user, **kwargs):
    user = await User.get(telegram_id=event_from_user.id)
    return {'telegram_id': user.telegram_id}


main_menu = Window(
    StaticMedia(url='https://i.imgur.com/IGFZ4JY.jpg'),
    SwitchTo(text=Format('Account'), id='profile', state=MenuSG.profile),
    Start(text=Format('Shop'), id='shop', state=ShopSG.category),
    Start(text=Format('Rules'), id='rules', state=MenuSG.rules),
    state=MenuSG.main_menu,
)
account = Window(
    StaticMedia(url='https://i.imgur.com/c47z58r.jpg'),
    Format('Account\nYour telegram id: {telegram_id}'),
    SwitchTo(text=Format('Back'), id='back', state=MenuSG.main_menu),
    state=MenuSG.profile,
    getter=get_user_info,
)
rules = Window(
    StaticMedia(url='https://i.imgur.com/Z0Ni2Lm.jpg'),
    Format('Rules'),
    SwitchTo(text=Format('Back'), id='back', state=MenuSG.main_menu),
    state=MenuSG.rules,
    getter=get_user_info,
)
MenuDLG = Dialog(main_menu, account, rules)
