
# @events.register(events.NewMessage(outgoing=True, pattern=r'\.update_bot_info'))
# async def uptodate(event):
#     await client.edit_message(event.message, 'processing....')
#     await update_bot_info()
#     await event.reply('Success')


# @events.register(events.NewMessage())
# async def joined_leave(event):
#     print(event.stringify())


# async def update_bot_info():
#     count = 0
#
#     cone = db.create_connection('bot_info.db')
#     sql_add = """INSERT INTO botInfo (
#                         userid,
#                         joined
#                     )
#                     VALUES (
#                         ?,
#                         True);"""
#     async for users in client.iter_participants(1193023700):
#         result = (str(users.id),)
#         with cone:
#             db.add_to_channel(cone, sql_add, result)
#         await asyncio.sleep(0.1)
#         count += 1
#         print(f'Iter at :{count}')


# @events.register(events.NewMessage(incoming=True, pattern=r'\.conve'))
# async def conve(event):
#     bot_user_id = event.peer_id.user_id
#     async with botClint.conversation(entity=event.peer_id) as con:
#         if await in_channel(bot_user_id):
#             await con.send_message(message='hello',
#                                        buttons=[[Button.text('Hello what is your name', resize=True), ], ])
#             res = await con.get_response()
#             print(res.stringify())
#             if res.message == 'Hello what is your name':
#                 await con.send_message(message='hello',
#                                            buttons=[[Button.text('Done', resize=True), ], ])
#                 resn = await con.get_response()
#                 if resn.message == 'Done':
#                     await con.send_message(message='Thanks',
#                                                buttons=Button.clear())
