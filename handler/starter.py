from telethon import events, Button

import dbUtile.dbmanger as db
import handler.clinetbot as tg_client
import handler.helper as tg_basic

botClint = tg_client.botClint
client = tg_client.client


@events.register(events.NewMessage(incoming=True, pattern=r'(\/start)( user_id_(\d{8}))?'))
async def start(event):
    is_referable = event.pattern_match
    referral_link = is_referable.group(3)
    print(referral_link)
    sql_update = """UPDATE botInfo
   SET invitedby = ?
 WHERE userid = ?;"""
    # print(event.stringify())
    bot_user_id = event.peer_id.user_id
    sql_table = '''CREATE TABLE botInfo (
        userid       INTEGER,
        position       STRING,
        warn         BOOLEAN,
        baned        BOOLEAN,
        started      BOOLEAN,
        referalid    STRING,
        invitedby    STRING
    );'''
    sql_insert_start = """INSERT INTO botInfo (
                        userid,
                        started,
                        referalid
                    )
                    VALUES (?,
                    ?,
                    ?
                    );"""

    cone = db.create_connection('bot_info.db')
    values = (bot_user_id, True, tg_basic.rangen())
    friend = await botClint.get_entity(bot_user_id)
    if referral_link is None:
        if db.create_table(cone, sql_table):
            # print(friend.stringify())
            await botClint.send_message(
                message='Hi ' + friend.first_name + 'You are the first users please Join Channel To benefit from the '
                                                    'bot',
                entity=event.peer_id,
                buttons=[
                    [Button.url('Join', url='https://t.me/ALL_UNVERSITY_IN_ONE'), ],
                    [Button.inline(text='Done', data=b'done'), ]
                ])
            db.add_to_channel(cone, sql_insert_start, values)
            cone.close()
        elif tg_basic.is_started(bot_user_id):
            text_g = 'Hi ' + friend.first_name + ' wellcome back again I know you like this bot'
            text_b = 'Hi ' + friend.first_name + 'wellcome back again I know you like this bot ,but I still mad on ' \
                                                 'you , please join the channel '
            await message(text_g, text_b, event, bot_user_id)

        else:
            # await event.reply('hi', buttons=Button.clear())
            await event.respond('Someone wants war', buttons=Button.clear())
            await botClint.send_message(
                message='Hi ' + friend.first_name + 'if you are not yet joined the channel \n please Join Channel To '
                                                    'benefit from the bot '
                                                    '\n if you joined just press Done',
                entity=event.peer_id,
                buttons=[
                    [Button.url('Join', url='https://t.me/ALL_UNVERSITY_IN_ONE'), ],
                    [Button.inline(text='Done', data=b'done'), ]
                ])
            db.add_to_channel(cone, sql_insert_start, values)
            cone.close()
    else:
        if tg_basic.is_invited(cone, bot_user_id) is None:
            await message(None, None, event, bot_user_id)
            db.add_to_channel(cone, sql_insert_start, values)
            update_values = (tg_basic.is_owner(cone, referral_link), bot_user_id)
            db.update(cone, sql_update, update_values)
            cone.close()
        else:
            await event.respond('The User Already Invited')
            await message(None, None, event, bot_user_id)
            # db.add_to_channel(cone, sql_insert_start, values)
            # update_values = (referral_link, is_owner(cone, referral_link))
            # db.update(cone, sql_update, update_values)
            # cone.close()


async def message(text_g, text_b, event, bot_user_id):
    friend = await botClint.get_entity(bot_user_id)
    if text_g is None or text_b is None:
        text_g = 'Hi ' + friend.first_name + ' wellcome to this bot'
        text_b = 'Hi ' + friend.first_name + 'wellcome I know you like this bot ,but I still mad on you , please join ' \
                                             'the channel' \
                                             'if you joined just press Done'
    if await tg_basic.in_channel(bot_user_id):
        await botClint.send_message(
            message=text_g,
            entity=event.peer_id,
            buttons=[
                [Button.text(text='💸Make Money💸', resize=True), Button.text(text='🆘help🆘', resize=True)],
                [Button.text(text='👨🏾‍💻About🧑🏽‍💻', resize=True)],
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
