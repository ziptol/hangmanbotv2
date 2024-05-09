# imports
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import hangmanGame

# grab env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# settings
WORDLISTFILENAME = "english-nouns.txt"
COMMANDPREFIX = "!"

class MyClient(discord.Client):

    # initialize variables
    def __init__(self, intents, wordListFileName, commandPrefix):
        
        discord.Client.__init__(self, intents=intents)

        # commands
        self.commandPrefix = commandPrefix

        # get word list
        wordlistFile = open(WORDLISTFILENAME, "r")
        self.wordlist = []
        for line in wordlistFile:
            self.wordlist.append(line)
        wordlistFile.close()

    # on ready
    async def on_ready(self):
        print(f'Up in this shit. Logged in as {self.user}')

    # command handling
    async def on_message(self,message):
        # ignore own message
        if message.author.id == self.user.id:
            return
        
        # command handler
        if message.content.startswith(self.commandPrefix):
            # extract command (last letters of first word)
            command = (message.content.split(" ")[0])[1:]
            match command:

                # Misc Commands
                case "hi":
                    await message.channel.send("Wassup")

                # Hangman Commands
                case "hangman":
                    self.hangGame = hangmanGame.HG(self.wordlist, 6)
                    await message.channel.send(self.hangGame.display())
                
                case "guess":
                    guessVal = message.content.split(" ")[1]
                    await message.channel.send(self.hangGame.guess(guessVal))


# set intents
intents = discord.Intents.default()
intents.message_content = True

# run bot
client = MyClient(intents=intents, wordListFileName=WORDLISTFILENAME, commandPrefix=COMMANDPREFIX)
client.run(TOKEN)