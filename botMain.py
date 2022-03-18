import asyncio
import logging

import handler.clinetbot as tg_client
import handler.helper as tg_helper

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
botClint = tg_client.botClint
client = tg_client.client

with botClint as opps:
    opps.add_event_handler(tg_helper.start)

with botClint as done:
    done.add_event_handler(tg_helper.done)

with botClint as m:
    m.add_event_handler(tg_helper.make_money)
with botClint as h:
    h.add_event_handler(tg_helper.helps)
with botClint as a:
    a.add_event_handler(tg_helper.about)

# with client as jl:
#     jl.add_event_handler(tg_helper.joined_leave)


def main():
    loop = asyncio.get_event_loop()

    botClint.start()
    client.start()

    loop.run_forever()


if __name__ == '__main__':
    main()
