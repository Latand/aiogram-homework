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
items = [
    Item(item_id=1, name=fake.name(), price=100, photo_url=fake.image_url()) for _ in
    range(2)
]


class ItemActionCB(CallbackData, prefix="item"):
    action: str
    item_id: int


def generate_item_kb(item_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Buy",
                    callback_data=ItemActionCB(action="buy", item_id=item_id))
    keyboard.button(text="Like",
                    callback_data=ItemActionCB(action="like", item_id=item_id))
    keyboard.button(text="Dislike",
                    callback_data=ItemActionCB(action="dislike", item_id=item_id))
    keyboard.button(text="Share with a friend",
                    switch_inline_query=str(item_id))
    keyboard.adjust(1, 2, 1)
    return keyboard.as_markup()


@inline_buttons_router.message(Command("items"))
async def items_command_handler(message: Message, bot):
    # Sending two example items with different IDs. You can expand this logic.
    for item in items:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=item.photo_url,
            caption=f"{item.name}\nPrice: {item.price}",
            reply_markup=generate_item_kb(item.item_id)
        )


@inline_buttons_router.callback_query(ItemActionCB.filter(F.action == "buy"))
async def buy_item_handler(query: CallbackQuery, callback_data: ItemActionCB):
    await query.message.edit_caption(
        caption=f"Buy item with item_id: {callback_data.item_id}"
    )
    await query.answer()


@inline_buttons_router.callback_query(ItemActionCB.filter(F.action == "like"))
async def like_item_handler(query: CallbackQuery, callback_data: ItemActionCB):
    # Logic to increase rating can be added here if desired.
    await query.answer(f"You have liked item: {callback_data.item_id}")

@inline_buttons_router.callback_query(ItemActionCB.filter(F.action == "dislike"))
async def dislike_item_handler(query: CallbackQuery, callback_data: ItemActionCB):
    # Logic to decrease rating can be added here if desired.
    await query.answer(f"You have disliked item: {callback_data.item_id}")