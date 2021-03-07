from logging import error
import discord

from bs4 import BeautifulSoup
import requests

import os
from dotenv import load_dotenv
load_dotenv()

client = discord.Client()
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

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    
    if msg.startswith("-search "):
        searchQuery = "/search?q=" + msg[8:]
        if "bot" not in searchQuery:
            searchQuery = searchQuery + " bots"
        embeds = getEmbed(searchQuery)
        
        for embed in embeds:
            await message.channel.send(embed=embed)
        await message.channel.send("**End of Results**")

    elif msg == "-top":
        searchQuery = "/list/top"
        embeds = getEmbed(searchQuery)
        for embed in embeds:
            await message.channel.send(embed = embed)
        await message.channel.send("**End of Results**")
        

client.run(os.getenv('TOKEN'))