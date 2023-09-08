#Import modules
import logging, mmap, os, math, time, datetime, re, asyncio, random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
import aiogram.utils.markdown as ftm
from aiogram.utils.emoji import emojize
from aiogram.utils.markdown import code, italic, bold, pre
from aiogram.utils.markdown import text as my_font
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter
from aiogram.types import Message, chat_permissions, ChatType
from aiogram.utils.exceptions import BadRequest
from hashlib import *
from filter import IsAdminFilter
from random import choice, randint
from key import *
from datetime import timedelta

#Variables
from config import *
times = dict()
rep = dict()
to = 0

# Send admin message about bot started
async def send_adm(*args, **kwargs):
    await bot.send_message(chat_id=adminId, text='Bot started!')
    
#Functions
def exists(path):
    try:
        os.stat(path)
    except OSError:
        return False
    return True

def hash(string: str):
    hash = sha1(string.strip().encode('utf-8')).hexdigest()
    return hash

#Bot init
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

#Add admin filter
dp.filters_factory.bind(IsAdminFilter)

#Commands
inline_btn_1 = types.InlineKeyboardButton('достал', callback_data='data')
inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_1)

@dp.message_handler(commands=['жб'], commands_prefix='.')
async def process_command_1(message: types.Message):
    count = await message.chat.get_member_count()
    print(await message.chat.get_administrators())
    if message.reply_to_message:
        rep_us = "Пожаловаться на " + message.reply_to_message.from_user["first_name"]
        data =  str(message.chat.id) + 's' + str(message.reply_to_message.from_user.id) + 's' + str(count)
        
        inline_kb1 = types.InlineKeyboardMarkup()
        inline_kb1.add(types.InlineKeyboardButton('НАСТУЧАТЬ 💅🏻', callback_data = str(data)))
        await message.reply(rep_us, reply_markup = inline_kb1)
    else:
        await message.reply("❗️ Алло, ответь на сообщение чела.")

@dp.callback_query_handler()
async def process_callback_button1(callback: types.CallbackQuery):
    data_en = callback.data.split('s')[:2]
    count = int(callback.data.split('s')[2])
    try:
        rp = rep[str(data_en)]
    except:
        rp = 0
        rep[str(data_en)] = 0
    if rp <= count/2:
        rep[str(data_en)] += 1
        print(rep)
    else:
        print("ban: ", data_en[1])
        await bot.send_message(data_en[0], "😡 BAN" + str(data_en[1]))

        admins = await bot.get_chat_administrators(data_en[0])

        for admin in admins:
            if admin.status == "creator":
                #return admin
                print(admin)
                await bot.send_message("ban", admin.user.id)

    await bot.send_message(callback.from_user.id, 'Я на него пожаловалась, и думаю что скоро я его исключу.')

@dp.message_handler(commands=['message_to'], commands_prefix='!/')
async def message_to(message: types.Message):
    text = message.text.split()
    print(text)
    to = text[1]
    mes = text[2:]
    await message.delete()
    await bot.send_message(to, mes)
 
#KICK

@dp.message_handler(is_admin=True, commands=['ick'], commands_prefix='k',
                    chat_type=[ChatType.GROUP, ChatType.SUPERGROUP])
async def kick_user(message: Message):
    if not message.reply_to_message:
        return await message.reply('❗️ Алло, ответь на сообщение чела.')
    await message.delete()

    user_id = message.reply_to_message.from_user.id
    seconds = 600
    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=user_id, until_date=timedelta(seconds=seconds))
    return await message.reply_to_message.reply(f'Выгнала 🥵 ')
  
#MUTE
@dp.message_handler(is_admin=True, commands=['ute'], commands_prefix='m')
async def mute_chat_member(message: Message):
    if message.reply_to_message:
        member_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        OnlyReadPermissions = types.ChatPermissions(can_send_messages=False,
                                                    can_send_media_messages=False,
                                                    can_send_polls=False,
                                                    can_send_other_messages=False,
                                                    can_add_web_page_previews=False,
                                                    can_change_info=False,
                                                    can_invite_users=False,
                                                    can_pin_messages=False)
        command = re.compile(r"(mute) ?(\d+)? ?([a-zA-Zа-яА-Я ]+)?").match(message.text)
        time = command.group(2)
        comment = command.group(3)
        if not time:
            time = 30
        else:
            time = int(time)
        until_date = datetime.datetime.now() + datetime.timedelta(minutes=time)
        try:
            await bot.restrict_chat_member(chat_id=chat_id, user_id=member_id, permissions=OnlyReadPermissions, until_date=until_date)
            await message.reply(f'❗️ Пользователь был ограничен отправлять сообщения на {time} минут.\n')
        except BadRequest:
            await message.reply(f'❗️ Этому или себе не сможешь ограничить.')
    else:
        msg = await message.reply(f'❗️ Ответьть на сообщение кому хочешь дать мут! ')
        await asyncio.sleep(15)
        await msg.delete()


@dp.message_handler(is_admin=True, commands=['nmute'], commands_prefix='u')
async def mute_chat_member(message: Message):
    if message.reply_to_message:
        member_id = message.reply_to_message.from_user.id
        chat_id = message.chat.id
        chat_permission = (await bot.get_chat(message.chat.id)).permissions
        try:
            await bot.restrict_chat_member(chat_id=chat_id, user_id=member_id, permissions=chat_permission, until_date=datetime.datetime.now())
            await message.reply(f'❗️ Снова может писать\n')
        except BadRequest:
            await message.reply('f❗️ Его нельзя размутить!')
    else:
        msg = await message.reply(f'❗️ Ответь на сообщение кому хочешь убрать мут!')
        await asyncio.sleep(15)
        await msg.delete()

@dp.message_handler(commands=['нфо'], commands_prefix='и')
async def random(message: types.Message):
    await message.delete()
    await message.answer(help)

@dp.message_handler(is_admin=True, commands = ['l'], commands_prefix = 'b')
async def cmd_bl(message: types.Message):
    texte = message.text.lower()
    file_name = hash(str(message.chat.id))
    print(file_name)
    file_name += '.bl'
    ex = exists(data_dir + file_name)
    if not ex:
        with open(data_dir + file_name, 'w+', encoding='utf-8') as a:
            a.write(' ')
    await message.delete()
    if len(texte.split()) >=2:
        type = texte.split()[1]
    if len(texte.split()) >= 3:
        text = texte.lower().split()[2:]
        text_str = " ".join(text)
        if type == "add":
             await message.answer("Добавлено ✅")
             with open(data_dir + file_name, 'r', encoding='utf-8') as r:
                 t = r.read()
             with open(data_dir + file_name, 'w', encoding='utf-8') as w:
                 w.write(text_str + '\n' + t)
        elif type == "delete":
            await message.answer("Удалено ❌")
            with open(data_dir + file_name, 'r', encoding='utf-8') as r:
                t = r.read()
            with open(data_dir + file_name, 'w', encoding='utf-8') as w:
                w.write(t.replace(text_str + '\n', ''))
        #else:
           # await message.answer("Управление блэклистом:\n*добавить слово: !bl add [слово]\n*удалить солово: !BL delete[слово]\n*удалить все солва :!BL clear\n*список запрещёных слов: !BL list")
    else:
        if type == "clear":
            with open(data_dir + file_name, 'w', encoding='utf-8') as w:
                w.close()
            await message.answer("Очищено ♻️")
        elif type == "list":
            with open(data_dir + file_name, 'r', encoding='utf-8') as r:
                t = r.read()
            await message.answer(t)
       # else:
          #  await message.answer("Управление блэклистом:\n*добавить солво: !BL add [слово]\n*удалить солово: !BL delete[слово]\n*удалить все солва :!BL clear\n*список запрещёных слов: !BL list")

@dp.message_handler(is_admin = True, commands=['pam'], commands_prefix = 's')
async def cmd_spam(message: types.Message):
    if len(message.text.split()) >= 3:
        count = int(message.text.split()[1])
        text = message.text.split()[2:]
        text_str = " ".join(text)
        print("[spamed]" + str(count) + " - \"" + text_str + "\"")
        await message.delete()
        if count <= 25:
            for i in range(count):
                await message.answer(text_str)
        else:
            await message.answer("Не спамь много!")
    else:
        await message.answer("Норм введи команду, я не поняла.")

@dp.message_handler(commands=['chatid'],commands_prefix = '!/')
async def cmd_id(message: types.Message):
    print(message)
    await message.delete()
    await bot.send_message(message.from_user.id, message.chat.id)

@dp.message_handler(commands=['ls'],commands_prefix = '!/')
async def cmd_id(message: types.Message):
    print(message)
    await message.delete()
    if message.reply_to_message:
        await bot.send_message(message.from_user.id, "User\'s ID: " + str(message.reply_to_message.from_user.id)) 
    else:
        await bot.send_message(message.from_user.id, "Зайка ты! ")

@dp.message_handler(is_admin = True, commands=['jl'], commands_prefix = '!/')
async def cmd_echo(message: types.Message):
    text = message.text.split()[1:]
    text_str = " ".join(text)
    print(text)
    print(text_str)
    await message.delete()
    await message.answer(text_str)

@dp.message_handler(content_types = ["new_chat_members"])
async def on_user_joined(message: types.Message):
    print(message)
    await message.delete()
    user = message.new_chat_members
    bot = user[0]["is_bot"]
    if not bot:
        await message.answer("Приветик ❤️ " + user[0]["first_name"])

@dp.message_handler(is_admin = True, commands = ["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("❗️ Ответь на сообщение кого хочешь заблокировать.")
        return

    await message.bot.delete_message(message.chat.id, message.message_id)
    await message.bot.kick_chat_member(chat_id = message.chat.id, user_id = message.reply_to_message.from_user.id)
    await message.reply_to_message.reply(
        ftm.text(
            ftm.text(ftm.hboild("❗️ Те блокировка")),
            ftm.text(ftm.hunderline("/n от администратора ")),
            sep = "\n"), parse_mode = "HTML")



@dp.message_handler()
async def filter_message(message: types.Message):
    global to
    to = to
    t2 = time.time()
    try:
        t1 = times[str(message.from_user.id)]
    except:
        t1 = 2<<15
    times[str(message.from_user.id)] = time.time()
    dt = abs(t1 - t2)
    print(dt)
    if dt <= 0.75:
        await message.delete()
        if abs(to - time.time()) > 5:
            rep = my_font("Кошмар, не спамьте пж 🆘")
            await message.answer(rep, parse_mode=types.ParseMode.MARKDOWN)
            to = time.time()
    text = message.text.lower().split()
    print(message)
    file_name = hash(str(message.chat.id))
    print(file_name)
    file_name += '.bl'
    cens = open(data_dir + file_name, 'r', encoding='utf-8').read().splitlines()
    if len(message.text) > 500:
        rep = my_font("🆘Алло, не пиши такие длинные сообщения.")
        await message.reply(rep, parse_mode = types.ParseMode.MARKDOWN)
        print("Оч большое сообщение 🆘")
    for word in cens:
        delete = (word in text)
        if delete:
            rep = my_font ("Удалила, блин, не пишите такое больше пж.🆘🆘🆘 ")
            await message.reply(rep, parse_mode=types.ParseMode.MARKDOWN)
            await message.delete()
        if (delete and not message.entities != []) or len(message.text) > 500:
            await message.delete()
            break

@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    global to
    to = to
    t2 = time.time()
    try:
        t1 = times[str(message.from_user.id)]
    except:
        t1 = 2<<15
    times[str(message.from_user.id)] = time.time()
    dt = abs(t1 - t2)
    print(dt)
    if dt <= 0.75:
        await message.delete()
        if abs(to - time.time()) > 5:
            rep = my_font("Блин, не спамь ок 🆘")
            await message.answer(rep, parse_mode=types.ParseMode.MARKDOWN)
            to = time.time()
    print(message)
                      
   # get chat admins list               


#Run
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
