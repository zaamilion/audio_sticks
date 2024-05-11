import tariffs
async def check_subscribe(bot,message,channels_id):
    for channel in channels_id:
        if (await bot.get_chat_member(user_id=message.from_user.id, chat_id=channel)).status == 'left':
            return False
    return True
def add_to_db(user_id, database):
    if user_id not in database.list:
        database.list[user_id] = [tariffs.default, []]

def save_db(num, database):
    if num != 10:
        num += 1
        return num
    database.dump()
    return num + 1

async def delete_old_message(user, messages):
    try:
        await messages[user].delete()
    except:
        return False

def get_tariff(call, users):
    for tariff in users.list[call.from_user.id][0].bot_tarifs:
        if tariff.name == call.data:
            return tariff