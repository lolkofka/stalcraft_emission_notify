import asyncio
import logging

import bot
from bot import main_bot
import loader
from db.database import connect

from emission_loop import start_loop


async def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('pymorphy3').setLevel(logging.WARNING)

    loader.load_dynamics('dynamic')
    
    await connect()

    await asyncio.gather(bot.start(), start_loop(main_bot))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
