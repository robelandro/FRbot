from telethon import events, Button

import handler.clinetbot as tg_client
import handler.helper as tg_basic

botClint = tg_client.botClint
client = tg_client.client


@events.register(events.CallbackQuery)
async def done(event):
    # print(event.stringify())
    bot_user_id = event.original_update.peer.user_id
    friend = await botClint.get_entity(bot_user_id)
    if event.data == b'done':
        text_g = 'Hi ' + friend.first_name + ' wellcome back again I know you like this bot'
        text_b = 'Hi ' + friend.first_name + 'wellcome back again I know you like this bot ,but I still mad on you , ' \
                                             'please join the channel '
        if await tg_basic.in_channel(bot_user_id):
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
