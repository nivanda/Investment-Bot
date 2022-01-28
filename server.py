from asyncio import events
from typing import AsyncContextManager
import discord, sys, os, pymongo, asyncio, json, random
from pymongo import database
import matplotlib.pyplot as plt
from datetime import datetime

from scipy import rand

TOKEN = ""
dbTOKEN = ""
CommandHelp = """To create investing account - [$create account], 
To list all stocks by name - [$list stocks], 
To view price of a stock - [$view price <stock name>], 
To buy certain ammount of stock - [$buy <stock name> <ammount>], 
To sell certain ammount of stock - [$sell <stock name> <ammount>], 
To list your stocks - [$list my stocks], 
To view your balance - [$balance]"""

with open("TOKEN.json", 'r') as tokenfile:
    DecodedFile = json.load(tokenfile)
    TOKEN = DecodedFile['TOKEN']
    dbTOKEN = DecodedFile['dbTOKEN']

#Database
client = discord.Client()
dbClient = pymongo.MongoClient(dbTOKEN)
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
            newPrice = stock['corporationPrice'] / stock['stockCount']
            stockHistory = stock['priceHistory']
            stockHistory[dt_string] = newPrice
            dbStocks.update_one({'name': stock['name']}, {'$set': {'currentPrice': newPrice, 'priceHistory': stockHistory}})
        await asyncio.sleep(60)
        if eventCoolDown == 120:
            eventCoolDown = 0
            for stock in stock_read:
                chance = random.randint(1, 100)
                if chance >= 1 and chance < 35:
                    chance = random.randint(1, 100)
                    if chance >= 1 and chance < 50:
                        corpPrice = stock['corporationPrice']
                        corpPrice = (corpPrice / 100) * 2 + corpPrice
                        eventHistory = stock['eventIDs']
                        eventID = random.randint(1, 10000000000000000)
                        eventData = {'stockName': stock['name'], 
                            'eventID': eventID, 
                            'content': f"{stock['name']}'s corporation price has risen by 2%", 
                            'priceChange': "+ 2%"}
                        eventHistory.append(eventID)
                        dbStocks.update_one({'name': stock['name']}, {'$set': {'corporationPrice': corpPrice, 'eventIDs': eventHistory}})
                        dbEvents.insert_one(eventData)
                    if chance >= 50 and chance < 100:
                        corpPrice = stock['corporationPrice']
                        corpPrice = corpPrice - (corpPrice / 100) * 2
                        eventHistory = stock['eventIDs']
                        eventID = random.randint(1, 10000000000000000)
                        eventData = {'stockName': stock['name'], 
                            'eventID': eventID, 
                            'content': f"{stock['name']}'s corporation price has dropped by 2%", 
                            'priceChange': "- 2%"}
                        eventHistory.append(eventID)
                        dbStocks.update_one({'name': stock['name']}, {'$set': {'corporationPrice': corpPrice, 'eventIDs': eventHistory}})
                        dbEvents.insert_one(eventData)
                if chance >= 35 and chance < 70:
                    chance = random.randint(1, 100)
                    if chance >= 1 and chance < 50:
                        corpPrice = stock['corporationPrice']
                        corpPrice = (corpPrice / 100) * 5 + corpPrice
                        eventHistory = stock['eventIDs']
                        eventID = random.randint(1, 10000000000000000)
                        eventData = {'stockName': stock['name'], 
                            'eventID': eventID, 
                            'content': f"{stock['name']}'s corporation price has risen by 5%", 
                            'priceChange': "+ 5%"}
                        eventHistory.append(eventID)
                        dbStocks.update_one({'name': stock['name']}, {'$set': {'corporationPrice': corpPrice, 'eventIDs': eventHistory}})
                        dbEvents.insert_one(eventData)
                    if chance >= 50 and chance < 100:
                        corpPrice = stock['corporationPrice']
                        corpPrice = corpPrice - (corpPrice / 100) * 5
                        eventHistory = stock['eventIDs']
                        eventID = random.randint(1, 10000000000000000)
                        eventData = {'stockName': stock['name'], 
                            'eventID': eventID, 
                            'content': f"{stock['name']}'s corporation price has dropped by 5%", 
                            'priceChange': "- 5%"}
                        eventHistory.append(eventID)
                        dbStocks.update_one({'name': stock['name']}, {'$set': {'corporationPrice': corpPrice, 'eventIDs': eventHistory}})
                        dbEvents.insert_one(eventData)
                if chance >= 70 and chance < 90:
                    chance = random.randint(1, 100)
                    if chance >= 1 and chance < 50:
                        corpPrice = stock['corporationPrice']
                        corpPrice = (corpPrice / 100) * 10 + corpPrice
                        eventHistory = stock['eventIDs']
                        eventID = random.randint(1, 10000000000000000)
                        eventData = {'stockName': stock['name'], 
                            'eventID': eventID, 
                            'content': f"{stock['name']}'s corporation price has risen by 10%", 
                            'priceChange': "+ 10%"}
                        eventHistory.append(eventID)
                        dbStocks.update_one({'name': stock['name']}, {'$set': {'corporationPrice': corpPrice, 'eventIDs': eventHistory}})
                        dbEvents.insert_one(eventData)
                    if chance >= 50 and chance < 100:
                        corpPrice = stock['corporationPrice']
                        corpPrice = corpPrice - (corpPrice / 100) * 10
                        eventHistory = stock['eventIDs']
                        eventID = random.randint(1, 10000000000000000)
                        eventData = {'stockName': stock['name'], 
                            'eventID': eventID, 
                            'content': f"{stock['name']}'s corporation price has dropped by 10%", 
                            'priceChange': "- 10%"}
                        eventHistory.append(eventID)
                        dbStocks.update_one({'name': stock['name']}, {'$set': {'corporationPrice': corpPrice, 'eventIDs': eventHistory}})
                        dbEvents.insert_one(eventData)
                if chance >= 90 and chance < 100:
                    chance = random.randint(1, 100)
                    if chance >= 1 and chance < 50:
                        corpPrice = stock['corporationPrice']
                        corpPrice = (corpPrice / 100) * 15 + corpPrice
                        eventHistory = stock['eventIDs']
                        eventID = random.randint(1, 10000000000000000)
                        eventData = {'stockName': stock['name'], 
                            'eventID': eventID, 
                            'content': f"{stock['name']}'s corporation price has risen by 15%", 
                            'priceChange': "+ 15%"}
                        eventHistory.append(eventID)
                        dbStocks.update_one({'name': stock['name']}, {'$set': {'corporationPrice': corpPrice, 'eventIDs': eventHistory}})
                        dbEvents.insert_one(eventData)
                    if chance >= 50 and chance < 100:
                        corpPrice = stock['corporationPrice']
                        corpPrice = corpPrice - (corpPrice / 100) * 15
                        eventHistory = stock['eventIDs']
                        eventID = random.randint(1, 10000000000000000)
                        eventData = {'stockName': stock['name'], 
                            'eventID': eventID, 
                            'content': f"{stock['name']}'s corporation price has dropped by 15%", 
                            'priceChange': "- 15%"}
                        eventHistory.append(eventID)
                        dbStocks.update_one({'name': stock['name']}, {'$set': {'corporationPrice': corpPrice, 'eventIDs': eventHistory}})
                        dbEvents.insert_one(eventData)
        
        

#client initialization
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord')
    await price_updater()

#commands
@client.event
async def on_message(message):
    global CommandHelp
    if message.author == client.user:
        return
    
    account_read = list(dbAccounts.find({}))
    stock_read = list(dbStocks.find({}))
    owner_found = False
    for account in account_read:
        if account['userID'] == message.author.id and account['permissions'] == 'Owner':
            owner_found = True
    
    if message.content == '$create account':
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
    
    if "$view price" in message.content:
        commandInfo = message.content.split(' ')
        commandInfo.remove('$view')
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

    if message.content == "$list stocks":
        stockCount = 1
        for stock in stock_read:
            await message.channel.send(f"{stockCount}) {stock['name']}")
            stockCount += 1
    
    if "$buy" in message.content:
        commandInfo = message.content.split(' ')
        commandInfo.remove('$buy')
        buyAmmount = 0
        try:
            buyAmmount = int(commandInfo[1])
        except:
            await message.channel.send("The buy ammount is not valid number, use only numbers")
            await message.channel.send("Just to remind, the right way for the command is [*buy <stock name> <ammount>]")
            return
        stockFound = False
        Price = 0
        notEnoughStocks = False
        stocksLeft = 0
        stockCount = 0
        for stock in stock_read:
            if stock['name'] == commandInfo[0]:
                stockFound = True
                Price = stock['currentPrice']
                stocksLeft = stock['stockCount'] - buyAmmount
                stockCount = stock['stockCount']
                if stocksLeft < 0:
                    notEnoughStocks = True
        if not stockFound:
            await message.channel.send("You specified stock was not found, maybe you wrote the command wrong....")
            await message.channel.send("The right way is [*buy <stock name> <ammount>]")
            return
        if notEnoughStocks:
            await message.channel.send(f"There is not enough stocks left, there is only {stockCount} available")
            return
        accountFound = False
        accountStocks = None
        notEnoughMoney = False
        leftOverMoney = 0
        Balance = 0
        for account in account_read:
            if account['userID'] == message.author.id:
                accountFound = True
                accountStocks = account['stocks']
                leftOverMoney = account['balance'] - (buyAmmount * Price)
                Balance = account['balance']
                if leftOverMoney < 0:
                    notEnoughMoney = True
        if not accountFound:
            await message.channel.send("You don't have an investing account, you can make one using [*create account]")
            return
        if notEnoughMoney:
            await message.channel.send("You don't have enough balance to make this purchase...")
            return
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        transactionData = {"userID": message.author.id, 
                           "actionType": "buy", 
                           "stockName": commandInfo[0],
                           "Ammount": buyAmmount,
                           "stockPrice": Price, 
                           'date': dt_string}
        if commandInfo[0] in accountStocks:
            accountStocks[commandInfo[0]] += buyAmmount
        else:
            accountStocks[commandInfo[0]] = buyAmmount
        Balance -= buyAmmount * Price
        stockCount -= buyAmmount
        dbAccounts.update_one({'userID': message.author.id}, {'$set': {'stocks': accountStocks, 'balance': Balance}})
        dbStocks.update_one({'name': commandInfo[0]}, {'$set': {'stockCount': stockCount}})
        dbTransactions.insert_one(transactionData)
        await message.channel.send(f"You successfully bought {buyAmmount} of {commandInfo[0]} at this price: {Price}")
    
    if "$sell" in message.content:
        commandInfo = message.content.split(' ')
        commandInfo.remove('$sell')
        sellAmmount = 0
        try:
            sellAmmount = int(commandInfo[1])
        except:
            await message.channel.send("The sell ammount is not valid number, use only numbers")
            await message.channel.send("Just to remind, the right way for the command is [*sell <stock name> <ammount>]")
            return
        stockFound = False
        Price = 0
        stockCount = 0
        for stock in stock_read:
            if stock['name'] == commandInfo[0]:
                stockFound = True
                Price = stock['currentPrice']
                stockCount = stock['stockCount']
        if not stockFound:
            await message.channel.send("You specified stock was not found, maybe you wrote the command wrong....")
            await message.channel.send("The right way is [*sell <stock name> <ammount>]")
            return
        accountFound = False
        accountStocks = None
        Balance = 0
        notEnoughStocks = False
        stocksLeft = 0
        noStock = False
        for account in account_read:
            if account['userID'] == message.author.id:
                accountFound = True
                accountStocks = account['stocks']
                Balance = account['balance']
                if commandInfo[0] not in accountStocks:
                    noStock = True
                else:
                    stocksLeft = accountStocks[commandInfo[0]] - sellAmmount
                    if stocksLeft < 0:
                        notEnoughStocks = True
        if not accountFound:
            await message.channel.send("You don't have an investing account, you can make one using [*create account]")
            return
        if noStock:
            await message.channel.send("You have never bought or sold this Stock....")
            return
        if notEnoughStocks:
            await message.channel.send(f"You don't have enough stocks to sell, there is only {accountStocks[commandInfo[0]]} available")
            return
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        transactionData = {"userID": message.author.id, 
                           "actionType": "sell", 
                           "stockName": commandInfo[0],
                           "Ammount": sellAmmount,
                           "stockPrice": Price, 
                           'date': dt_string}
        Balance += sellAmmount * Price
        stockCount += sellAmmount
        accountStocks[commandInfo[0]] -= sellAmmount
        dbAccounts.update_one({'userID': message.author.id}, {'$set': {'stocks': accountStocks, 'balance': Balance}})
        dbStocks.update_one({'name': commandInfo[0]}, {'$set': {'stockCount': stockCount}})
        dbTransactions.insert_one(transactionData)
        await message.channel.send(f"You successfully sold {sellAmmount} of {commandInfo[0]} at this price: {Price}")
    
    if message.content == "$list my stocks":
        accountFound = False
        accountStocks = None
        for account in account_read:
            if account['userID'] == message.author.id:
                accountFound = True
                accountStocks = account['stocks']
        if not accountFound:
            await message.channel.send("You don't have an investing account, you can make one using [*create account]")
            return
        for key, value in accountStocks.items():
            await message.channel.send(f"1) {key} = {value}")
    
    if message.content == "$balance":
        accountFound = False
        Balance = 0
        for account in account_read:
            if account['userID'] == message.author.id:
                accountFound = True
                Balance = account['balance']
        if not accountFound:
            await message.channel.send("You don't have an investing account, you can make one using [*create account]")
            return
        await message.channel.send(f"Your balance is ${Balance}")
    
    if message.content == "$help":
        await message.channel.send(CommandHelp)
    
    if owner_found:
        if '$create stock' in message.content:
            commandInfo = message.content.split(' ')
            commandInfo.remove('$create')
            commandInfo.remove("stock")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            eventID = random.randint(1, 10000000000000000)
            

            stockData = {'name': commandInfo[0], 
                         'currentPrice': 0, 
                         'priceHistory': {dt_string: 0}, 
                         'stockCount': int(commandInfo[1]), 
                         'corporationPrice': int(commandInfo[2]), 
                         'eventIDs': [eventID]}
            eventData = {'stockName': commandInfo[0], 
                         'eventID': eventID, 
                         'content': f"{commandInfo[0]} stock got created! Happy investing!", 
                         'priceChange': "None"}
            dbStocks.insert_one(stockData)
            dbEvents.insert_one(eventData)
            await message.channel.send(f"Stock Created, stock name = {commandInfo[0]}, stock count = {commandInfo[1]}, corporation price = {commandInfo[2]}")

client.run(TOKEN)