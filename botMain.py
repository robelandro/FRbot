import asyncio
import logging
import handler.main_function as main_function
import handler.inline_answer as inline_answer
import handler.clinetbot as tg_client
import handler.starter as tg_helper

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
bot_token = '1024253219:AAHO7JBCgnYrBRrJR7hNPClIMFWLkaWi2Q8'
botClint = tg_client.botClint
# client = tg_client.client

with botClint as opps:
    opps.add_event_handler(tg_helper.start)

with botClint as done:
    done.add_event_handler(inline_answer.done)

with botClint as m:
    m.add_event_handler(main_function.make_money)
with botClint as h:
    h.add_event_handler(main_function.helps)
with botClint as a:
    a.add_event_handler(main_function.about)

# with client as jl:
#     jl.add_event_handler(tg_helper.joined_leave)


def main():
    loop = asyncio.get_event_loop()

    botClint.start(bot_token=bot_token)
    # client.start()

    loop.run_forever()


if __name__ == '__main__':
    main()
