from sqlite3 import OperationalError

from telethon.errors import UserNotParticipantError
from telethon import events, Button

import os
import random
import dbUtile.dbmanger as db
import handler.clinetbot as tg_client
import asyncio

botClint = tg_client.botClint
client = tg_client.client


@events.register(events.NewMessage(incoming=True, pattern=r'\/start'))
async def start(event):
    bot_user_id = event.peer_id.user_id
    sql_table = '''CREATE TABLE botInfo (
        userid       INTEGER,
        joined       BOOLEAN,
        warn         BOOLEAN,
        baned        BOOLEAN,
        started      BOOLEAN,
        referalid    INTEGER,
        programState BOOLEAN
    );'''
    sql_insert_start = """INSERT INTO botInfo (
                        userid,
                        joined,
                        started,
                        referalid
                    )
                    VALUES (?,
                    ?,
                    ?,
                    ?
                    );"""
    os.chdir('.')
    cone = db.create_connection(os.getcwd() + '\\' + 'bot_info.db')
    values = (bot_user_id, False, True, rangen())
    friend = await botClint.get_entity(bot_user_id)
    if db.create_table(cone, sql_table):
        # print(friend.stringify())
        await botClint.send_message(
            message='Hi ' + friend.first_name + ' You are the first users please Join Channel To benefit from the bot',
            entity=event.peer_id,
            buttons=[
                [Button.url('Join', url='https://t.me/ALL_UNVERSITY_IN_ONE'), ],
                [Button.inline(text='Done', data=b'done'), ]
            ])
        db.add_to_channel(cone, sql_insert_start, values)
        cone.close()
    elif is_started(bot_user_id):
        text_g = 'Hi ' + friend.first_name + ' wellcome back again I know you like this bot'
        text_b = 'Hi ' + friend.first_name + ' wellcome back again I know you like this bot ,but I still mad on you , please join the channel'
        if await in_channel(bot_user_id):
            await botClint.send_message(
                message=text_g,
                entity=event.peer_id,
                buttons=[
                    [Button.text(text='Make Money', resize=True), Button.text(text='help', resize=True)],
                    [Button.text(text='About', resize=True)]
                ])
        else:
            await event.respond('Someone wants war', buttons=Button.clear())
            # await event.reply('hi', buttons=Button.clear())
            await botClint.send_message(
                message=text_b,
                entity=event.peer_id,
                buttons=[
                    [Button.url('Join', url='https://t.me/ALL_UNVERSITY_IN_ONE'), ],
                    [Button.inline(text='Done', data=b'done'), ]
                ])

    else:
        # await event.reply('hi', buttons=Button.clear())
        await event.respond('Someone wants war', buttons=Button.clear())
        await botClint.send_message(
            message='Hi ' + friend.first_name + 'if you are not yet joined the channel \n please Join Channel To benefit from the bot '
                                                '\n if you joined just press Done',
            entity=event.peer_id,
            buttons=[
                [Button.url('Join', url='https://t.me/ALL_UNVERSITY_IN_ONE'), ],
                [Button.inline(text='Done', data=b'done'), ]
            ])
        db.add_to_channel(cone, sql_insert_start, values)
        cone.close()


@events.register(events.NewMessage(outgoing=True, pattern=r'\.update_bot_info'))
async def uptodate(event):
    await client.edit_message(event.message, 'processing....')
    await update_bot_info()
    await event.reply('Success')


# @events.register(events.NewMessage())
# async def joined_leave(event):
#     print(event.stringify())


async def update_bot_info():
    count = 0
    os.chdir('.')
    cone = db.create_connection(os.getcwd() + '\\' + 'bot_info.db')
    sql_add = """INSERT INTO botInfo (
                        userid,
                        joined
                    )
                    VALUES (
                        ?,
                        True);"""
    async for users in client.iter_participants(1193023700):
        result = (str(users.id),)
        with cone:
            db.add_to_channel(cone, sql_add, result)
        await asyncio.sleep(0.1)
        count += 1
        print(f'Iter at :{count}')


def is_started(user_id):
    os.chdir('.')
    cone = db.create_connection(os.getcwd() + '\\' + 'bot_info.db')
    result = 0
    sql_read = """SELECT 
    started
    FROM botInfo WHERE userid =""" + str(user_id) + ';'
    x = db.select(cone, sql_read)
    for ir in x:
        result = ir[0]
    print(result)
    return result


def is_joined(user_id):
    os.chdir('.')
    cone = db.create_connection(os.getcwd() + '\\' + 'bot_info.db')
    result = 0
    sql_read = """SELECT 
    joined
    FROM botInfo WHERE userid =""" + str(user_id) + ';'
    x = db.select(cone, sql_read)
    for ir in x:
        result = ir[0]
    print(result)
    return result


async def in_channel(user_id):
    print(user_id)
    try:
        print("yes")
        await botClint.get_participants('ALL_UNVERSITY_IN_ONE')
        result = await botClint.get_permissions(entity=1193023700, user=user_id)
        return True
    except UserNotParticipantError as e:
        print(e)
        return False


def rangen():
    os.chdir('.')

    def results_gen():
        t = []
        for x in range(8):
            h = random.randrange(9)
            t.append(str(h))
        result = t[0] + t[1] + t[2] + t[3] + t[4] + t[5] + t[6] + t[7]
        return int(result)

    to_be_return = results_gen()
    cone = db.create_connection(os.getcwd() + '\\' + 'bot_info.db')
    sql_read = """SELECT referalid FROM botInfo;"""

    with cone:
        try:
            list_to_check = db.select(cone, sql_read)
        except OperationalError as er:
            return to_be_return
        for k in list_to_check:
            while k[0] == to_be_return:
                to_be_return = results_gen()
    return to_be_return


@events.register(events.CallbackQuery)
async def done(event):
    # print(event.stringify())
    bot_user_id = event.original_update.peer.user_id
    friend = await botClint.get_entity(bot_user_id)
    if event.data == b'done':
        text_g = 'Hi ' + friend.first_name + ' wellcome back again I know you like this bot'
        text_b = 'Hi ' + friend.first_name + ' wellcome back again I know you like this bot ,but I still mad on you , please join the channel'
        if await in_channel(bot_user_id):
            await botClint.send_message(
                message=text_g,
                entity=event.original_update.peer,
                buttons=[
                    [Button.text(text='Make Money', resize=True), Button.text(text='help', resize=True)],
                    [Button.text(text='About', resize=True)]
                ])
        else:
            await event.respond('Someone wants war', buttons=Button.clear())
            # await event.reply('hi', buttons=Button.clear())
            await botClint.send_message(
                message=text_b,
                entity=event.original_update.peer,
                buttons=[
                    [Button.url('Join', url='https://t.me/ALL_UNVERSITY_IN_ONE'), ],
                    [Button.inline(text='Done', data=b'done'), ]
                ])


@events.register(events.NewMessage(incoming=True, pattern=r'Make Money'))
async def make_money(event):
    await botClint.send_message(message='Not Yet Completed', entity=event.peer_id)


@events.register(events.NewMessage(incoming=True, pattern=r'About'))
async def about(event):
    await botClint.send_message(message='Not Yet Completed', entity=event.peer_id)


@events.register(events.NewMessage(incoming=True, pattern=r'help'))
async def helps(event):
    await botClint.send_message(message='Not Yet Completed', entity=event.peer_id)
