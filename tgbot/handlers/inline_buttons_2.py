from dataclasses import dataclass

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from faker import Faker

inline_buttons_router = Router()


@dataclass
class Item:
    item_id: int
    name: str
    price: int
    photo_url: str


fake = Faker()

# Here how you can create a list of fake items
items = [
    Item(item_id=1, name=fake.name(), price=100, photo_url=fake.image_url())
    for _ in range(2)
]
