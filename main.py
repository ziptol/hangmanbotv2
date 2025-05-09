# imports
import os
import discord 
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timedelta
import hangmanGame
import leaderboard as lb
import birthdaybot as bd
import random
import connectfour

# grab env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
HOMECHANNEL = int(os.getenv('HOMECHANNEL'))

# settings
WORDLISTFILENAME = "assets/english-nouns.txt"
LEADERBOARDFILENAME = "leaderboard.txt"
COMMANDPREFIX = "?"
C4WINPOINTS = 3
HMWINPOINTS = 1
BIRTHDAYFILENAME = "birthdays.csv"

class MyClient(discord.Client):

    # ---------------------------------------------------------------------------- #
    #                                Initialization                                #
    # ---------------------------------------------------------------------------- #
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

        # games
        self.hangGame = None
        self.conGame = None
        self.home_channel = None

    # on ready
    async def on_ready(self):
        print(f'Up in this shit. Logged in as {self.user}')
        
        # initialize birthday check task
        asyncio.create_task(self.daily_task())

        # set home channel
        self.home_channel = self.get_channel(HOMECHANNEL)
        if self.home_channel:
            print(f"Home channel: {self.home_channel}")
        else:
            print("Home channel not found!")


    # ---------------------------------------------------------------------------- #
    #                                Daily Task                                    #
    # ---------------------------------------------------------------------------- #
    async def daily_task(self):
        await self.wait_until_ready()  # Make sure bot is ready

        while not self.is_closed():
            now = datetime.now()
            print(now)
            # Set target time (5 seconds past midnight)
            target_time = now.replace(hour=0, minute=0, second=5, microsecond=0)

            # If time has passed today, schedule for tomorrow
            if now >= target_time:
                target_time += timedelta(days=1)

            wait_seconds = (target_time - now).total_seconds()
            print(f"Sleeping for {wait_seconds} seconds until birthday check.")
            await asyncio.sleep(wait_seconds)

            # Check for birthdays and send message
            birthday_people = bd.check_birthdays(BIRTHDAYFILENAME)
            if birthday_people and self.home_channel:
                message = "🎉 Happy Birthday to: " + ", ".join(birthday_people) + "!"
                await self.home_channel.send(message)
            else:
                print("No birthdays today.")

            # Sleep for 24 hours
            await asyncio.sleep(24 * 60 * 60)

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

                case "george":
                    await message.channel.send("https://youtu.be/AwZG9NLAGmg")

                case "tag":
                    await message.channel.send("https://www.youtube.com/watch?v=rV5A3uvxqQI")

                case "dice":
                    file = discord.File("assets/fuckDice.jpg")
                    embed = discord.Embed()
                    embed.set_image(url="attachment://fuckDice.jpg")                    
                    await message.channel.send(file=file, embed=embed)
                
                case "aria":
                    file = discord.File("assets/nwalkpie.png")
                    embed = discord.Embed()
                    embed.set_image(url="attachment://nwalkpie.png")                    
                    await message.channel.send(file=file, embed=embed)
                
                case "slime":
                    await message.channel.send("https://www.amazon.com/Awkward-Styles-Autism-T-Shirt-Toddler/dp/B08534BD4T/ref=sr_1_2_sspa?crid=W1GA96OIR4US&dib=eyJ2IjoiMSJ9.Hobyjo941-GLgqwSbPROaT54QEaW0pQjpmzzaw6q3ALr_SViuIaaAsAeoOxvZGbly-RinWi7GU_c-7lfQh_7HMcqXdAXaKLVce7wu67onmPswvt6nxml_14vYWlLwd-zZOQq0W04W8oGbroix9eSY7sjSA0PiWPNk7f11jMqIejgDoBxbkEFr8KDGkTIdN1GHRU40fHaS68_RQValzdBvFxl7WmlMtodsaiQpz-_pP7A-iIPMuTY7apmvvRn5qurvsNch7fv-Xjanhx5QSAIbPnCS6j9f5MPDRQjOmRNycc.MoHsDoOs9MjcJ6CqYXngr89Q7ttSMCw7TqbPxPqAZU8&dib_tag=se&keywords=autism+shirt&qid=1715286134&sprefix=autism+shirt%2Caps%2C107&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1")
                
                # ----------------------------- Birthday Commands ----------------------------- #
                case "addbday":
                    parts = message.content.strip().split()

                    if len(parts) != 3:
                        await message.channel.send("fuck you. do addbirhtday <name> <MM-DD>")
                        return

                    username, date = parts[1], parts[2]

                    try:
                        bd.add_birthday(BIRTHDAYFILENAME, username, date)
                        await message.channel.send(f"Added birthday: {username} - {date}")
                    except ValueError as ve:
                        await message.channel.send(f"Error: {ve}")
                    except Exception as e:
                        print("Failed to add birthday. Check server logs.")

                case "listbdays":
                    birthdays = bd.list_birthdays(BIRTHDAYFILENAME)
                    if not birthdays:
                        await message.channel.send("No birthdays found")
                    else:
                        formatted = "\n".join(birthdays)
                        await message.channel.send(f"**Birthday List:**\n{formatted}")

                case "removebday":
                    parts = message.content.strip().split()

                    if len(parts) != 2:
                        await message.channel.send("fuck you. do removebday <name>")
                        return

                    username = parts[1]

                    try:
                        success = bd.remove_birthday(BIRTHDAYFILENAME, username)
                        if success:
                            await message.channel.send(f"Removed birthday entry for {username}.")
                        else:
                            await message.channel.send(f"No birthday found for {username}.")
                    except Exception as e:
                        print(f"Error: {e}")
                        await message.channel.send("Failed to remove birthday. Check server logs.")

                # ----------------------------- Hangman Commands ----------------------------- #
                # Start a game of hangman, takes no parameters
                case "hangman":
                    # if no active game, start one
                    if(self.hangGame == None):
                        self.hangGame = hangmanGame.HG(self.wordlist, 6)
                        homeMessage = await message.channel.send(self.hangGame.display()[1])
                        self.hangGame.setHomeMessage(homeMessage)
                        print(self.hangGame.getWord())
                    # if there's an active game, tell players to end it
                    else:
                        await message.channel.send(f"There's already an active game dumbass, use {COMMANDPREFIX}hangstop to end it")
                
                # Guess a hangman word, takes either a single letter or the full word
                case "guess":
                    # if no active game, tell players to start one
                    if(self.hangGame == None):
                        await message.channel.send(f"There's no game, use {COMMANDPREFIX}hangman to start one!")
                        return
                    # Run hangman guess code
                    guessVal = message.content.split(" ")[1]
                    guessReturn = self.hangGame.guess(guessVal)
                    # Display game board
                    await self.hangGame.getHomeMessage().edit(content = guessReturn[1])
                    # Check for win or loss
                    if(guessReturn[0] == 1 or guessReturn[0] == 2):
                        self.hangGame = None
                        # If won, add to leaderboard
                        if(guessReturn[0] == 1):
                            lb.incLeaderboard(LEADERBOARDFILENAME,str(message.author.name),HMWINPOINTS)
                
                # Stop hangman game, takes no parameters
                case "hangstop":
                    # If no active game
                    if(self.hangGame == None):
                        await message.channel.send("There's no game going, but I guess I can try...")
                    await message.channel.send("Ending game!")
                    self.hangGame = None

                # --------------------------- Connect Four Commands -------------------------- #
                # Start a game of connect four
                case "connectfour":
                    # if no active game
                    if self.conGame == None:
                        # create new connect four game 
                        self.conGame = connectfour.C4()
                        homeMessage = await message.channel.send(self.conGame.display()[1])
                        self.conGame.setHomeMessage(homeMessage)
                    # if there is an active game
                    else:
                        await message.channel.send(f"There's a game going! To stop it use {COMMANDPREFIX}connectstop")
                
                case "drop":
                    # if no active game, tell players to start one
                    if(self.conGame == None):
                        await message.channel.send(f"There's no game, use {COMMANDPREFIX}connectfour to start one!")
                        return
                    # get desired row
                    rowDrop = message.content.split(" ")[1]
                    dropReturn = self.conGame.droppiece(rowDrop,message.author.name)
                    # display game board
                    await self.conGame.getHomeMessage().edit(content = dropReturn[1])
                    # Check for win or loss
                    if(dropReturn[0] != 0):
                        self.conGame = None
                        if(dropReturn[0] == 1):
                            lb.incLeaderboard(LEADERBOARDFILENAME,str(message.author.name),C4WINPOINTS)

                    await message.delete()

                case "connectstop":
                    # If no active game
                    if(self.conGame == None):
                        await message.channel.send("There's no game going, but I guess I can try...")
                    await message.channel.send("Ending game!")
                    self.conGame = None
                
                # --------------------------------- Dice Bot --------------------------------- #
                # Roll dice, takes integer >= 1 
                case "roll":
                    rollVal = message.content.split(" ")[1]
                    try:
                        rollInt = int(rollVal)
                    except:
                        await message.channel.send("Invalid roll")
                        return
                    await message.channel.send(f"Rolling d{rollInt}...")
                    await message.channel.send("You rolled: "+str(random.randint(1,rollInt)))

                # ------------------------------- Utilities ------------------------------ #
                # Display help message, takes no parameters
                case "help":    
                    await message.channel.send("I cant be bothered tbh")

                # Get leaderboard, takes no parameters
                case "leaderboard":
                    print("sending leaderboard!")
                    # display leaderboard 
                    leadermessage = "**Leaderboard:**\n"
                    for line in lb.getLeaderboard(LEADERBOARDFILENAME):
                        leadermessage += str(line[0])+": "+str(line[1])+"\n"
                        
                    print(leadermessage)
                    await message.channel.send(leadermessage)

                


# set intents
intents = discord.Intents.default()
intents.message_content = True

# run bot
client = MyClient(intents=intents, wordListFileName=WORDLISTFILENAME, commandPrefix=COMMANDPREFIX)
client.run(TOKEN)