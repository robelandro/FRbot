from telethon import events, Button

import handler.clinetbot as tg_client
import handler.helper as tg_basic

botClint = tg_client.botClint
client = tg_client.client


@events.register(events.NewMessage(incoming=True, pattern=r'Make Money'))
async def make_money(event):
    bot_user_id = event.peer_id.user_id
    friend = await botClint.get_entity(bot_user_id)
    text_b = 'Hi ' + friend.first_name + 'wellcome I know you like this bot ,but I still mad on you , please join ' \
                                         'the channel' \
                                         'if you joined just press Done'
    if await tg_basic.in_channel(bot_user_id):
        await event.respond('💰', buttons=Button.clear())
        # await botClint.send_message(message='Not Yet Completed', entity=event.peer_id)
        await botClint.send_message(message=friend.first_name + ' Choice One of them',
                                    entity=event.peer_id,
                                    buttons=[[Button.inline('🤼Invite Link🤼', b'i_link'), Button.inline('📒Info About Invited📒', b'iai'), ],
                                             [Button.inline('💸My Money💸', b'money'), Button.inline('🏦WithDraw🏦', b'withdraw'), ],
                                             [Button.inline('🏠To Home🏠', b'home'), Button.inline('🔙Back🔙', b'back'), ], ])
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


@events.register(events.NewMessage(incoming=True, pattern=r'About'))
async def about(event):
    text = """About:
🖋<i>This bot is developed by @Human_is_code</i>
© Copyright 2022 Nftalem Revision
🔸<b>Built</b> Using Telethon Telegram Client library"""
    bot_user_id = event.peer_id.user_id
    if await tg_basic.in_channel(bot_user_id):
        await botClint.send_message(message=text, entity=event.peer_id,parse_mode='html')


@events.register(events.NewMessage(incoming=True, pattern=r'help'))
async def helps(event):
    bot_user_id = event.peer_id.user_id
    if await tg_basic.in_channel(bot_user_id):
        await botClint.send_message(message='Please  Contact @Human_is_code ', entity=event.peer_id)
