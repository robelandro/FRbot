from telethon import events, Button

import dbUtile.dbmanger as db
import handler.clinetbot as tg_client
import handler.helper as tg_basic

botClint = tg_client.botClint
client = tg_client.client

cone = db.create_connection('bot_info.db')
markup_button = [[Button.inline('🏠To Home🏠', b'home'), Button.inline('🔙Back🔙', b'back'), ], ]


@events.register(events.CallbackQuery)
async def done(event):
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
            await event.edit('Your Invitation Link Would be :\n\n'
                             'http://t.me/Spam_loyal_bot?start=user_id='
                             + str(tg_basic.invitation_link(cone, bot_user_id)) + '\n',
                             buttons=markup_button,
                             link_preview=False)
        if event.data == b'home':
            await good_message(event, text_g)
        if event.data == b'iai':
            await event.edit('Your invited status would :\n\n',
                             buttons=markup_button)
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


async def good_message(event, text):
    await event.edit(
        message=text,
        entity=event.original_update.peer,
        buttons=[
            [Button.text(text='Make Money', resize=True), Button.text(text='help', resize=True)],
            [Button.text(text='About', resize=True)]
        ])
def formatted():
