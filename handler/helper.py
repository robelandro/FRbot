from telethon import events, Button
import os
from pprint import pprint

from telethon.errors import UserNotParticipantError

import dbUtile.dbmanger as db
import handler.clinetbot as tg_client
import asyncio

botClint = tg_client.botClint
client = tg_client.client


@events.register(events.NewMessage(incoming=True, pattern=r'\/start'))
async def start(event):
    await in_channel(event.peer_id.user_id)
    # print(event.stringify())
    sql_table = '''CREATE TABLE botInfo (
    userid       INTEGER,
    joined       BOOLEAN,
    warn         BOOLEAN,
    baned        BOOLEAN,
    started      BOOLEAN,
    referalid    INTEGER,
    programState BOOLEAN
);'''
    sql_read_start = """
    SELECT 
       started
  FROM botInfo WHERE userid = """ + str(event.peer_id.user_id) + ';'
    sql_insert_start = """UPDATE botInfo
    SET started = TRUE
    WHERE userid =?;"""
    os.chdir('.')
    cone = db.create_connection(os.getcwd() + '\\' + 'bot_info.db')
    user_id = (event.peer_id.user_id,)
    friend = await botClint.get_entity(event.peer_id.user_id)
    if db.create_table(cone, sql_table):
        # print(friend.stringify())
        await update_bot_info()
        await botClint.send_message(message='Hi ' + friend.first_name + ' please Join Channel To benefit from the bot',
                                    entity=event.peer_id,
                                    buttons=[
                                        [Button.url('Join', url='https://t.me/ALL_UNVERSITY_IN_ONE'), ],
                                        [Button.inline(text='Done', data=b'done'), ]
                                    ])
        db.add_to_channel(cone, sql_insert_start, user_id)
        cone.close()
    if is_started(event.peer_id.user_id):
        print("pressed")
        text_g = 'Hi ' + friend.first_name + ' wellcome back again I know you like this bot'
        text_b = 'Hi ' + friend.first_name + ' wellcome back again I know you like this bot ,but I still mad on you , please join the channel'
        if is_joined(event.peer_id.user_id):
            await botClint.send_message(
                message=text_g,
                entity=event.peer_id,
                buttons=[
                    [Button.text(text='Make Money', resize=True), Button.text(text='help', resize=True)],
                    [Button.text(text='About', resize=True)]
                ])
        else:
            await botClint.send_message(
                message=text_b,
                entity=event.peer_id,
                buttons=[
                    [Button.url('Join', url='https://t.me/ALL_UNVERSITY_IN_ONE'), ],
                    [Button.inline(text='Done', data=b'done'), ]
                ])
    else:
        await botClint.send_message(message='Hi ' + friend.first_name + ' please Join Channel To benefit from the bot',
                                    entity=event.peer_id,
                                    buttons=[
                                        [Button.url('Join', url='https://t.me/ALL_UNVERSITY_IN_ONE'), ],
                                        [Button.inline(text='Done', data=b'done'), ]
                                    ])


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
        await botClint.get_participants('ALL_UNVERSITY_IN_ONE')
        result = await botClint.get_permissions(entity=1193023700, user=user_id)
        if result.has_default_permissions:
            print('yes')
        else:
            print('no')
    except UserNotParticipantError as e:
        print(e)

