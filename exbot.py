import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
import wikipediaapi

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


# Command: Roll
@bot.command(name='roll')
async def roll(ctx, dice: str):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")

    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception as e:
        await ctx.send("Invalid dice format. Use the format `!roll NdM`, e.g., `!roll 2d6`.")
        return

    result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
    await ctx.send(f'Rolls: {result}')


# Command: 8ball
@bot.command(name='8ball')
async def eight_ball(ctx, *, question: str):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")

    responses = [
        "Yes",
        "No",
        "Maybe",
        "Ask again later",
        "Cannot predict now",
        "Don't count on it",
        "Outlook not so good",
        "Certainly not",
    ]
    response = random.choice(responses)
    await ctx.send(f'Question: {question}\nAnswer: {response}')

# Command: Server Info
@bot.command(name='serverinfo')
async def serverinfo(ctx):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")

    guild = ctx.guild
    embed = discord.Embed(title=f"Server Information - {guild.name}", color=0x00ff00)
    embed.add_field(name="Server ID", value=guild.id, inline=False)
    embed.add_field(name="Members", value=guild.member_count, inline=False)
    embed.add_field(name="Creation Date", value=guild.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.set_thumbnail(url=guild.icon_url)
    await ctx.send(embed=embed)


# Command: User Info
@bot.command(name='userinfo')
async def userinfo(ctx, user: discord.Member = None):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")

    user = user or ctx.author
    embed = discord.Embed(title=f"User Information - {user.name}", color=0x00ff00)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Nickname", value=user.nick, inline=False)
    embed.add_field(name="Roles", value=", ".join(role.name for role in user.roles), inline=False)
    embed.add_field(name="Joined Server", value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name="Account Created", value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)


# Command: Avatar
@bot.command(name='avatar')
async def avatar(ctx, user: discord.Member = None):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")

    user = user or ctx.author
    await ctx.send(f"Avatar of {user.name}: {user.avatar_url}")


# Command: Kick
@bot.command(name='kick')
async def kick(ctx, user: discord.Member, *, reason=None):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")

    if ctx.author.guild_permissions.kick_members:
        await user.kick(reason=reason)
        await ctx.send(f"{user.name} has been kicked.")
    else:
        await ctx.send("You don't have permission to kick members.")


# Command: Ban
@bot.command(name='ban')
async def ban(ctx, user: discord.Member, *, reason=None):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")

    if ctx.author.guild_permissions.ban_members:
        await user.ban(reason=reason)
        await ctx.send(f"{user.name} has been banned.")
    else:
        await ctx.send("You don't have permission to ban members.")
        
# Command: Wikipedia
@bot.command(name='wikipedia')
async def wikipedia(ctx, query):
    print(f"Command invoked by: {ctx.author.name} ({ctx.author.id})")

    wiki_wiki = wikipediaapi.Wikipedia('en')  # You can change the language code if needed
    page_py = wiki_wiki.page(query)

    if page_py.exists():
        # Create and send an embed with Wikipedia information
        embed = discord.Embed(title=f"{query.capitalize()} on Wikipedia", color=0x00ff00)
        embed.add_field(name="Summary", value=page_py.text[:500], inline=False)  # Display first 500 characters
        embed.add_field(name="Link", value=page_py.fullurl, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No Wikipedia page found for {query}.")        


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
