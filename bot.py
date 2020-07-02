import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import random
import time
import os
import sqlite3 as sq
import time
from datetime import datetime
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
API_TOKEN = '806775981:AAEcCZBL3ulrIEUcgJ8LfYVliIzIenEksUg'

# Configure logging
logging.basicConfig(level=logging.INFO)


class TS(Helper):
    mode = HelperMode.snake_case
    T_S1 = ListItem()
    T_S2 = ListItem()
    T_S3 = ListItem()


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

a = 0
ct = ' pip'
usid = 0
wlis = ['859850095', '898287979']

con = sq.connect(':memory:')
c = con.cursor()
c.execute("CREATE TABLE em(id integer, pol integer)")
con.commit()

con1 = sq.connect(':memory:')
c1 = con1.cursor()
c1.execute("CREATE TABLE om(id integer, p1 integer,p2 integer, p3 integer, p4 integer, p5 integer, p6 integer)")

con2 = sq.connect(':memory:')
c2 = con2.cursor()
c2.execute("CREATE TABLE sd(id integer, col integer, st integer)")
o = 0

con3 = sq.connect(":memory:")
ar = con3.cursor()
ar.execute("CREATE TABLE army(id integer, strong integer)")

conb = sq.connect(":memory:")
bu = conb.cursor()
bu.execute("CREATE TABLE bu(id integer, per1 integer, per2 text)")
@dp.message_handler(commands= ['start'])
async def ga(msg: types.message):
    c.execute("SELECT id FROM em WHERE id = ?", (msg.from_user.id,))
    r = c.fetchone()
    c_t = datetime.now()
    if r == None:
        c.execute("INSERT INTO em(id, pol) VALUES(?,?)", (msg.from_user.id, 100))
        c1.execute("INSERT INTO om(id,p1,p2,p3,p4,p5, p6) VALUES(?,?,?,?,?,?,?)", (msg.from_user.id,c_t.year, c_t.month,c_t.day,c_t.hour, c_t.minute, c_t.second))
        c2.execute("INSERT INTO sd(id, col, st) VALUES(?,?,?)", (msg.from_user.id, 1, 10))
        ar.execute("INSERT INTO army(id, strong) VALUES(?,?)",(msg.from_user.id,0))
        await msg.answer('Добро пожаловать в игру!')
    else:
        await msg.answer('Ты уже в игре!')

@dp.message_handler(commands=['moni'])
async def mo(msg :types.message ):
    c.execute("SELECT id FROM em WHERE id = ?",(msg.from_user.id,))
    r = c.fetchone()
    c_t = datetime.now()
    try:
        c1.execute("SELECT * FROM om WHERE id = ? ",(msg.from_user.id,))
        r = c1.fetchone()
        c.execute("SELECT pol FROM em WHERE id =?",(msg.from_user.id,))
        r1 = c.fetchone()
        c2.execute("SELECT col FROM sd WHERE id = ?",(msg.from_user.id,))
        r2 = c2.fetchone()
        global o
        o = ((c_t.year * 31536000+c_t.month * 2629743 + c_t.day * 86400 + c_t.hour * 3600+ c_t.minute * 60 + c_t.second) - (r[1] * 31536000 + r[2] * 2629743 + r[3] * 86400+ r[4] * 3600 + r[5] * 60 + r[6])) // 8
        c.execute("UPDATE em SET pol = ? WHERE id = ?",(r1[0]+o*r2[0],msg.from_user.id))
        print(o)
        print(r2[0])
        await msg.answer(""" ❗️Ты собрал деньги 💲
❕Денег собрано:%(a)i 💸
❕Твои деньги: %(b)i💰"""%{"a":o*r2[0], "b": r1[0]+o*r2[0]})
        c1.execute("UPDATE om SET p1 = ?, p2 = ?, p3 = ?,p4 = ?, p5 =?, p6 = ? WHERE id = ?",(c_t.year, c_t.month,c_t.day,c_t.hour,c_t.minute,c_t.second, msg.from_user.id))
    except:
        await msg.answer('Ты ещё не в игре! Чтобы начать игру напиши /start')
@dp.message_handler(commands= ['buy'])
async def buy(msg: types.message):
   try:
        c_t = datetime.now()
        i = msg.from_user.id

        c2.execute("SELECT * FROM sd WHERE id = ?", (msg.from_user.id,))
        r2 = c2.fetchone()
        c.execute("SELECT pol FROM em WHERE id = ?",(i,))
        r = c.fetchone()
        print(r2)
        print(r)
        if r[0] >= r2[2]:
            c2.execute("UPDATE sd SET col = ?, st = ? WHERE id = ?",(r2[1]+1, r2[2]+r2[2]//10, i))
            c.execute("UPDATE em SET pol = ? WHERE id = ?",(r[0]-r2[2],i))
            print(r[0] - r2[2])
            await msg.answer("""❗️Ты построил здание 🔨
❕Твои здания: %(x)i 🏛️
❕У тебя осталось денег: %(y)i 💰"""%{"x":r2[1]+1, "y":r[0]-r2[2]})

        else:
            await msg.answer("""❗️Не хватает денег!
❕ Нужно: %(x)i
💰 У тебя: %(y)i"""%{"x":r2[2], "y": r[0]})
   except:
       await msg.answer('Ты ещё не в игре! Чтобы начать игру напиши /start')

@dp.message_handler(commands= ['test'])
@dp.async_task
async def test(msg: types.message):
    a = 'удалить'
    b = 'выключено'
    i_b_1 = types.InlineKeyboardButton(a, callback_data='b1')
    i_b_2 = types.InlineKeyboardButton(b, callback_data= 'b2')
    i_k_1 = types.InlineKeyboardMarkup().add(i_b_1, i_b_2)
    print(msg.from_user.id)
    await msg.answer('Что хочешь узнать?', reply_markup = i_k_1)
    await asyncio.sleep(10)
    c_i = msg.chat.id
    m_i = msg.message_id +1
    await bot.delete_message(chat_id=c_i, message_id=m_i)

    @dp.callback_query_handler(lambda m: m.data == 'b1'  )
    async def l(m):
        print(m.from_user.id)
        await bot.edit_message_text(chat_id=m.message.chat.id, message_id=m.message.message_id, text=m.from_user.id)





@dp.message_handler(commands=['army'])
async def army(msg: types.message):
    try:
     ar.execute("SELECT strong FROM army WHERE id =?",(msg.from_user.id,))
     r = ar.fetchone()
     b_b = types.InlineKeyboardButton ("Усилить на 1", callback_data='a1')
     b_b1 = types.InlineKeyboardButton ("Усилить 10", callback_data='a2')
     b_b2 = types.InlineKeyboardButton("Усилить 25", callback_data='a3')
     b_b3 = types.InlineKeyboardButton("Усилить на 100", callback_data='a4')
     b_k = types.InlineKeyboardMarkup().add(b_b,b_b1,b_b2,b_b3)
     print(msg.message_id + 1)
     await msg.answer("@%(j)s Сила твоей армии: %(a)i"%{"j":msg.from_user.username, "a":r[0]}, reply_markup = b_k)
    except:
        await msg.answer("Ты ещё не начал игру!")
    @dp.callback_query_handler(lambda m: m.data == 'a1')
    async def barm(m):
        try:
          ar.execute("SELECT strong FROM army WHERE id =?", (m.from_user.id,))
          c.execute("SELECT pol FROM em WHERE id = ?", (m.from_user.id,))
          r = ar.fetchone()
          r1 = c.fetchone()
          if (r1[0]<10):
            await m.answer("""❗️Не хватает денег!
❕ Нужно: 10
💰 У тебя: %(g)i"""%{"g":r1[0]})
          else:
            c.execute("UPDATE em SET pol = ? WHERE id = ?",(r1[0]-10,m.from_user.id))
            ar.execute("UPDATE army SET strong = ? WHERE id = ?",(r[0]+1,m.from_user.id))
            await m.answer("Ты усилил армию! Теперь её сила равна: %(a)i"%{"a":r[0]+1})
            o = m.message.message_id
            print(o)
        except:
            await m.answer("Ты ещё не начал игру! Нажми /start и создай великую империю!")

    @dp.callback_query_handler(lambda m: m.data == 'a2')
    async def barm(m):
        try:
            ar.execute("SELECT strong FROM army WHERE id =?", (m.from_user.id,))
            c.execute("SELECT pol FROM em WHERE id = ?", (m.from_user.id,))
            r = ar.fetchone()
            r1 = c.fetchone()
            if (r1[0] < 100):
                await m.answer("""❗️Не хватает денег!
    ❕ Нужно: 100
    💰 У тебя: %(g)i""" % {"g": r1[0]})
            else:
                c.execute("UPDATE em SET pol = ? WHERE id = ?", (r1[0] - 100, m.from_user.id))
                ar.execute("UPDATE army SET strong = ? WHERE id = ?", (r[0] + 10, m.from_user.id))
                await m.answer("Ты усилил армию! Теперь её сила равна: %(a)i" % {"a": r[0] + 10})
                o = m.message.message_id
                print(o)
        except:
            await m.answer("Ты ещё не начал игру! Нажми /start и создай великую империю!")

    @dp.callback_query_handler(lambda m: m.data == 'a3')
    async def barm(m):
        try:
            ar.execute("SELECT strong FROM army WHERE id =?", (m.from_user.id,))
            c.execute("SELECT pol FROM em WHERE id = ?", (m.from_user.id,))
            r = ar.fetchone()
            r1 = c.fetchone()
            if (r1[0] < 250):
                await m.answer("""❗️Не хватает денег!
    ❕ Нужно: 250
    💰 У тебя: %(g)i""" % {"g": r1[0]})
            else:
                c.execute("UPDATE em SET pol = ? WHERE id = ?", (r1[0] - 250, m.from_user.id))
                ar.execute("UPDATE army SET strong = ? WHERE id = ?", (r[0] + 25, m.from_user.id))
                await m.answer("Ты усилил армию! Теперь её сила равна: %(a)i" % {"a": r[0] + 25})
                o = m.message.message_id
                print(o)
        except:
            await m.answer("Ты ещё не начал игру! Нажми /start и создай великую империю!")

    @dp.callback_query_handler(lambda m: m.data == 'a4')
    async def barm(m):
        try:
            ar.execute("SELECT strong FROM army WHERE id =?", (m.from_user.id,))
            c.execute("SELECT pol FROM em WHERE id = ?", (m.from_user.id,))
            r = ar.fetchone()
            r1 = c.fetchone()
            if (r1[0] < 1000):
                await m.answer("""❗️Не хватает денег!
    ❕ Нужно: 1000
    💰 У тебя: %(g)i""" % {"g": r1[0]})
            else:
                c.execute("UPDATE em SET pol = ? WHERE id = ?", (r1[0] - 1000, m.from_user.id))
                ar.execute("UPDATE army SET strong = ? WHERE id = ?", (r[0] + 100, m.from_user.id))
                await m.answer("Ты усилил армию! Теперь её сила равна: %(a)i" % {"a": r[0] + 100})
                o = m.message.message_id
                print(o)
        except:
            await m.answer("Ты ещё не начал игру! Нажми /start и создай великую империю!")


@dp.message_handler(commands='battle')
async def but(msg: types.message):
    try:
      m_i = msg.message_id +1
      bu.execute("INSERT INTO bu(id, per1,per2) VALUES(?,?,?)",(m_i, msg.from_user.id, msg.from_user.username))
      print(msg.from_user.id)
      s_b = InlineKeyboardButton("Вступить в битву!", callback_data='sb')
      s_k = InlineKeyboardMarkup().add(s_b)
      print(msg.message_id)
      await msg.answer("@%(a)s приглашает на битву!"%{"a":msg.from_user.username}, reply_markup=s_k)
    except:
        await msg.answer("Ты ещё не начал игру!")
    @dp.callback_query_handler(lambda m: m.data == 'sb')
    async def bitva(m):
    #   try:
            ar.execute("SELECT strong FROM army WHERE id=?",(m.from_user.id,))
            p2 = ar.fetchone()
            bu.execute("SELECT per1, per2 FROM bu WHERE id = ?", (m.message.message_id,))
            i1 = bu.fetchone()
            print(m.message.message_id)
            print(i1)
            if i1 == None:
                 bu.execute("SELECT per1, per2 FROM bu WHERE id = ?", (m.message.message_id,))
                 i1 = bu.fetchone()
            ar.execute("SELECT strong FROM army WHERE id=?", (i1[0],))
            p1 = ar.fetchone()
            if (m.from_user.id == i1[0]):
                await m.answer ("Ты не можешь биться сам с собой!")
            else:
                  await bot.edit_message_text(chat_id= m.message.chat.id, message_id=m.message.message_id , text = """❗️Началась жестокая битва!
⚔️ @%(x)s vs @%(y)s ⚔️
❕Идёт расчёт результатов..."""%{"x":i1[1],"y":m.from_user.username})
                  if (p1[0] > p2[0]):
                      print(p1[0])
                      print(p2[0])
                      r1=p1[0]-p2[0]
                      r2=0
                      ar.execute("UPDATE army SET strong = ? WHERE id = ?",(r1,i1[0]))
                      ar.execute("UPDATE army SET strong = ? WHERE id = ?",(r2, m.from_user.id))
                      bu.execute("DELETE FROM bu WHERE id = ?",(m.message.message_id,))
                      await asyncio.sleep(3)
                      await bot.edit_message_text(chat_id= m.message.chat.id, message_id= m.message.message_id, text = '🏆Победил @%(x)s!🏆'%{"x":i1[1]})
                      c.execute("SELECT pol FROM em WHERE id = ?",(i1[0],))
                      moni = c.fetchone()
                      c2.execute("SELECT col FROM  sd WHERE id = ?",(i1[0],))
                      uvel = c2.fetchone()
                      ne = moni[0]+uvel[0] * 5
                      c.execute("UPDATE em SET pol = ? WHERE id = ?",(ne,i1[0]))
                      await bot.send_message(i1[0],'Ты победил!')
                  elif (p1[0]<p2[0]):
                      print(p1[0])
                      print(p2[0])
                      r2 = p2[0] - p1[0]
                      r1 = 0
                      ar.execute("UPDATE army SET strong = ? WHERE id = ?", (r1, i1[0]))
                      ar.execute("UPDATE army SET strong = ? WHERE id = ?", (r2, m.from_user.id))
                      bu.execute("DELETE FROM bu WHERE id = ?", (m.message.message_id,))
                      await asyncio.sleep(3)
                      await bot.edit_message_text(chat_id=m.message.chat.id, message_id=m.message.message_id, text='🏆Победил @%(x)s!🏆' % {"x": m.from_user.username})
                      c.execute("SELECT pol FROM em WHERE id = ?", (m.from_user.id,))
                      moni = c.fetchone()
                      c2.execute("SELECT col FROM sd WHERE id = ?", (m.from_user.id,))
                      uvel = c2.fetchone()
                      ne = moni[0] + uvel[0] * 5
                      c.execute("UPDATE em SET pol = ? WHERE id = ?", (ne,m.from_user.id))
                      await bot.send_message(m.from_user.id, 'Ты победил!')
                  elif (p1[0] == p2[0]):
                      r2 = 0
                      r1 = 0
                      ar.execute("UPDATE army SET strong = ? WHERE id = ?", (r1, i1[0]))
                      ar.execute("UPDATE army SET strong = ? WHERE id = ?", (r2, m.from_user.id))
                      bu.execute("DELETE FROM bu WHERE id = ?", (m.message.message_id,))
                      await asyncio.sleep(3)
                      await bot.edit_message_text(chat_id=m.message.chat.id, message_id=m.message.message_id,text='🤝Ничья! Никто не одержал победу!🤝')
                      await bot.send_message(m.from_user.id, 'Ничья!')
                      await bot.send_message(i1[0], 'Ничья!')
      # except:
         #  await m.answer('Ты ещё не начал игру! ')







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


