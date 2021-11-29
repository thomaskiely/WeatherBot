import discord
from discord import message
from discord.ext import commands
from discord.message import Message
import requests, json
import time


client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('ready')


#command to get the weather
@client.command()
async def weather(ctx, *, content:str):

    #read the location from the user
    location = content
    print(location)

    
    #get weather data from getWeather function
    weatherList = getWeather(location)

    #assign elements of weatherList to new variables
    #(description,temperature,feels like temp, humidity, wind speed, cloud percentage,sunset time)

    description = weatherList[0]
    temperature = kelvinToFarenHeit(weatherList[1])
    feelsLike = kelvinToFarenHeit(weatherList[2])
    humidity = weatherList[3]
    #convert m/s to mph
    windSpeed = round(weatherList[4]*2.237)
    cloudPercentage = weatherList[5]
    sunsetTime = weatherList[6]
    sunsetTimeFormatted = epochToNormalTime(sunsetTime)



    await ctx.send("Weather in "+location+ " is "+description + ". Temperature is "+str(temperature)+"°F, "+ " feels like "+str(feelsLike)+"°F. Wind speed is "+str(windSpeed)+"mph. Humidity is "+ str(humidity)+"%. Cloudiness is "+ str(cloudPercentage)+"%. Sunset at "+ str(sunsetTimeFormatted)+" PM EST.")


    



@client.command()
async def echo(ctx, *,content:str):
    await ctx.send(content)


#function to convert kelvin to farenheit

def kelvinToFarenHeit(kelvinTemp):
    conversion = (9/5)*(kelvinTemp-273)+32

    farenheitTemp = round(conversion)
    return farenheitTemp



#convert epoch time to 24 hour
def epochToNormalTime(epochTime):
    
    formattedTime = time.strftime('%H:%M',time.localtime(epochTime))
    return formattedTime
    






def getWeather(locationString):
    #API KEY for weather
    myKey = "KEY"

    #base API call that we will fill in with criteria
    baseWeather = "https://api.openweathermap.org/data/2.5/weather?"

    #assign the user input to city variable to use in the API call
    city = locationString

    #create link for API call
    weatherCall = baseWeather + "q=" + city + "&appid=" + myKey

    #http request
    response = requests.get(weatherCall)

    if response.status_code == 200:
        data = response.json()

        #get main weather data
        main = data['main']

        #get temperature data
        temperature = main['temp']

        #get feels like temp
        feelsLike = main['feels_like']

        #get humidity
        humidity = main['humidity']

        #get wind data
        wind = data['wind']

        #get wind speed
        windSpeed = wind['speed']

        #get clouds data
        cloudData = data['clouds']

        #get cloudiness percentage
        cloudPercentage = cloudData['all']


        #get description
        getDescription = data['weather']
        description = getDescription[0]['description']
        description2 = getDescription[0]['main']


        #get sunset time
        getTimes = data['sys']
        sunset = getTimes['sunset']


    else:
        print("error in http request")
        print(response.status_code)
        print(weatherCall)


    #return a list of the following
    #(description,temperature,feels like temp, humidity, wind speed, cloud percentage,sunset time)
    weatherItems = [description2,temperature,feelsLike,humidity,windSpeed,cloudPercentage,sunset]

    print(weatherItems)
    return weatherItems



    


client.run('KEY')



