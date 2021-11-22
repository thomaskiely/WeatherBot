import discord
from discord import message
from discord.ext import commands
from discord.message import Message
import requests, json


client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('ready')


#command to get the weather
@client.command()
async def weather(ctx, *, content:str):

    location = content
    print(location)

    
    
    weath = getWeather(location)

    farWeath = kelvinToFarenHeit(weath)

    weathString = str(farWeath)

    await ctx.send("Weather in "+location+ " is "+weathString+"°F")



@client.command()
async def echo(ctx, *,content:str):
    await ctx.send(content)


#function to convert kelvin to farenheit

def kelvinToFarenHeit(kelvinTemp):
    conversion = (9/5)*(kelvinTemp-273)+32

    farenheitTemp = round(conversion)
    return farenheitTemp


    
    






def getWeather(locationString):
    myKey = "37b834df06bbdc5c9c6e4c8449a3e0af"

    baseWeather = "https://api.openweathermap.org/data/2.5/weather?"

    city = locationString

    weatherCall = baseWeather + "q=" + city + "&appid=" + myKey

    #http request
    response = requests.get(weatherCall)

    if response.status_code == 200:
        data = response.json()

        main = data['main']

        temperature = main['temp']

        wind = data['wind']

        windSpeed = wind['speed']

        print(f"Temperature: {temperature}")
       
        print(f"Wind Speed: {windSpeed}")

    else:
        print("error in http request")
        print(response.status_code)
        print(weatherCall)

    return temperature



    


client.run('OTA1MTM4MzQ4MDA2NDQ1MTE3.YYFtxg.y3oqsj6d94ZJ24OcQzn8-9oGSwg')



