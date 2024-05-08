# imports
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

# grab env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# grab hangman words list
wordlistFileName = "english-nouns.txt"
wordlistFile = open(wordlistFileName, "r")
wordlist = []
for line in wordlistFile:
    wordlist.append(line)
wordlistFile.close()
wordlistLength = len(wordlist)

# hangman game state
hangIsActive = 0
hangActiveMessage = ""
hangWord = ""
hangGuessed = []

# set intents
intents = discord.Intents.default()
intents.message_content = True

# run bot
bot = commands.Bot(intents=intents,command_prefix='!')


# ------------------------------- Misc Commands ------------------------------ #
# Startup
@bot.event
async def on_ready():
    print(f'Up in this shit. Logged in as {bot.user}')

# Hi
@bot.command(description = "hi")
async def hi(ctx):
    await ctx.send("Hi")

# Durv
@bot.command(description = "durv time")
async def durv(ctx):
    await ctx.send("Durv")

# ---------------------------------- Hangman --------------------------------- #

@bot.command(description = "Starts a game of hangman")
async def hangman(ctx):

    # determine if a game is currently active
    global hangIsActive
    if hangIsActive == 1:
        await ctx.send("A hangman game is currently active, type !hangstop to close it")
        return

    # establish hangman word
    wordlistIndex = random.randint(0, wordlistLength)
    await ctx.send(hangWord)

    # display play board
    hangWordLength = len(hangWord)
    hangDisplay = "\_  "*hangWordLength
    global hangActiveMessage
    hangActiveMessage = await ctx.send(hangDisplay)

    # set hangman gamestate
    hangIsActive = 1

@bot.command(description = "Gets hangman game status")
async def hangstatus(ctx):
    await ctx.send(f'Active({hangIsActive}), Messageid({hangActiveMessage}), Word({hangWord})')

@bot.command(description = "Stops a hangman game")
async def hangstop(ctx):
    hangIsActive = 0
    hangActiveMessage = ""
    await ctx.send(f'Ending hangman game, the word was {hangWord}')

bot.run(TOKEN)