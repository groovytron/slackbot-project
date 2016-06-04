"""
	Module allowing to start a bot connecting to Slack through Slakp API.
	User can then ask the bot if a Twitch streamer is streaming.
"""
import os
import asyncio

from .zerabot import bot, consumer, answer
from .twitch import check_user
from .api import api_call

def main():
    print("Bot is starting...")
    # print(os.environ.get('SLACK_TOKEN'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot())
    loop.close()
