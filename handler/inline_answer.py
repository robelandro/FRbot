from telethon import events, Button

import dbUtile.dbmanger as db
import handler.clinetbot as tg_client
import handler.helper as tg_basic

botClint = tg_client.botClint
client = tg_client.client

markup_button = [[Button.inline('🏠To Home🏠', b'home'), Button.inline('🔙Back🔙', b'back'), ], ]


@events.register(events.CallbackQuery)
async def done(event):
    cone = db.create_connection('bot_info.db')
    # print(event.stringify())
    bot_user_id = event.original_update.peer.user_id
    friend = await botClint.get_entity(bot_user_id)
    text_g = 'Hi ' + friend.first_name + ' wellcome back again I know you like this bot'
    text_b = 'Hi ' + friend.first_name + 'wellcome back again I know you like this bot ,but I still mad on you , ' \
                                         'please join the channel '
    if await tg_basic.in_channel(bot_user_id):
        if event.data == b'done':
            await good_message(event, text_g)
        if event.data == b'i_link':
            await for_link(event, cone, bot_user_id)
        if event.data == b'home':
            await good_message(event, text_g)
        if event.data == b'iai':
            await fro_information(event, cone, bot_user_id)
        if event.data == b'money':
            await for_money(event, cone, bot_user_id)
        if event.data == b'withdraw':
            await for_withdraw(event, cone, bot_user_id)
        if event.data == b'back':
            if tg_basic.get_position(cone, bot_user_id) == 'MakeMoney':
                tg_basic.update_position(cone, bot_user_id, 'Home')
                await event.edit(friend.first_name + ' Choice One of them',
                                 buttons=[[Button.inline('🤼Invite Link🤼', b'i_link'),
                                           Button.inline('📒Info About Invited📒', b'iai'), ],
                                          [Button.inline('💸My Balance💸', b'money'),
                                           Button.inline('🏦WithDraw🏦', b'withdraw'), ],
                                          [Button.inline('🏠To Home🏠', b'home'),
                                           Button.inline('🔙Back🔙', b'back'), ], ]
                                 )
            else:
                await good_message(event, text_g)
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


async def good_message(event, textg):
    await event.edit(
        textg)
    await botClint.send_message(message='🏠home sweet home🏠',
                                entity=event.original_update.peer,
                                buttons=[
                                    [Button.text(text='💸Make Money💸', resize=True),
                                     Button.text(text='🆘help🆘', resize=True)],
                                    [Button.text(text='👨🏾‍💻About🧑🏽‍💻', resize=True)],
                                ])


async def formatted(invited_by):
    result = ''
    cone = db.create_connection('bot_info.db')
    n = await tg_basic.invited_list_name(cone, invited_by)
    j = await tg_basic.invited_joined_list(cone, invited_by)
    if len(n) == len(j):
        for x in range(len(n)):
            if j[x]:
                v = 'Joined'
            else:
                v = 'Not Joined'
            result += n[x] + ' | ' + v + '\n'
        result += 'Total :' + str(len(n))
        return result
    else:
        result = 'Something wrong'
        return result


async def account(invited_by):
    cone = db.create_connection('bot_info.db')
    result = 0
    j = await tg_basic.invited_joined_list(cone, invited_by)
    for k in j:
        if k:
            result += 4
    return result


async def for_link(event, cone, bot_user_id):
    tg_basic.update_position(cone, bot_user_id, 'MakeMoney')
    # tg_client.previous_position = tg_client.current_position
    # tg_client.current_position = 'Invite_link'
    await event.edit('Your Invitation Link Would be :\n\n'
                     'http://t.me/Spam_loyal_bot?start=user_id_'
                     + str(tg_basic.invitation_link(cone, bot_user_id)) + '\n\n' +
                     'If your invited friends joined the telegram , you will get 4 birr for each person ',
                     buttons=markup_button,
                     link_preview=False)


async def fro_information(event, cone, bot_user_id):
    tg_basic.update_position(cone, bot_user_id, 'MakeMoney')
    # tg_client.previous_position = tg_client.current_position
    # tg_client.current_position = 'Information'
    await event.edit('Your invited status would :\n\n' + await formatted(bot_user_id),
                     buttons=markup_button)


async def for_money(event, cone, bot_user_id):
    tg_basic.update_position(cone, bot_user_id, 'MakeMoney')
    # tg_client.previous_position = tg_client.current_position
    # tg_client.current_position = 'Account'
    await event.edit('Your account balance : ' + str(await account(bot_user_id)) + ' birr\n' +
                     'You can with withdraw your money after your reached 50 birr and above',
                     buttons=markup_button)


async def for_withdraw(event, cone, bot_user_id):
    tg_basic.update_position(cone, bot_user_id, 'MakeMoney')
    # tg_client.previous_position = tg_client.current_position
    # tg_client.current_position = 'Withdraw'
    if 50 <= await account(bot_user_id):
        await event.edit('Please  Contact @Human_is_code : \n '
                         'We Currently Supported Telebir And Cbe Birr',
                         buttons=markup_button)
    else:
        await event.edit(
            'You Have not reach 50 birr and above and make sure all your invited friends are joined the '
            'channel , if you have doubt Please  Contact @Human_is_code '
            , buttons=markup_button)
