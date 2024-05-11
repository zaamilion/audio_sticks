import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import importlib
import shutil
import os
import sys
import tokens
import markups
import functions
import db
import fsm
import blanks

BASE_PATH = '/workspaces/audio_sticks'
SELF_PATH = '/workspaces/audio_sticks/main_bot'
BASE_BOT_PATH = '/workspaces/audio_sticks/default_bot'

last_message = {}
bot = Bot(token=tokens.token)
dp = Dispatcher()
rt = Router()
dp.include_router(rt)

users = db.Database('users')
users.load()
# users db type: {user_id: [tarif: Tarif, [bot: aiogram.bot,...]],...}

@rt.message(F.text == 'create_bot')
async def creating_bot0(message: types.Message, state: FSMContext):
    await functions.delete_old_message(message.from_user.id, last_message)
    functions.add_to_db(message.from_user.id, users)
    last_message[message.from_user.id] = await message.answer(blanks.choose_tarif_for_new_bot, reply_markup=markups.generate_tariffs_markup(users.list[message.from_user.id][0].bot_tarifs))
    await state.set_state(fsm.creating_bot.tarif)

@rt.callback_query(fsm.creating_bot.tarif)
async def creating_bot1(call: types.callback_query, state: FSMContext):
    await functions.delete_old_message(call.from_user.id, last_message)
    tarif = functions.get_tariff(call, users)
    await state.update_data(tariff=tarif)
    users.list[call.from_user.id][0].bot_tarifs[tarif] -= 1
    if users.list[call.from_user.id][0].bot_tarifs[tarif] == 0:
        del users.list[call.from_user.id][0].bot_tarifs[tarif]
    last_message[call.from_user.id] = await bot.send_message(call.from_user.id, blanks.create_bot, reply_markup=markups.generate_tariffs_markup(users.list[call.from_user.id][0].bot_tarifs))
    await state.set_state(fsm.creating_bot.token)

@rt.message(fsm.creating_bot.token)
async def creating_bot2(message: types.Message, state: FSMContext):
    await functions.delete_old_message(message.from_user.id, last_message)
    bot_tarif = await state.get_data()
    bot_tarif = list(bot_tarif.values())[0]
    owner = message.from_user.id 
    token = message.text
    name = f'{owner}{len(users.list[owner][1])}'
    new_path = BASE_PATH + f'/{name}'
    shutil.copytree(BASE_BOT_PATH, new_path)

    sys.path.append(new_path)
    new_module = importlib.import_module(name)
    from new_module import main, tokens
    tokens.owner = owner
    tokens.token = token
    tokens.bot_tarif = bot_tarif
    tokens.path = new_path
    import tokens
    asyncio.create_task(main.running)
    await state.clear()
    await message.answer('Succesfully')

async def running():
    await dp.start_polling(bot)

asyncio.run(running())