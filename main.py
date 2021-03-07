from logging import error
import discord
from discord.ext import commands
import random
from bs4 import BeautifulSoup
import requests
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

client = commands.Bot(command_prefix="-", help_command=None)

url = "https://top.gg"

def getEmbed(searchQuery):
    resultsPage = BeautifulSoup(requests.get(url + searchQuery).text, 'html.parser')
    results = resultsPage.find("div",{"id":"bot-list"}).find_all("li",{"class": "column bot-card is-3"})
    embeds = []
    for result in results:
        embed = discord.Embed()
        try:
            tags = result.find("p",{"class":"card-tags"}).text
        except:
            tags = result.find("span",{"class":"card-tags"}).text
        resultUrl = ""
        try:
            embed.title = result.find("div",{"class":"bot-name"}).text.strip()
            resultUrl = resultUrl + url + result.find("a", {"class":"info"}).get("href")
        except AttributeError:
            embed.title = result.find("a",{"class":"bot-name"}).text.strip()
            resultUrl = resultUrl + url + result.find("a", {"class":"bot-name"}).get("href")
        except:
            continue

        embed.description = result.find("p", {"class": "bot-description"}).text
        embed.set_image(url= result.find("img").get("src"))

            
        embed.url = resultUrl
        embed.add_field(name="More Info", value=resultUrl, inline=False)
        embed.add_field(name="Invite", value=resultUrl + "/invite/", inline=False)
        embed.add_field(name="Tags", value=tags, inline=False)
        if("Promoted" in tags):
            embed.colour = 0xa39324
        embeds.append(embed)
    return embeds


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def hello(ctx):
    await ctx.send("Hi")

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

    
@client.command()
async def search(ctx, *, msg):
    if ctx.author == client.user:
        return
    searchQuery = "/search?q=" + msg
    if "bot" not in searchQuery:
        searchQuery = searchQuery + " bots"
    embeds = getEmbed(searchQuery)
        
    for embed in embeds:
        await ctx.channel.send(embed=embed)
    embed2 = discord.Embed()
    embed2.title = "**End of Results**"
    embed2.add_field(name="More Results: ", value=url + searchQuery)
    await ctx.channel.send(embed=embed2)

@client.command()
async def top(ctx):
    if ctx.author == client.user:
        return
    searchQuery = "/list/top"
    embeds = getEmbed(searchQuery)
    for embed in embeds:
        await ctx.channel.send(embed = embed)
    embed2 = discord.Embed()
    embed2.title = "**End of Results**"
    embed2.add_field(name="More Results: ", value=url + searchQuery)
    await ctx.channel.send(embed=embed2)

@client.command()
async def help(ctx):
    if ctx.author == client.user:
        return
    helps = [
        {
            "command": "-help",
            "description": "Shows help on how to use the bot."
        },
        {
            "command": "-search [Search Query (Mandatory)]",
            "description": "Searches [Search Query] for matching bots on https://top.gg/"
        },
        {
            "command": "-top",
            "description": "Shows top trending bots on https://top.gg/"
        },
        {
            "command": "-meme",
            "description": "Shows a random meme."
        }
    ]

    embed = discord.Embed()
    embed.title = "Bot Commands Help"
    for help in helps:
        embed.add_field(name="Command", value=help["command"], inline=True)
        embed.add_field(name="Description", value=help["description"], inline=True)
        embed.add_field(name="-----------------------------------------", value="----------------------------------------\n", inline=False)
    await ctx.send(embed=embed)
        


client.run(os.getenv('TOKEN'))