from asyncio import events
from lib2to3.pgen2 import token
from typing import AsyncContextManager
import discord, sys, os, pymongo, asyncio, json, random
from pymongo import database
import matplotlib.pyplot as plt
from datetime import datetime

TOKEN = None
dbTOKEN = None
with open("TOKEN.json", 'r') as tokenfile:
    TOKEN = json.load(tokenfile)['TOKEN']
    dbTOKEN = json.load(tokenfile)['dbTOKEN']

#Database
client = discord.Client(dbTOKEN)
dbClient = pymongo.MongoClient()
Database = dbClient['Investment-Bot']
dbEvents = Database['events']
dbAccounts = Database['accounts']
dbStocks = Database['stocks']
dbTransactions = Database['transactions']

#price and event updater
async def price_updater():
    eventCoolDown = 0
    while True:
        eventCoolDown += 1
        stock_read = list(dbStocks.find({}))
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        for stock in stock_read:
            newPrice = int(stock['corporationPrice']) / int(stock['stockCount'])
            stockHistory = stock['priceHistory']
            stockHistory[dt_string] = newPrice
            dbStocks.update_one({'name': stock['name']}, {'$set': {'currentPrice': newPrice, 'priceHistory': stockHistory}})
        await asyncio.sleep(60)
        if eventCoolDown == 120:
            pass
        
        

#client initialization
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord')
    await price_updater()

#commands
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    account_read = list(dbAccounts.find({}))
    stock_read = list(dbStocks.find({}))
    owner_found = False
    for account in account_read:
        if account['userID'] == message.author.id and account['permissions'] == 'Owner':
            owner_found = True
    
    if message.content == '*create account':
        for account in account_read:
            if account['userID'] == message.author.id:
                await message.channel.send("You already have an account, you can't make a second one")
                return
        accountData = {'userID': message.author.id, 
                       'permissions': 'User', 
                       'balance': 5000, 
                       'stocks': {}}
        dbAccounts.insert_one(accountData)
        await message.channel.send("Account Created! Thank you for using our bot!")
    
    if "*view price" in message.content:
        commandInfo = message.content.split(' ')
        commandInfo.remove('*view')
        commandInfo.remove("price")
        noStock = True
        price = 0
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        for stock in stock_read:
            if stock['name'] == commandInfo[0]:
                noStock = False
                price = stock['currentPrice']
        if noStock:
            await message.channel.send("No stock found.... Check your command, the command should be [*view price <stock name>]")
            await message.channel.send("You can also get list of available stocks with: [*list stocks]")
            return
        await message.channel.send(f"{commandInfo[0]} at {dt_string} is ${price}")

    if message.content == "*list stocks":
        stockCount = 1
        for stock in stock_read:
            await message.channel.send(f"{stockCount}) {stock['name']}")
            stockCount += 1
    
    if "*buy" in message.content
    
    if owner_found:
        if '*create stock' in message.content:
            commandInfo = message.content.split(' ')
            commandInfo.remove('*create')
            commandInfo.remove("stock")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            eventID = random.randint(1, 10000000000000000)
            

            stockData = {'name': commandInfo[0], 
                         'currentPrice': 0, 
                         'priceHistory': {dt_string: 0}, 
                         'stockCount': commandInfo[1], 
                         'corporationPrice': commandInfo[2], 
                         'eventIDs': [eventID]}
            eventData = {'stockName': commandInfo[0], 
                         'eventID': eventID, 
                         'content': f"{commandInfo[0]} stock got created! Happy investing!", 
                         'priceChange': "None"}
            dbStocks.insert_one(stockData)
            dbEvents.insert_one(eventData)
            await message.channel.send(f"Stock Created, stock name = {commandInfo[0]}, stock count = {commandInfo[1]}, corporation price = {commandInfo[2]}")

client.run(TOKEN)