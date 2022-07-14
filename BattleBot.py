# Vincent Paone
# Project began 6/30/2022 --
# BattleBot - main file
#


from array import array
from ast import alias
import time
import os
import re
import json
import discord
import asyncio
from tokenize import String
from discord.ext import commands
from discord.utils import get
import random
from types import SimpleNamespace

# search for the config.json file in the current directory and load the file
current_directory = os.getcwd()
print(current_directory)
# mac and windows treat file paths differently so you may need to change this string below to the exact file path of your config
if os.path.exists(os.getcwd() + "/config.json"):
    print("CONFIG PATH EXISTS")
    with open("./config.json") as f:
        configData = json.load(f)
        print("CONFIG OPENED")

# if the config file doesn't exist within the current directory, use the template to create the file automatically
else:
    print("CONFIG PATH DOES NOT EXIST")
    configTemplate = {"Token": "", "Prefix": ""}

    with open(os.getcwd() + "/config.json", "w+") as f:
        # dump the configTemplate to the new config.json
        json.dump(configTemplate, f)
        print("NEW CONFIG CREATED USING PROVIDED TEMPLATE")

# grab some info from the config file
TOKEN = configData["TOKEN"]
prefix = configData["PREFIX"]

# search for the c.json file in the current directory and load the file
if os.path.exists(os.getcwd() + "/c.json"):
    print("CHARACTER JSON EXISTS")
    with open("./c.json") as f:
        cData = json.load(f)
        print("CHARACTERS JSON OPENED")

# if the c file doesn't exist use the template to create the file
else:
    cTemplate = {"CHARACTER 1": [{"NAME": ""},{"HP": ""},{"ATTACK": ""},{"DEFENSE": ""},{"SANITY": ""}],"CHARACTER 2": [{"NAME": ""},{"HP": ""},{"ATTACK": ""},{"DEFENSE": ""},{"SANITY": ""}]}

    print("TEMPLATE USED TO CREATE CHARACTER JSON (C.JSON) IN THE CURRENT DIRECTORY")
    with open(os.getcwd() + "./c.json", "w+") as f:
        json.dump(cTemplate, f)  # dump the character template to new c.json

# pull the data from the character json
char1 = cData["CHARACTER 1"]
char2 = cData["CHARACTER 2"]


# print character sheets to the console
print(f"{char1}\n")
print(f"{char2}\n")

print(type(char1))
print(type(char2))


for attr in char1:
    for stat in attr:
        print(stat)
    print(attr)


# we need to assign the prefix to the bot and denote the bot as 'client'
# 'client' can be called anything it is just a variable to refer to the bot
client = commands.Bot(command_prefix=prefix)

# we need this to check the bot connected properly in the on_ready fxn
full_ready = False

# wait for the bot to FULLY connect to the server
# once bot connects print message in local terminal


@client.event
async def on_ready():
    print('$$$$$ We have logged in as {0.user} $$$$$'.format(client))
    print(f'$$$$$ {client} $$$$$')
    full_ready = True

    # if full_ready == True:
    #     print('$$$$$ Loading Cogs...standby $$$$$')
    #     loadCogs()
    # else:
    #     print('$$$$$ Bot not ready, Cogs not loaded $$$$$')

# every time there is a message in any channel in any guild, this runs
# param: message - The message content that was last sent


@client.event
async def on_message(message):

    # grabs username, user unique id, and the user message
    messageAuthor = message.author
    user_id = str(message.author.id)
    user_message = str(message.content)

    # cleaned up username without # id
    username = str(message.author).split('#')[0]

    # channel name the message was sent from
    channel = str(message.channel.name)
    # server name the message was sent from
    guild = str(message.guild.name)

    # on every message print it to the terminal
    # print the username, the message, the channel it was sent in and the server (guild)
    # print(f'{username}: {user_message} [userid= {user_id} (channel= {channel})]')
    print(f'{username}: {user_message} \t(channel= {channel} on server= {guild})')
    # ignore messages sent from the bot itself
    # prevents infinite replying
    if message.author == client.user:
        return
    # if message starts with 'hello'
    if user_message.lower().startswith('hello'):
        await message.channel.send(f'Hello {messageAuthor.mention}!')
        return
    # necessary to process anything the bot will do
    await client.process_commands(message)


@client.command(aliases=['create', 'cr'])
async def create_fighter(ctx):
    print("")

@client.command(aliases=['f', 'battle', 'b'])
async def fight(ctx, player2):
    player1 = ctx.message.author
    print(player1)
    player2 = ctx.message.mentions[0]
    print(player2)
    
    print(type(player1))
    print(type(player2))
    
    char1 = [{"NAME": "FIGHTER A"}, {"HEALTH": 10}, {"ATTACK": 10}]
    char1name = char1[0]["NAME"]
    char1hp = char1[1]["HEALTH"]
    char1atk = char1[2]["ATTACK"]
    
    char2 = [{"NAME": "FIGHTER B"}, {"HEALTH": 30}, {"ATTACK": 5}]
    char2name = char2[0]["NAME"]
    char2hp = char2[1]["HEALTH"]
    char2atk = char2[2]["ATTACK"]

    fighters = [char1, char2]


    await ctx.send(f'{player1.mention} WANTS TO BATTLE {player2.mention}!\n{player2.mention} DO YOU ACCEPT? (REPLY YES/NO)')

    try:

        msg = await client.wait_for('message', timeout=10.0, check=lambda message: message.author == player2)

        print(ctx.author)
        message = str(msg.content)

        print(msg.author)
        
        if message.lower() == "yes":
            await ctx.channel.send(f'WHO PICKS THEIR CHARACTER FIRST? COIN FLIP WILL DECIDE! {player1.mention} HEADS, OR TAILS?')
        
            validanswer=False
            while validanswer==False :
                try: 
                    msg = await client.wait_for('message', timeout=10.0, check=lambda message: message.author == player1)
                    message = str(msg.content)
                    print(message)
                    if "heads" == message.lower() or "tails" == message.lower():
                        print("CORRECT INPUT")
                        validanswer=True
                    else: 
                        print("WRONG INPUT")
                        await ctx.channel.send(f"{player1.mention} PLEASE ENTER A VALID ANSWER, EITHER \"HEADS\" OR \"TAILS\"")
                        validanswer=False
                except asyncio.TimeoutError:
                    await ctx.channel.send(f"ERROR: Timeout Exception, {player2.mention} wins by default.")
                    break # need to break out of the while loop after 1 timeout error
                    
                    
            if message.lower() == "heads":
                if coinflip() == "heads":
                    await ctx.channel.send(f"{player1.mention} WON THE COIN TOSS AND WILL CHOOSE FIRST")
                    firstpick = player1
                    secondpick = player2
                else:
                    await ctx.channel.send(f"{player2.mention} WON THE COIN TOSS AND WILL CHOOSE FIRST")
                    firstpick = player2
                    secondpick = player1
            elif message.lower() == "tails":
                if coinflip() == "tails":
                    await ctx.channel.send(f"{player1.mention} WON THE COIN TOSS AND WILL CHOOSE FIRST")
                    firstpick = player1
                    secondpick = player2
                else:
                    await ctx.channel.send(f"{player2.mention} WON THE COIN TOSS AND WILL CHOOSE FIRST")
                    firstpick = player2
                    secondpick = player1
                    
        else:
            await ctx.channel.send(f"{player2.mention} HAS DENIED THE BATTLE REQUEST, {player1.mention} WINS BY DEFAULT")
                    
    

    except asyncio.TimeoutError:
        await ctx.channel.send(f"ERROR: Timeout Exception, {player1.mention} wins by default.")
    
    await ctx.channel.send(f"{firstpick.mention} WHICH FIGHTER DO YOU CHOOSE?\n")
    await ctx.channel.send(f"```----- FIGHTER 1 -----\n\nNAME: {char1name}\nHEALTH: {char1hp}\nATTACK: {char1atk}\n\n\n\t\tOR\n\n\n----- FIGHTER 2 -----\n\nNAME: {char2name}\nHEALTH: {char2hp}\nATTACK: {char2atk}\n\n\nENTER THE NUMBER OF THE FIGHTER YOU CHOOSE. (i.e. \"2\")```")

    char_select = await client.wait_for('message', timeout=10.0, check=lambda message: message.author == firstpick) 

    char_select_format = int(char_select.content) - 1
    firstpick_fighter = fighters[char_select_format]
    print(fighters[char_select_format])
    await ctx.channel.send(f"{firstpick} CHOOSES {firstpick_fighter}")



def coinflip():
    outcome = random.choice(["heads", "tails"])
    print(outcome)
    return outcome

def loadCogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                # -3 cuts the .py extension from filename
                client.load_extension(f'cogs.{filename[:-3]}')
                print(f'----- Cog {filename} loaded -----')
            except commands.ExtensionAlreadyLoaded:
                print(f'----- Cog {filename} aleady loaded -----')

# Function to unload all Cogs in the cogs folder
# Runs on -rl all


def unloadCogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                client.unload_extension(f'cogs.{filename[:-3]}')
                print(f'----- Cog {filename} unloaded successfully -----')
            except commands.ExtensionNotLoaded:
                print(f'----- Cog {filename} is not loaded -----')

# Load a Cog file
# do $load "name of cog file"
# only admin should be able to run this
# param: ctx - The context in which the command has been executed
# param: extension - The name of the Cog file you want to load


@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'```Cog {extension}.py loaded```')
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f'```{extension}.py is already loaded```')
    except commands.ExtensionNotFound:
        await ctx.send(f'```{extension}.py does not exist```')


# Unload a Cog file
# do $unload "name of cog file"
# only admin should be able to run this
# param: ctx- The context of which the command is entered
# param: extension - The name of the Cog file to unload
@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Cog {extension}.py unloaded')
    except commands.ExtensionNotLoaded:
        await ctx.send(f'{extension}.py is not loaded')
    except commands.ExtensionNotFound:
        await ctx.send(f'{extension}.py does not exist')


# does unload then load of cog file
# do $rl or $refreshload "name of cog file"
# only admin should be able to run this
# param: ctx - The context in which the command has been executed
# param: extension - The name of the Cog file to reload
# do $rl all to unload/load all Cogs
@client.command(aliases=['rl'], description='Reloads all Cog files')
@commands.has_permissions(administrator=True)
async def refreshload(ctx, extension):

    if extension == 'all':
        unloadCogs()
        await ctx.send(f'``` All Cogs unloaded successfully```')
        time.sleep(2)
        loadCogs()
        await ctx.send(f'``` All Cogs loaded successfully```')
    else:
        try:
            client.unload_extension(f'cogs.{extension}')
            await ctx.send(f'```Cog {extension}.py unloaded```')
            time.sleep(2)
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f'```Cog {extension}.py loaded```')
        except commands.ExtensionNotLoaded:
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f'```Cog {extension}.py loaded```')
        except commands.ExtensionNotFound:
            await ctx.send(f'```Cog {extension}.py not in directory```')


# # add a banned word to the bannedWords list in the json config
# # only admin should be able to run this
# # param: ctx - The context of which the command is entered
# # param: word - The word you want to be on the banned words list
# @client.command()
# @commands.has_permissions(administrator=True)
# # message can only be sent 1 time, every 3 seconds, per user.
# @commands.cooldown(1, 3, commands.BucketType.user)
# async def banword(ctx, word):
#     # check if the word is already banned
#     if word.lower() in bannedWords:
#         await ctx.send("```Already banned```")
#     else:
#         bannedWords.append(word.lower())
#         # add it to the list
#         with open("./config.json", "r+") as f:
#             data = json.load(f)
#             data["bannedWords"] = bannedWords
#             f.seek(0)
#             f.write(json.dumps(data))
#             f.truncate()  # resizes file

#         await ctx.send("```Word added to banned words list```")


# # remove a banned word from the bannedWords list in the json config
# # only admin should be able to run this
# # param: ctx The context of which the command is entered
# # param: word - The word you want to remove from the banned words list
# @client.command(aliases=['unban'])
# @commands.has_permissions(administrator=True)
# # message can only be sent 1 time, every 3 seconds, per user.
# @commands.cooldown(1, 3, commands.BucketType.user)
# async def rmvbannedword(ctx, word):
#     if word.lower() in bannedWords:
#         bannedWords.remove(word.lower())

#         with open("./config.json", "r+") as f:
#             data = json.load(f)
#             data["bannedWords"] = bannedWords
#             f.seek(0)
#             f.write(json.dumps(data))
#             f.truncate()

#         await ctx.send("```Word removed from banned words list```")

#     # if the word isn't in the list
#     else:
#         await ctx.send("```Word isn't banned```")

# # save information, username/password/nickname into a json
# # only admin should be able to run this
# # param: ctx The context of which the command is entered


# @client.command(aliases=['new_acc'])
# @commands.has_permissions(administrator=True)
# @commands.cooldown(1, 3, commands.BucketType.user)
# async def saveAccount(ctx):

#     # prompt #1 for username entry
#     await ctx.send(f"Enter in the Username you wish to add {ctx.author.mention}")
#     try:
#         user_message = await client.wait_for('message', timeout=15, check=lambda message: message.author == ctx.author)
#         username = str(user_message.content)
#     except asyncio.TimeoutError:
#         await ctx.channel.send("```ERROR: Timeout Exception```")

#     # prompt #2 for password entry
#     await ctx.send(f"Enter in the Password you wish to add {ctx.author.mention}")
#     try:
#         user_message = await client.wait_for('message', timeout=15, check=lambda message: message.author == ctx.author)
#         password = str(user_message.content)
#     except asyncio.TimeoutError:
#         await ctx.channel.send("```ERROR: Timeout Exception```")

#     # check if the account info is already in the list
#     if username.lower() in accUsers and password in accPasses:
#         userindex = accUsers.index(username)
#         passindex = accPasses.index(password)

#         if userindex == passindex:
#             await ctx.send(f"```Account info already exists at position indices {userindex} and {passindex}\n It will not be appended.```")
#     else:
#         # add it to the list
#         accUsers.append(username.lower())
#         accPasses.append(password)
#         with open("./acc.json", "r+") as f:
#             data = json.load(f)
#             data["Usernames"] = accUsers
#             data["Passwords"] = accPasses
#             f.seek(0)
#             f.write(json.dumps(data))
#             f.truncate()  # resizes file

#     # prompt #3 for nickname entry
#     await ctx.send(f"```Provide a nickname for this entry? Reply Y/N```")
#     user_message = await client.wait_for('message', timeout=15, check=lambda message: message.author == ctx.author)
#     user_reply = str(user_message.content)

#     if user_reply.lower() == "y":
#         await ctx.send("What would you like to name this entry?")
#         user_message = await client.wait_for('message', timeout=15, check=lambda message: message.author == ctx.author)
#         nickname = str(user_message.content)

#         if nickname.lower() in accNick:
#             await ctx.send("Nickname already exists in the list, default will be applied")
#             # have them try again, and enter Default for a default nickname to apply
#     else:
#         # if user does not want to apply a nickname a default will be chosen
#         await ctx.send("```No nickname chosen. Default will be applied.```")
#         nickname = username + '#' + str(accUsers.index(username))

#     accNick.append(nickname)
#     with open("./acc.json", "r+") as f:
#         data = json.load(f)
#         data["Account_name"] = accNick
#         f.seek(0)
#         f.write(json.dumps(data))
#         f.truncate()  # resizes file

#     await ctx.send(f"```Added the following account information:\n Username: {username}\n Password: {password}\n Nickname: {nickname}```")


# # clear all data from a json file the user chooses
# # only admin should be able to run this
# # param: ctx The context of which the command is entered
# # param: data_file The json file which the user wants wiped of data
# @client.command(aliases=['clean'])
# @commands.has_permissions(administrator=True)
# # message can only be sent 1 time, every 5 seconds, per user.
# @commands.cooldown(1, 5, commands.BucketType.user)
# async def cleardata(ctx, data_file):

#     data_file = "/" + data_file + ".json"
#     print(data_file)

#     if os.path.exists(os.getcwd() + data_file):
#         print("true")
#         with open("." + data_file, "r") as f:
#             data = json.load(f)
#             for o in data:
#                 data.pop(o)
#                 await ctx.send(f"Removed {o}")
#                 print("true")

#             f.seek(0)
#             f.write(json.dumps(data))
#             f.truncate()

#     else:
#         print("false")

client.run(TOKEN)
