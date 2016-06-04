""" Functions allowing to interct with Twitch API. """

import asyncio
import json
import sys
from urllib.request import urlopen
from urllib.error import URLError
from aiohttp import ClientSession, errors
import aiohttp

async def check_user(user):
    """ returns the current player status """
    async with ClientSession() as session:
        url = 'https://api.twitch.tv/kraken/streams/{}'.format(user)
        async with session.get(url) as response:
            try:
                info = await response.read()
                info = json.loads(info.decode('utf-8'))
                # print(info)
                try:
                    if info['stream'] == None:
                        return "{0} is offline".format(user)
                    else:
                        return "{0} is playing {1} in front of {2} viewers, watch here {3}".format(info['stream']['channel']['display_name'], info['stream']['game'], info['stream']['viewers'], info['stream']['channel']['url'])
                except KeyError as e:
                    return "{0} doesn't exist.".format(user)
            except URLError as e:
                    pass
                    if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
                        return "{0} does not exist".format(user)
                    else:
                        return "an error occured"
