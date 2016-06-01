import asyncio
import json
import sys
from urllib.request import urlopen
from urllib.error import URLError
from aiohttp import ClientSession, errors
import aiohttp

from api import api_call

from bot_token import TOKEN

from twitch import check_user

import re

async def answer(user_token, message):
    data = {"token": TOKEN, "channel": user_token,"text": message}
    await api_call("chat.postMessage", data, TOKEN)


async def consumer(message):
    """Display the message."""
    #print("message user:", message.get('user'))
    message_user = message.get('user')
    if message.get('type') == 'message' and message_user != None:
        #user = await api_call('users.info',{'user': message.get('user')})
        # asked_user = re.search(r'(\S+)', message["text"].strip())
        asked_user = message["text"].split(' ', 1)[0]
        user_status = await check_user(asked_user)
        #print("{0}: {1}".format(user["user"]["name"],user_status))
        #bot_answer = "{0}: {1}".format(user["user"]["name"],user_status)
        bot_answer = "{0}".format(user_status)
        #print(bot_answer)
        #print(message)
        await answer(message['channel'], bot_answer)
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
                #print(message)
                #my_self = rtm['self']['id']
                #print(my_self)
                #print(rtm['self']['name'])
                asyncio.ensure_future(consumer(message))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot())
    loop.close()
