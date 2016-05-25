""""""
import argparse
from urllib.request import urlopen
from urllib.error import URLError
import json
import asyncio
from aiohttp import ClientSession, errors

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
                    return "Watch here {0}"format(info['stream']['channel']['url'])
            except URLError as e:
                    pass
                    if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
                        status = 2
                        return "{0} does not exist".format(user)
                    else:
                        status = 3
                        return "an error occured"

async def fetch(user):
    async with ClientSession() as session:
        url = 'https://api.twitch.tv/kraken/streams/' + user
        try:
            async with session.get(url) as response:
                return await response.read()
        except errors.ClientOSError as e:
            return e

async def run(users):
    tasks = []
    for user in users:
        task = asyncio.ensure_future(fetch(user))
        tasks.append(task)
    responses = await asyncio.gather(*tasks)
    print(responses)

# main
try:
    # user = parse_args().USER[0]
    users = ['Zerator', 'Fukano', 'Domingo', '-1']
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(users))
    loop.run_until_complete(future)
except KeyboardInterrupt:
    pass
