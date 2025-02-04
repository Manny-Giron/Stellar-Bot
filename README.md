# How to get started:

import discord
from discord.ext import commands
from bs4 import BeautifulSoup

import json
import datetime
import requests
import pytz 
import timezone





intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="-stellar", intents=intents)
# Create a new Discord client
client = discord.Client(intents=intents)


# Event listener for when a message is sent
@client.event
async def on_message(message):
  #Gets NASAs unique photo of the day using BS4
  async def getUniquePOTD():
    site = "https://apod.nasa.gov/apod/astropix.html"
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    image = soup.find_all('img')
    url = image[0]['src']
    url = "https://apod.nasa.gov/apod/" + url
    await message.channel.send(url)

  #checks for prefix to call bot's command
  if message.content.startswith('-stellar'):
    text = message.content[9:]
    #return error to client, if no text is given
    if text.lower() == '':
      await message.channel.send('Input error, try again or type "-stellar help" for commands.')
      
    if text.lower() == "help":
      #return message to client, with list of commands
      await message.channel.send("'POTD' - Picture of the Day \n'NPS' - Number of People in Space\n")

    if text.lower() == "potd":
        await getUniquePOTD()
    if text.lower() == "nps":
      NPSURL = 'http://api.open-notify.org/astros.json'
      response = requests.get(NPSURL)

      #ensure response was valid, get current date, get num people and people in space + craft
      if response.status_code == 200:
        currentDate = datetime.date.today()
        currenatDate = str(currentDate)
        data = response.json()
        nps = data['number']
        
        people = data['people']
        namesAndCraft = ""
        #formatting for display
        for person in people:
          personData = person['name'] + ' - ' + person['craft']
          namesAndCraft += personData + '\n'
          
                        
          
        #return message to client
        await message.channel.send("There are currently " + str(nps) + " people in space.  " + currenatDate + "\n" + namesAndCraft)

    

      

# Turns on bot
client.run('MTIwMzU1NDIyOTQ0OTY1ODQzMA.GmL-RK.hn4bmf5AT3m6fFK4U7K65LAB46PEP0z0j4IPYU')


