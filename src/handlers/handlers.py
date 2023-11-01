import json

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from src.config.config import Config
from src.services.services import validate_request
from src.database.mongodb import aggregate_salary_data


router = Router()


check = {"dt_from": "2022-09-01T00:00:00",
         "dt_upto": "2022-12-31T23:59:00",
         "group_type": "month"}


@router.message(Command(commands=['start']))
async def process_start(message: Message):
    await message.answer(text=f"Привет {message.from_user.first_name}")


@router.message()
async def process_request(message: Message):
    try:
        request_data = json.loads(message.text)
        if validate_request(request_data):
            response = await aggregate_salary_data(
                request_data["dt_from"],
                request_data["dt_upto"],
                request_data["group_type"]
            )
            await message.answer(str(response))
        else:
            await message.answer(text=f'Невалидный запос. Пример запроса:\n '
                                      f'{str(check)}')
    except json.JSONDecodeError:
        await message.answer(text="Ошибка: Неверный формат JSON")
