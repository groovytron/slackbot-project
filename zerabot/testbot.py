import asyncio
import json
import sys
import argparse
from urllib.request import urlopen
from urllib.error import URLError
from aiohttp import ClientSession, errors
import aiohttp

from api import api_call

from bot_token import TOKEN


async def consumer(message):
    """Display the message."""
    if message.get('type') == 'message':
        user = await api_call('users.info',{'user': message.get('user')})
        user_status = await check_user(message["text"])
        print("{0}: {1}".format(user["user"]["name"],user_status))
    else:
        print(message, file=sys.stderr)


async def bot(token=TOKEN):
    """Create a bot that joins Slack."""
    rtm = await api_call("rtm.start")
    assert rtm['ok'], "Error connecting to RTM."

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(rtm["url"]) as ws:
            async for msg in ws:
                assert msg.tp == aiohttp.MsgType.text
                message = json.loads(msg.data)
                asyncio.ensure_future(consumer(message))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot())
    loop.close()


async def check_user(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    async with ClientSession() as session:
        url = 'https://api.twitch.tv/kraken/streams/{}'.format(user)
        async with session.get(url) as response:
            try:
                info = await response.read()
                info = json.loads(info.decode('utf-8'))
                # print(info)
                if info['stream'] == None:
                    status = 1
                    return "{0}, is offline".format(user)
                else:
                    status = 0
                    print(info['stream']['channel']['display_name'], "is playing", info['stream']['game'], "in front of", info['stream']['viewers'], "viewers")
                    return "Watch here {0}".format(info['stream']['channel']['url'])
            except URLError as e:
                    pass
                    if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
                        status = 2
                        return "{0} does not exist".format(user)
                    else:
                        status = 3
                        return "an error occured"
