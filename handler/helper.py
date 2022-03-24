import logging
import random
from sqlite3 import Error
from sqlite3 import OperationalError

from telethon import Button
from telethon.errors import UserNotParticipantError

import dbUtile.dbmanger as db
import handler.clinetbot as tg_client

botClint = tg_client.botClint
# client = tg_client.client

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
loger = logging.getLogger()


def is_invited(connect, user_id):
    id_r = None
    sql_read_for = """SELECT userid
      FROM botInfo WHERE userid =""" + str(user_id) + ';'
    try:
        read_result = db.select(connect, sql_read_for)
        for op in read_result:
            id_r = op[0]
        return id_r
    except Error as e:
        loger.error(e)
        return id_r


def is_owner(connect, referral_link):
    id_r = None
    sql_read_owner = """SELECT userid
      FROM botInfo WHERE referalid =""" + str(referral_link) + ';'
    try:
        read_result = db.select(connect, sql_read_owner)
        for op in read_result:
            id_r = op[0]
        return id_r
    except Error as e:
        loger.error(e)
        return id_r


def is_started(user_id):
    cone = db.create_connection('bot_info.db')
    result = 0
    sql_read = """SELECT 
    started
    FROM botInfo WHERE userid =""" + str(user_id) + ';'
    x = db.select(cone, sql_read)
    for ir in x:
        result = ir[0]
    print(result)
    return result


# def is_joined(user_id):
#     cone = db.create_connection('bot_info.db')
#     result = 0
#     sql_read = """SELECT
#     joined
#     FROM botInfo WHERE userid =""" + str(user_id) + ';'
#     x = db.select(cone, sql_read)
#     for ir in x:
#         result = ir[0]
#     print(result)
#     return result


async def in_channel(user_id):
    print(user_id)
    try:
        print("yes")
        k = await botClint.get_input_entity('ALL_UNVERSITY_IN_ONE')
        await botClint.get_participants('ALL_UNVERSITY_IN_ONE')
        await botClint.get_permissions(entity=k.channel_id, user=user_id)
        return True
    except UserNotParticipantError as e:
        loger.error(e)
        return False


def rangen():
    def results_gen():
        t = []
        for x in range(8):
            h = random.randrange(1, 10)
            t.append(str(h))
        result = t[0] + t[1] + t[2] + t[3] + t[4] + t[5] + t[6] + t[7]
        return int(result)

    to_be_return = results_gen()
    cone = db.create_connection('bot_info.db')
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


def invitation_link(connect, user_id):
    id_r = None
    sql_read_for = """SELECT referalid
      FROM botInfo WHERE userid =""" + str(user_id) + ';'
    try:
        read_result = db.select(connect, sql_read_for)
        for op in read_result:
            id_r = op[0]
        return id_r
    except Error as e:
        print(e)
        return id_r


def invited_list(connect, invited_by):
    id_r = []
    sql_read_for = """SELECT userid
      FROM botInfo WHERE invitedby =""" + str(invited_by) + ';'
    try:
        read_result = db.select(connect, sql_read_for)
        for op in read_result:
            id_r.append(op[0])
        return id_r
    except Error as e:
        loger.error(e)
        return id_r


async def invited_list_name(connect, invited_by):
    first_name_of = []

    for user_id in invited_list(connect, invited_by):
        friend = await botClint.get_entity(user_id)
        first_name_of.append(friend.first_name)

    return first_name_of


async def invited_joined_list(connect, invited_by):
    list_of = []

    for user_id in invited_list(connect, invited_by):
        if await in_channel(user_id):
            list_of.append(True)
        else:
            list_of.append(False)
    return list_of


async def when_make_money(peer_id, first_name):
    await botClint.send_message(message=first_name + ' Choice One of them',
                                entity=peer_id,
                                buttons=[[Button.inline('🤼Invite Link🤼', b'i_link'),
                                          Button.inline('📒Info About Invited📒', b'iai'), ],
                                         [Button.inline('💸My Balance💸', b'money'),
                                          Button.inline('🏦WithDraw🏦', b'withdraw'), ],
                                         [Button.inline('🏠To Home🏠', b'home'),
                                          Button.inline('🔙Back🔙', b'back'), ], ])


def update_position(connect, user_id, position):
    sql_update = """UPDATE botInfo
   SET position = ?
 WHERE userid = ?;"""
    values = (position, user_id)
    db.update(connect, sql_update, values)


def get_position(connect, user_id):
    result = None
    sql_read = """SELECT position FROM botInfo WHERE userid =""" + str(user_id) + ';'
    x = db.select(connect, sql_read)
    for ir in x:
        result = ir[0]
    return result
