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

# Prefix for commands
client = commands.Bot(command_prefix="-stellar", intents=intents)
# Create a new Discord client
client = discord.Client(intents=intents)

# Event listener for when a message is sent
@client.event
async def on_message(message):
  #gets 
  async def getUniquePOTD():
    site = "https://apod.nasa.gov/apod/astropix.html"
    response = requests.get(site)
    soup = BeautifulSoup(response.text, 'html.parser')
    image = soup.find_all('img')
    url = image[0]['src']
    url = "https://apod.nasa.gov/apod/" + url
    await message.channel.send(url)
    
  if message.content.startswith('-stellar'):
    text = message.content[9:]
    
    if text.lower() == '':
      await message.channel.send('Input error, try again or type "-stellar help" for commands.')
      
    if text.lower() == "help":
      await message.channel.send("'POTD' - Picture of the Day \n'NPS' - Number of People in Space\n")

    if text.lower() == "potd":
        await getUniquePOTD()
    if text.lower() == "nps":
      NPSURL = 'http://api.open-notify.org/astros.json'
      response = requests.get(NPSURL)
      
      if response.status_code == 200:
        currentDate = datetime.date.today()
        currenatDate = str(currentDate)
        data = response.json()
        nps = data['number']
        
        people = data['people']
        namesAndCraft = ""
        
        for person in people:
          personData = person['name'] + ' - ' + person['craft']
          namesAndCraft += personData + '\n'

        await message.channel.send("There are currently " + str(nps) + " people in space.  " + currenatDate + "\n" + namesAndCraft)

    

      

# Turns on bot 
client.run('MTA2OTA0Mjg1NDk3NjAzNjg5NA.GTHPzt.Fd-kdvX6IqYN9XyLySqw41cg50xs3jEpdsRu0U')
