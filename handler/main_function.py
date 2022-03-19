from telethon import events

import handler.clinetbot as tg_client

botClint = tg_client.botClint
client = tg_client.client


@events.register(events.NewMessage(incoming=True, pattern=r'Make Money'))
async def make_money(event):
    await botClint.send_message(message='Not Yet Completed', entity=event.peer_id)


@events.register(events.NewMessage(incoming=True, pattern=r'About'))
async def about(event):
    await botClint.send_message(message='Not Yet Completed', entity=event.peer_id)


@events.register(events.NewMessage(incoming=True, pattern=r'help'))
async def helps(event):
    await botClint.send_message(message='Not Yet Completed', entity=event.peer_id)
