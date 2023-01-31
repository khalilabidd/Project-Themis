import discord
import responses
from settings import *
from teams import *

# Send messages
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
async def devide_teams(client,user,message_channel):
    try:
        channel1 = client.get_channel(TEAM1_VC_ID)
        channel2 = client.get_channel(TEAM2_VC_ID)
        members = get_players(user)
        memids = [member.id for member in members]
        if len(memids)==8:
            team1,team2 = devideTeam(memids)
            for member in members:
                if member.id in team1:
                    await member.move_to(channel1)
                elif member.id in team2:
                    await member.move_to(channel2)
        else:
            await message_channel.send(f'Not enough players for deviding teams. Current players:{len(memids)}, Required players 8')
    except Exception as e:
        print(e)

def get_players(user):
    # currently retrieve members of in the user's current channel
    # TODO: retrieve list of players in user's lobby once the API is ready
    channel = user.voice.channel
    members = channel.members
    return members

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        # If the user message contains a '?' in front of the text, it becomes a private message
        if user_message[0] == '?':
            user_message = user_message[1:]  # [1:] Removes the '?'
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
        if user_message.lower() == '!teams':
            await devide_teams(client,message.author,message.channel)


    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)