import re
from typing import Generator, Callable

import pytest
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_mock.facade_factory import private_chat_tg_control
from aiogram_mock.tg_control import PrivateChatTgControl

from tgbot.handlers import routers_list

bot = Bot(token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
dispatcher = Dispatcher()
dispatcher.include_routers(*routers_list)


@pytest.fixture()
def tg_control() -> Generator[PrivateChatTgControl, None, None]:
    with private_chat_tg_control(
        bot=bot,
        dispatcher=dispatcher,
    ) as tg_control:
        yield tg_control


SHOP_BUTTONS = [
    "Electronics",
    "Clothing",
    "Footwear",
    "Books",
    "Toys",
    "Back to Main Menu",
]

COURSES_BUTTONS = [
    "Programming",
    "Design",
    "Marketing",
    "Languages",
    "Photography",
    "Course Catalog",
    "Back to Main Menu",
]

ITEMS_BUTTONS = [
    "Buy",
    "Like",
    "Dislike",
    "Share with a friend",
]


async def markup_check(keyboard: InlineKeyboardMarkup, markup: list[int]):
    assert len(keyboard.inline_keyboard) == len(markup)
    for row, n_buttons in zip(keyboard.inline_keyboard, markup):
        assert len(row) == n_buttons


async def buttons_text_check(keyboard: InlineKeyboardMarkup, texts: list[str]):
    btn_idx = 0
    for row in keyboard.inline_keyboard:
        for button in row:
            assert button.text == texts[btn_idx]
            btn_idx += 1


async def callback_data_check(keyboard: InlineKeyboardMarkup):
    for row in keyboard.inline_keyboard:
        for button in row:
            assert re.match(r"action:(\w+)", button.callback_data)


@pytest.mark.asyncio
async def test_shop_buttons(tg_control):
    await tg_control.send("/shop_buttons")
    assert tg_control.last_message.text
    assert tg_control.last_message.reply_markup
    assert tg_control.last_message.reply_markup.inline_keyboard

    await markup_check(tg_control.last_message.reply_markup, [3, 2, 1])
    await buttons_text_check(tg_control.last_message.reply_markup, SHOP_BUTTONS)
    await callback_data_check(tg_control.last_message.reply_markup)


@pytest.mark.asyncio
async def test_courses_buttons(tg_control):
    await tg_control.send("/courses_buttons")
    assert tg_control.last_message.text
    assert tg_control.last_message.reply_markup
    assert tg_control.last_message.reply_markup.inline_keyboard

    await markup_check(tg_control.last_message.reply_markup, [2, 2, 2, 1])
    await buttons_text_check(tg_control.last_message.reply_markup, COURSES_BUTTONS)
    await callback_data_check(tg_control.last_message.reply_markup)


def button_text_selector(text: str) -> Callable[[InlineKeyboardButton], bool]:
    return lambda button: button.text == text


@pytest.mark.asyncio
async def test_items(tg_control):
    await tg_control.send("/items")
    assert len(tg_control.messages) == 3

    for message in tg_control.messages[-2:]:
        assert message.photo
        assert message.caption
        assert message.reply_markup
        assert message.reply_markup.inline_keyboard

    mocked_user_message, first_message, second_message = tg_control.messages
    await markup_check(first_message.reply_markup, [1, 2, 1])
    await buttons_text_check(first_message.reply_markup, ITEMS_BUTTONS)

    item_id = first_message.reply_markup.inline_keyboard[0][0].callback_data.split(":")[
        -1
    ]
    assert item_id.isdigit()

    answer = await tg_control.click(button_text_selector("Buy"), first_message)
    first_message = tg_control.messages[-2]
    assert answer
    assert first_message.caption == f"Buy item with item_id: {item_id}"
    assert first_message.reply_markup is None

    item_id = second_message.reply_markup.inline_keyboard[0][0].callback_data.split(
        ":"
    )[-1]
    assert item_id.isdigit()

    callback_answer = await tg_control.click(
        button_text_selector("Like"), second_message
    )
    assert callback_answer.text == f"You have liked item: {item_id}"
    assert callback_answer.show_alert is None

    callback_answer = await tg_control.click(
        button_text_selector("Dislike"), second_message
    )
    assert callback_answer.text == f"You have disliked item: {item_id}"
    assert callback_answer.show_alert is None
