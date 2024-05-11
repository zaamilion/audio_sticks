import tariffs
async def check_subscribe(bot,message,channels_id):
    for channel in channels_id:
        if (await bot.get_chat_member(user_id=message.from_user.id, chat_id=channel)).status == 'left':
            return False
    return True
def add_to_db(user_id, database):
    if user_id not in database.list.keys():
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

def get_tarif_idx(call, users):
    for i in range(len(users.list[call.from_user.id][0].bot_tarifs)):
        if users.list[call.from_user.id][0].bot_tarifs[i][0].name == call.data:
            return i

def to_classs(dic):
    self = tariffs.Tarif('',0,0,[])
    self.name = dic['name']
    self.quantity = dic['quantity']
    self.price = dic['price']
    for key, value in dic['bot_tarifs']:
        self.bot_tarifs.append([tariffs.BotTarif(**key), value])
    return self