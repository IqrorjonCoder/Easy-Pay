import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

API_TOKEN = 'XXXXXXXXXXXXXXXXXXXX'

bot = Bot(token=API_TOKEN)

button1 = KeyboardButton("Add to base")
button2 = KeyboardButton('About IqrorjonCoder')

keybord1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1).add(button2)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hi!. It is registration bot for EasyPay App. It is created by @IqrorjonCoder ", reply_markup=keybord1)

    class Form(StatesGroup):
        ism = State()
        familiya = State()
        karta_raqam = State()
        karta_muddat = State()
        karta_parol = State()

    @dp.message_handler(text="Add to base")
    async def cmd_start(message: types.Message):
        await Form.ism.set()
        await message.answer("enter your firstname ?")

    @dp.message_handler(state=Form.ism)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['ism'] = message.text
        await Form.next()
        await message.answer("enter your lastname ?")

    @dp.message_handler(state=Form.familiya)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['familiya'] = message.text
        await Form.next()
        await message.answer("enter your card number ?")

    @dp.message_handler(state=Form.karta_raqam)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['karta_raqam'] = message.text
        await Form.next()
        await message.answer("enter your card date of expiry ?")

    @dp.message_handler(state=Form.karta_muddat)
    async def process_name(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['karta_muddat'] = message.text
        await Form.next()
        await message.answer("enter your card password ?")

    @dp.message_handler(state=Form.karta_parol)
    async def process_gender(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['karta_parol'] = message.text
            data['karta_hisob'] = "1500"

            rasm_url = f"./photos/{data['ism']}__{data['familiya']}__{data['karta_raqam']}__{data['karta_muddat']}__{data['karta_hisob']}__{data['karta_parol']}"
            json_url = f"{data['ism']}__{data['familiya']}__{data['karta_raqam']}__{data['karta_muddat']}__{data['karta_hisob']}__{data['karta_parol']}"

            dic = {
                "ism": data['ism'],
                "familiya": data['familiya'],
                "karta_raqam": data['karta_raqam'],
                "karta_muddat": data['karta_muddat'],
                "karta_hisob": data['karta_hisob'],
                "karta_parol": data['karta_parol'],
                "rasm_url": rasm_url
            }

            with open(f"./jsons/{json_url}.json", "w") as outfile:
                json.dump(dic, outfile)

            with open(f"database_json.json", "w") as outfile:
                json.dump(dic, outfile)

        await message.answer("send me your photo: ")

        @dp.message_handler(content_types=['photo'])
        async def handle_docs_photo(message: types.Message):
            try:

                f = open(f'database_json.json', 'r')
                data = json.load(f)

                await message.photo[-1].download(destination_file=f"{data['rasm_url']}.jpg")

                await message.answer("you added to base successfully !!!")

            except:
                pass

        await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
