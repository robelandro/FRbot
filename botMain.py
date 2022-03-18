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

with client as n:
    n.add_event_handler(tg_helper.uptodate)

# with client as jl:
#     jl.add_event_handler(tg_helper.joined_leave)


def main():
    loop = asyncio.get_event_loop()

    botClint.start()
    client.start()

    loop.run_forever()


if __name__ == '__main__':
    main()
