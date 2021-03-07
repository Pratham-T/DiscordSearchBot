import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv
load_dotenv()

images = [
'https://i.imgur.com/JQGhevZ.jpg',
'https://i.imgur.com/yl4U0ZY.jpg',
'https://i.imgur.com/NuDbYN6.jpg',
'https://i.imgur.com/OGwJeAX.jpg',
'https://i.imgur.com/IFcT93v.jpg',
'https://i.imgur.com/WAjMADM.jpg',
'https://i.imgur.com/6AiIwzp.jpg',
'https://i.imgur.com/SZWbVzh.jpg',
'https://i.imgur.com/LWMk1N3.jpg',
'https://i.imgur.com/VCmy1lp.jpg',
'https://i.imgur.com/UIHtWjS.jpg',
'https://i.imgur.com/9iUeAKt.jpg',
'https://i.imgur.com/42IdSrp.jpg',
'https://i.imgur.com/YYHB9Vm.jpg']

client = commands.Bot(command_prefix="-")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def hello(ctx):
    await ctx.send("hi")

@client.command(aliases=['user','info'])
@commands.has_permissions(kick_members=True)
async def whois(ctx,member:discord.Member):
    embed = discord.Embed(title = member.name, description = member.mention, color = discord.Colour.red())
    embed.add_field(name = "ID",value = member.id,inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    await ctx.send(embed=embed)

@client.command()
async def meme(ctx):
    embed = discord.Embed(color = discord.Colour.green())
    random_link = random.choice(images)
    embed.set_image(url = random_link)
    await ctx.send(embed=embed)

client.run(os.getenv('TOKEN'))