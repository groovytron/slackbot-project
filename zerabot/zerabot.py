import asyncio
import json
import sys
from aiohttp import ClientSession, errors
import aiohttp

from api import api_call

from bot_token import TOKEN

from twitch import check_user

bot_infos = dict()

async def answer(user_token, message):
    data = {"token": TOKEN, "channel": user_token,"text": message}
    await api_call("chat.postMessage", data, TOKEN)


async def consumer(message):
    """Display the message."""
    global bot_infos
    #print("message user:", message.get('user'))
    message_user = message.get('user')
    print("received message:", message)
    print(message_user, " != ", bot_infos['id'], message_user != bot_infos['id'])
    if message.get('type') == 'message' and message_user not in (bot_infos['id'], None):
        #user = await api_call('users.info',{'user': message.get('user')})
        # asked_user = re.search(r'(\S+)', message["text"].strip())
        text = message["text"].split(' ')
        if text[0] != ("<@" + str(bot_infos['id']) + ">:"):
            await answer(message['channel'], "Please call me")

        else:
            asked_user = text[1]
            user_status = await check_user(asked_user)
        #print("{0}: {1}".format(user["user"]["name"],user_status))
        #bot_answer = "{0}: {1}".format(user["user"]["name"],user_status)
            bot_answer = "{0}".format(user_status)
        #print(bot_answer)
        #print(message)
            await answer(message['channel'], bot_answer)
    #else:
    #    print(message, file=sys.stderr)


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
                # infos = {'id': rtm['self']['id']}
                global bot_infos
                bot_infos.update({'id': rtm['self']['id'], 'name': rtm['self']['name']})
                print(bot_infos)
                #print(my_self)
                #print(rtm['self']['name'])
                asyncio.ensure_future(consumer(message))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot())
    loop.close()
