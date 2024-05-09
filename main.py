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
COMMANDPREFIX = "?"

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

        # hangman
        self.hangGame = None

    # on ready
    async def on_ready(self):
        print(f'Up in this shit. Logged in as {self.user}')

    # ---------------------------------------------------------------------------- #
    #                                Command Handler                               #
    # ---------------------------------------------------------------------------- #
    async def on_message(self,message):
        # ignore own message
        if message.author.id == self.user.id:
            return
        
        # command handler
        if message.content.startswith(self.commandPrefix):
            # extract command (last letters of first word)
            command = (message.content.split(" ")[0])[1:]
            match command:

                # ------------------------------- Misc Commands ------------------------------ #
                case "hi":
                    print("Hi command recieved")
                    await message.channel.send("Wassup")
                
                case "durv":
                    embed = discord.Embed()
                    embed.set_image(url="https://media.discordapp.net/attachments/540314464994459656/947874538291597373/3A12A02F-065E-4EE2-981A-7B3590FE5A8B.gif?ex=663d9134&is=663c3fb4&hm=727946ebf7f38be776f69c6cab8ed8e354d88f54f63305d445ed3798b93acaac&=&width=540&height=720")
                    await message.channel.send(embed=embed)

                # ----------------------------- Hangman Commands ----------------------------- #
                # Start Game
                case "hangman":
                    # if no active game, start one
                    if(self.hangGame == None):
                        self.hangGame = hangmanGame.HG(self.wordlist, 6)
                        homeMessage = await message.channel.send(self.hangGame.display()[1])
                        self.hangGame.setHomeMessage(homeMessage)
                    # if there's an active game, tell players to end it
                    else:
                        await message.channel.send("There's already an active game dumbass, use !hangstop to end it")
                
                # Guess
                case "guess":
                    # if no active game, tell players to start one
                    if(self.hangGame == None):
                        await message.channel.send("There's no game, use !hangman to start one!")
                        return
                    # Run hangman guess code
                    guessVal = message.content.split(" ")[1]
                    guessReturn = self.hangGame.guess(guessVal)
                    # Display game board
                    await self.hangGame.getHomeMessage().edit(content = guessReturn[1])
                    # Check for win or loss
                    if(guessReturn[0] == 1 or guessReturn[0] == 2):
                        self.hangGame = None
                    
                # End Game
                case "hangstop":
                    # If no active game
                    if(self.hangGame == None):
                        await message.channel.send("There's no game going, but I guess I can try...")
                    await message.channel.send("Ending game!")
                    self.hangGame = None

                # ------------------------------- Trash Cleanup ------------------------------ #
                case "help":    
                    await message.channel.send("I cant be bothered tbh")


# set intents
intents = discord.Intents.default()
intents.message_content = True

# run bot
client = MyClient(intents=intents, wordListFileName=WORDLISTFILENAME, commandPrefix=COMMANDPREFIX)
client.run(TOKEN)