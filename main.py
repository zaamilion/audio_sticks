from asyncio import run
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import random
import sys
sys.path.insert(0,'z:\\pythonprojects\\audio_sticks\\path\\data')
import db
import tokens
import markups

stoping = False

dp = Dispatcher()
bot = Bot(token=tokens.TOKEN)

voice = db.Database('voices')
users = db.Database('users')
requests = 0
@dp.message(CommandStart())
async def start(message: types.Message):
    global requests
    requests += 1
    if requests == 10:
        users.dump()
        requests = 0
    if message.from_user.id not in users.list:
        users.list.append(message.from_user.id)
    if (await bot.get_chat_member(user_id=message.from_user.id, chat_id=-1002013605939)).status != 'left':
        if message.from_user.id == tokens.owner:
            print('wtf')
            await message.answer('Привет! Админ-панель войспака:', markup=markups.admin_panel)
    else:
        await message.answer('⚙️Подпишись на канал для пользования ботом:\n\n@voicemessage_studio', reply_markup=markups.markup_subscribe)

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
        await message.answer('⚙️Подпишись на канал для пользования ботом:\n\n@voicemessage_studio', reply_markup=markup_subscribe)"""

@dp.callback_query()
async def cquery(call: types.callback_query):
    global requests, stoping
    requests += 1
    if requests == 10:
        dp.dump()
        requests = 0
    if call.from_user.id not in users.list:
        users.list.append(call.from_user.id)
    if call.data == 'sub':
        if (await bot.get_chat_member(user_id=call.from_user.id, chat_id=-1002013605939)).status != 'left':
            await call.answer('гуд')
        else:
            await bot.send_message(call.from_user.id, '⚙️Подпишись на канал для пользования ботом:\n\n@voicemessage_studio', reply_markup=markup_subscribe)

@dp.inline_query()
async def inline(query: types.InlineQuery):
    global requests, stoping
    requests += 1
    if requests == 10:
        users.dump()
        requests = 0
    # добавление в бд
    if query.from_user.id not in users.list:
        users.list.append(query.from_user.id)
    if (await bot.get_chat_member(user_id=query.from_user.id, chat_id=-1002013605939)).status != 'left':
        res_ids = {}
        for name, id in voice_ids.items():
            res_ids[name] = tuple([len(set(query.query.lower().split()) & set(name.split())), id])
            #print(query.query, name, id)
        searched = [(i) for i in tuple(sorted(res_ids.items(), key=lambda x: x[1][0], reverse=True)[0])]
        res = [types.InlineQueryResultCachedVoice(id=searched[0][:10], title=searched[0],voice_file_id=searched[1][1], reverse=True)]
        #print(query.query, res, end='\n###################################\n')
        await query.answer(res)
    else:
        await query.answer([types.InlineQueryResultArticle(id="0", title='ПОДПИШИСЬ НА КАНАЛ', input_message_content=types.InputTextMessageContent(message_text='Чтобы пользоваться ботом подпишись на канал:\n\n@voicemessage_studio'))])
async def running():
    await dp.start_polling(bot)
run(running())