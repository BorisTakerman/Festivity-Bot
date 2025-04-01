import discord
import json
from discord.ext import commands

# Load stored names or create an empty dictionary
try:
    with open("names_backup.json", "r") as f:
        original_names = json.load(f)
except FileNotFoundError:
    original_names = {}

# Bot setup
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to flip and reverse text
def flip_and_reverse(text):
    flipped = text[::-1]  # Reverse the text
    return flipped

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def AprilFools(ctx):
    "Flips all channel names and nicknames for April Fools."
    for guild in bot.guilds:
        # Flip channel names
        for channel in guild.channels:
            if str(channel.id) not in original_names:
                original_names[str(channel.id)] = channel.name
            flipped_name = flip_and_reverse(channel.name)
            await channel.edit(name=flipped_name)

        # Flip member nicknames
        for member in guild.members:
            if member.nick and str(member.id) not in original_names:
                original_names[str(member.id)] = member.nick
                flipped_nick = flip_and_reverse(member.nick)
                await member.edit(nick=flipped_nick)

    # Save the original names to file
    with open("names_backup.json", "w") as f:
        json.dump(original_names, f)
    
    await ctx.send("April Fools prank activated! All names flipped!")
    print("All names flipped!")

@bot.command()
async def restore(ctx):
    "Restores all channel names and nicknames to original values."
    with open("names_backup.json", "r") as f:
        original_names = json.load(f)
    
    for guild in bot.guilds:
        for channel in guild.channels:
            if str(channel.id) in original_names:
                await channel.edit(name=original_names[str(channel.id)])
        for member in guild.members:
            if str(member.id) in original_names and member.nick:
                await member.edit(nick=original_names[str(member.id)])
    
    await ctx.send("Server restored to normal!")

# Run the bot
bot.run("YOUR_BOT_TOKEN")
