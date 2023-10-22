from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

inline_buttons_router = Router()


class ActionCB(CallbackData, prefix="action"):
    action: str


# Online Shop Theme
def shop_kb():
    inline_kb = InlineKeyboardBuilder()
    inline_kb.button(text="Electronics", callback_data=ActionCB(action="electronics"))
    inline_kb.button(text="Clothing", callback_data=ActionCB(action="clothing"))
    inline_kb.button(text="Footwear", callback_data=ActionCB(action="footwear"))
    inline_kb.button(text="Books", callback_data=ActionCB(action="books"))
    inline_kb.button(text="Toys", callback_data=ActionCB(action="toys"))
    inline_kb.button(
        text="Back to Main Menu", callback_data=ActionCB(action="back_main")
    )

    inline_kb.adjust(3, 2, 1)
    return inline_kb.as_markup()


# Educational Courses Theme
def courses_kb():
    inline_kb = InlineKeyboardBuilder()
    inline_kb.button(text="Programming", callback_data=ActionCB(action="programming"))
    inline_kb.button(text="Design", callback_data=ActionCB(action="design"))
    inline_kb.button(text="Marketing", callback_data=ActionCB(action="marketing"))
    inline_kb.button(text="Languages", callback_data=ActionCB(action="languages"))
    inline_kb.button(text="Photography", callback_data=ActionCB(action="photography"))
    inline_kb.button(
        text="Course Catalog", callback_data=ActionCB(action="course_catalog")
    )
    inline_kb.button(
        text="Back to Main Menu", callback_data=ActionCB(action="back_main")
    )

    inline_kb.adjust(2, 2, 2, 1)
    return inline_kb.as_markup()


@inline_buttons_router.message(Command("shop_buttons"))
async def shop_buttons_handler(message: Message):
    text = "Choose a product category to explore:"
    await message.answer(text, reply_markup=shop_kb())


@inline_buttons_router.message(Command("courses_buttons"))
async def courses_buttons_handler(message: Message):
    text = "Select a course category to enroll in:"
    await message.answer(text, reply_markup=courses_kb())
