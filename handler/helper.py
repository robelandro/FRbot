import random
from sqlite3 import Error
from sqlite3 import OperationalError

from telethon.errors import UserNotParticipantError

import dbUtile.dbmanger as db
import handler.clinetbot as tg_client

botClint = tg_client.botClint
client = tg_client.client


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
        e.with_traceback()
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
        e.with_traceback()
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


def is_joined(user_id):
    cone = db.create_connection('bot_info.db')
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
        await botClint.get_permissions(entity=1193023700, user=user_id)
        return True
    except UserNotParticipantError as e:
        print(e)
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
