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


# Event: Greet new members
@bot.event
async def on_member_join(member):
    print(f'New member joined: {member.name} ({member.id})')

    # Send a welcome message
    welcome_channel = member.guild.system_channel  # You can customize this to the channel you want
    if welcome_channel:
        await welcome_channel.send(f'Welcome, {member.mention}!')


# Event: Member leaves
@bot.event
async def on_member_remove(member):
    print(f'Member left: {member.name} ({member.id})')

    # Perform actions when a member leaves


# Event: Member status update
@bot.event
async def on_member_update(before, after):
    if before.status != after.status and after.status == discord.Status.online:
        print(f'Member {after.name} ({after.id}) came online after being offline.')

        # Send a welcome back message
        welcome_channel = after.guild.system_channel  # You can customize this to the channel you want
        if welcome_channel:
            await welcome_channel.send(f'Welcome back, {after.mention}!')


# Command: Hello
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


# Command: Ping
@bot.command(name='ping')
async def ping(ctx):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")
    latency = bot.latency * 1000  # Convert to milliseconds
    await ctx.send(f'Pong! Latency: {latency:.2f}ms')


# Command: Info
@bot.command(name='info')
async def info(ctx):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")
    embed = discord.Embed(title="Bot Information", color=0x00ff00)
    embed.add_field(name="Creator", value="Your Name", inline=False)
    embed.add_field(name="Version", value="1.0", inline=False)
    await ctx.send(embed=embed)


# Event: Process Commands
@bot.event
async def on_message(message):
    if message.author == bot.user or not message.content.startswith('!'):
        return  # Ignore messages from the bot and messages without the prefix

    print(f"Message received: {message.content}")

    # Process commands
    await bot.process_commands(message)


# Run the bot
bot.run(DISCORD_BOT_TOKEN)
