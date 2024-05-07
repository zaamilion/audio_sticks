from asyncio import run
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import random
import sys
import os
sys.path.insert(0,'/workspaces/audio_sticks/data')
import db
import tokens
import markups
import functions
import classes
import blanks
stoping = False

dp = Dispatcher()
rt = Router()
dp.include_router(rt)
bot = Bot(token=tokens.TOKEN)

voice_ids = db.Database('voices')
voice_ids.list = {}
users = db.Database('users')
requests = 0
last_message = {}

@rt.message(CommandStart())
async def start(message: types.Message):
    global requests
    await functions.delete_old_message(message.from_user.id, last_message)
    requests = functions.save_db(requests, users)
    functions.add_to_db(message.from_user.id, users)
    if await functions.check_subscribe(bot, message, tokens.channels):
        if message.from_user.id == tokens.owner:
            await message.answer('Привет! Админ-панель войспака:', reply_markup=markups.admin_panel)
    else:
        await message.answer(blanks.subscribe_message, reply_markup=markups.markup_subscribe)

"""
@dp.message()
async def commands(message: types.Message):
    global requests
    requests += 1
    if requests == 10:
        dp.dump()
        requests = 0
    if message.from_user.id not in users.list:
        users.list.append(message.from_user.id)
    if (await bot.get_chat_member(user_id=message.from_user.id, chat_id=-1002013605939)).status != 'left':
        
        await message.answer('Бот работает в инлайн режиме')
    else:
        await message.answer(blanks.subscribe_message, reply_markup=markup_subscribe)"""

@rt.callback_query()
async def cquery(call: types.callback_query, state: FSMContext):
    global requests, last_message
    functions.add_to_db(call.from_user.id, users)
    requests = functions.save_db(requests, users)
    await functions.delete_old_message(call.from_user.id, last_message)
    if await functions.check_subscribe(bot, call, tokens.channels):
        if call.data == 'cancel':
            await state.clear()
            await bot.send_message(call.from_user.id, 'Админ-панель войспака:', reply_markup=markups.admin_panel)
        elif call.data == 'sub':
            await call.answer('гуд')
        elif call.data == 'list_voice':
            voice_ids.dump()
            res = voice_ids.load()
            res_names = '\n🔊'.join([key for key in res])
            print(res_names)
            text = f'Список гс в боте: {len(res)}/{tokens.bot_tarif.quantity} по тарифу {tokens.bot_tarif.name} \n🔊{res_names}'
            last_message[call.from_user.id] = await bot.send_message(call.from_user.id, text)
        elif call.data == 'add_voice':
            last_message[call.from_user.id] = await bot.send_message(call.from_user.id,blanks.add_voice)
            await state.set_state(classes.get_voice.audio)
        elif call.data == 'delete_voice':
            last_message[call.from_user.id] = await bot.send_message(call.from_user.id,blanks.delete_voice_text)
            await state.set_state(classes.delete_voice.name)

    else:
        await bot.send_message(call.from_user.id, blanks.subscribe_message, reply_markup=markup_subscribe)
@rt.message(classes.get_voice.audio)
async def audio_review(message: types.Message, state: FSMContext):
    await functions.delete_old_message(message.from_user.id, last_message)
    if len(voice_ids.list) == tokens.bot_tarif.quantity:
        last_message[message.from_user.id] = await message.answer(blanks.no_place_for_sound)
        await message.answer('Админ-панель войспака:', reply_markup=markups.admin_panel)
    elif message.caption in voice_ids.list.keys():
        last_message[message.from_user.id] = await message.answer(blanks.voice_already_here, reply_markup=markups.cancel)
    elif not message.audio:
        last_message[message.from_user.id] = await message.answer(blanks.no_audio_in_message, reply_markup=markups.cancel)
    elif message.audio.file_size > 5300000:
        last_message[message.from_user.id] = await message.answer(blanks.too_big_audio_in_message, reply_markup=markups.cancel)
    elif message.caption is None:
        last_message[message.from_user.id] = await message.answer(blanks.bad_audio_caption_in_message, reply_markup=markups.cancel)
    elif len(message.caption) > 50:
        last_message[message.from_user.id] = await message.answer(blanks.bad_audio_caption_in_message, reply_markup=markups.cancel)
    else:
        await bot.download(message.audio.file_id, f'{message.caption}.mp3')
        test_sending = await bot.send_voice(message.from_user.id, types.FSInputFile(f'{message.caption}.mp3'))
        voice_ids.list[message.caption] = test_sending.voice.file_id
        os.remove(f'{message.caption}.mp3')
        await state.clear()
        await message.answer(blanks.succesfully_adding_voice)
        await message.answer('Админ-панель войспака:', reply_markup=markups.admin_panel)

@rt.message(classes.delete_voice.name)
async def delete_audio_step1(message: types.Message, state: FSMContext):
    await functions.delete_old_message(message.from_user.id, last_message)
    res_ids = {}
    for name, id in voice_ids.list.items():
        res_ids[name] = tuple([len(set(query.query.lower().split()) & set(name.split())), id])
    searched = [(i) for i in tuple(sorted(res_ids.items(), key=lambda x: x[1][0], reverse=True)[0])][:1]
    # остановился тут
    await state.set_state(classes.delete_voice.yes_or_no)

@rt.inline_query()
async def inline(query: types.InlineQuery):
    global requests, stoping
    await functions.delete_old_message(query.from_user.id, last_message)
    functions.add_to_db(query.from_user.id, users)
    requests = functions.save_db(requests, users)
    if await functions.check_subscribe(bot, query, tokens.channels):
        res_ids = {}
        for name, id in voice_ids.list.items():
            res_ids[name] = tuple([len(set(query.query.lower().split()) & set(name.split())), id])
        searched = [(i) for i in tuple(sorted(res_ids.items(), key=lambda x: x[1][0], reverse=True)[0])]
        res = [types.InlineQueryResultCachedVoice(id=searched[0][:10], title=searched[0],voice_file_id=searched[1][1], reverse=True)]
        await query.answer(res)
    else:
        await query.answer([types.InlineQueryResultArticle(id="0", title='ПОДПИШИСЬ НА КАНАЛ', input_message_content=types.InputTextMessageContent(message_text='Чтобы пользоваться ботом подпишись на канал:\n\n@voicemessage_studio'))])

async def running():
    await dp.start_polling(bot)
run(running())