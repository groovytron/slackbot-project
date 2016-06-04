import asyncio
import json
import sys
from aiohttp import ClientSession, errors
import aiohttp

from .api import api_call

from .config import TOKEN

from .twitch import check_user

bot_infos = dict()
handled_commands = ("streams","help")
bot_help = """
Hmm... You seem to have asked for help or tried to do something wrong with me. Call me with `@{name}: command`
*Avalaible commands*:
    •`@{name}: streams toto` checks if toto is streaming.
            """
async def send_help(user):
    """ Makes the bot send help text to the specified user. """
    global bot_help
    bot_answer = bot_help.format(name=bot_infos['name'])
    await answer(user, bot_answer)


async def answer(user, message):
    """ Sends a message to the user. """
    data = {"token": TOKEN, "channel": user,"text": message}
    await api_call("chat.postMessage", data, TOKEN)


async def consumer(message):
    """
    Consumes the given message, parse it and makes the bot react
    depending on the message.
    """
    global bot_infos, bot_help, handled_commands
    message_user = message.get('user')
    if message.get('type') == 'message' and message_user not in (bot_infos['id'], None):
        text = message["text"].split(' ')
        if text[0] == ("<@" + str(bot_infos['id']) + ">:"):
            if  len(text) < 3:
                await send_help(message['channel'])

            else:
                if text[1] in handled_commands:
                    if text[1] == handled_commands[0]:
                        asked_user = text[2]
                        user_status = await check_user(asked_user)
                        bot_answer = "{0}".format(user_status)
                        await answer(message['channel'], bot_answer)
                else:
                    await send_help(message['channel'])
    else:
       print(message, file=sys.stderr)


async def bot(token=TOKEN):
    """Creates a Slack bot with whitch to communicate."""
    rtm = await api_call("rtm.start")
    assert rtm['ok'], "Error connecting to RTM."

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(rtm["url"]) as ws:
            async for msg in ws:
                assert msg.tp == aiohttp.MsgType.text
                message = json.loads(msg.data)
                global bot_infos
                bot_infos.update({'id': rtm['self']['id'], 'name': rtm['self']['name']})
                print(bot_infos)
                asyncio.ensure_future(consumer(message))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot())
    loop.close()
