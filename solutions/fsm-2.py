from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

form_router = Router()
class TestClass(StatesGroup):
    answer1 = State()
    answer2 = State()
    answer3 = State()


@form_router.message(Command("form"))
async def forms(message: Message, state: FSMContext):
    await message.answer(f"Имя")
    await state.set_state(TestClass.answer1)


@form_router.message(TestClass.answer1)
async def forms(message: Message, state: FSMContext):
    await state.update_data(answer1=message.text)
    await message.answer(f"Email")
    await state.set_state(TestClass.answer2)


@form_router.message(TestClass.answer2)
async def forms(message: Message, state: FSMContext):
    await state.update_data(answer2=message.text)
    await message.answer("Номер телефона")
    await state.set_state(TestClass.answer3)


@form_router.message(TestClass.answer3)
async def forms(message: Message, state: FSMContext):
    answers = await state.get_data()
    await message.answer(f"Hello! You entered the following data:\n\n"
                         f"Name: {answers['answer1']}\n"
                         f"Email: {answers['answer2']}\n"
                         f"Phone: {message.text}")
    await state.clear()
