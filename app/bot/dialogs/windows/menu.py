from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Format
from database.models.user import User

from bot.states import MenuSG, ShopSG


async def get_user_info(dialog_manager: DialogManager, event_from_user, **kwargs):
    user = await User.get_or_none(telegram_id=event_from_user.id)
    return {'user': user}


main_menu = Window(
    # StaticMedia(),
    Format('Main menu'),
    SwitchTo(text=Format('Profile'), id='profile', state=MenuSG.profile),
    Start(text=Format('Shop'), id='shop', state=ShopSG.shop),
    Start(text=Format('Rules'), id='rules', state=MenuSG.rules),
    state=MenuSG.main_menu,
)
profile = Window(
    # StaticMedia(),
    Format('Profile'),
    SwitchTo(text=Format('Back'), id='back', state=MenuSG.main_menu),
    state=MenuSG.profile,
    getter=get_user_info,
)
rules = Window(
    # StaticMedia(),
    Format('Rules'),
    SwitchTo(text=Format('Back'), id='back', state=MenuSG.main_menu),
    state=MenuSG.rules,
    getter=get_user_info,
)
MenuDLG = Dialog(main_menu, profile, rules)
