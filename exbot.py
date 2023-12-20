import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)


# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Example command
@bot.command(name='hello')
async def hello(ctx):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")

    if isinstance(ctx.author, discord.Member):  # Check if the author is a Member (in a guild)
        if ctx.guild and ctx.author.guild_permissions.administrator:
            await ctx.send('Hello!')
        else:
            await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send("This command can only be used in a server.")

@bot.event
async def on_message(message):
    print(f"Message received: {message.content}")

    # Process commands
    await bot.process_commands(message)


# Run the bot
bot.run(DISCORD_BOT_TOKEN)
