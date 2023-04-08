import discord
import time
from responses import handle_response 
from settings import *
from teams import *

class Counter:
    def __init__(self):
        self.count = 0
        self.timer = time.time()

    def increment(self):
        if time.time()-self.timer>300:
            self.count = 1
        else:
            self.count += 1
        self.timer = time.time()


async def divide_teams(client,user,message_channel):
    default_response = ref = ''
    try:
        channel1 = client.get_channel(TEAM1_VC_ID)
        channel2 = client.get_channel(TEAM2_VC_ID)
        members = get_players(user)
        memids = [member.id for member in members]
        if len(memids) in [4,6,8]:
            team1,team2 = divideTeam(memids)
            for member in members:
                if member.id in team1:
                    await member.move_to(channel1)
                elif member.id in team2:
                    await member.move_to(channel2)
        else:
            if (len(memids)<4):
                default_response = f'You need to have more players to divide teams. Current players: {len(memids)}'
                ref = 'minplayers'
            elif (len(memids)>8):
                default_response = f'You cannot have more than 8 players to divide teams. Current players: {len(memids)}'
                ref = 'maxplayers'
            else:
                default_response = f'You need to have even number of players to divide teams. Current players: {len(memids)}'
                ref = 'evenplayers'
    except Exception as e:
        ref = 'error'
        print(e)
    message = handle_response(ref,default_response)
    if message:
        await message_channel.send(message)

def get_players(user):
    channel = user.voice.channel
    members = channel.members
    return members

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True
    client = discord.Client(intents=intents)

    counter = Counter()

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if (message.author == client.user) or (message.channel.id not in CHANNELS_ID):
            return
        if message.content == 'Hey Themis!':
            default_response = "Hey there everyone, I'm Themis and my mission is to ensure justice, divine order, fairness and law."
            response = handle_response(message.content,default_response)
            await message.channel.send(response)
        elif message.content == '!help':
            await message.channel.send("Commands: \n !teams - divide teams to seperate channels")
        elif message.content.lower() == '!teams':
            await divide_teams(client,message.author,message.channel)
            counter.increment()
            if counter.count>2:
                ref = 'try:'+str(counter.count)
                response = handle_response(ref)
                if response:
                    await message.channel.send(response)
        else:
            response = handle_response(message.content)
            if response:
                await message.channel.send(response)
    client.run(TOKEN)