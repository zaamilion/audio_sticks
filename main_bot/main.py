import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import CommandStart
import os
import threading
import importlib
import json
from aiogram.fsm.context import FSMContext
import subprocess
import shutil
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

sys.path.append(BASE_PATH)

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
    await state.clear()
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
    global tokenz
    await functions.delete_old_message(message.from_user.id, last_message)
    last_message[message.from_user.id] = await message.answer('Waiting...')
    bot_tarif = await state.get_data()
    bot_tarif = list(bot_tarif.values())[0]
    owner_bot = message.from_user.id 
    token_bot = message.text
    name = f'{owner_bot}{len(users.list[owner_bot][1])}'
    new_path = BASE_PATH + f'/{name}'
    
    dict_tokens = {}
    dict_tokens['token'] = token_bot
    dict_tokens['owner'] = owner_bot
    dict_tokens['tarif'] = bot_tarif.__dict__

    shutil.copytree(BASE_BOT_PATH, new_path)
    
    with open(f'{new_path}/tokens.json', 'w') as file:
        json.dump(dict_tokens, file)

    await asyncio.create_subprocess_shell(f'cd {new_path}&&python3 main.py')
    await functions.delete_old_message(message.from_user.id, last_message)
    last_message[message.from_user.id] = await message.answer('Succesfull')

async def running():
    await dp.start_polling(bot)

asyncio.run(running())