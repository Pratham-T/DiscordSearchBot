import discord
import os
from dotenv import load_dotenv
load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.split()
    searchQuery = ""
    #edit this to fetch and display search results
    if msg[0] == "-search":
        for i in range(1, len(msg)):
            searchQuery = searchQuery + (msg[i] + " ")
        await message.channel.send("You want to search: " + searchQuery)

client.run(os.getenv('TOKEN'))