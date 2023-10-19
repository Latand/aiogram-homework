from typing import Generator

import pytest
from aiogram import Bot, Dispatcher
from aiogram_mock.facade_factory import private_chat_tg_control
from aiogram_mock.tg_control import PrivateChatTgControl

from faker import Faker

from tgbot.handlers import routers_list

bot = Bot(token='123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11')
dispatcher = Dispatcher()
dispatcher.include_routers(*routers_list)
fake = Faker()

fake_name = fake.name()
fake_email = fake.email()
fake_phone = fake.phone_number()

@pytest.fixture()
def tg_control() -> Generator[PrivateChatTgControl, None, None]:
    with private_chat_tg_control(
            bot=bot,
            dispatcher=dispatcher,
    ) as tg_control:
        yield tg_control


@pytest.mark.asyncio
async def test_start(tg_control):
    await tg_control.send("/form")
    assert tg_control.last_message.text


@pytest.mark.asyncio
async def test_enter_name(tg_control):
    await tg_control.send(fake_name)
    assert tg_control.last_message.text


@pytest.mark.asyncio
async def test_enter_email(tg_control):
    await tg_control.send(fake_email)
    assert tg_control.last_message.text


@pytest.mark.asyncio
async def test_enter_phone(tg_control):
    await tg_control.send(fake_phone)
    assert tg_control.last_message.text == (
        f"""Hello! You entered the following data:

Name: {fake_name}
Email: {fake_email}
Phone: {fake_phone}"""
    )
