import disnake
import os
import json

from disnake.ext import commands
from pymongo import MongoClient

from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    token = infos["token"]
    connection_mongo = infos["mongo"]

cluster = MongoClient(connection_mongo)

cluster_guilds = cluster["discord"]["guilds"]

client = commands.Bot(command_prefix=commands.when_mentioned_or("n!"), intents=disnake.Intents.all(), test_guilds=[863538221366509578])

client.remove_command("help")

@client.event
async def on_ready():

    print(f"{client.user.name} ON\n{len(client.guilds)} servers\n{len(client.all_slash_commands)} comandos\n{len(client.users)} usuários")
    
    await client.change_presence(activity=disnake.Game(name="discord.gg/nYsRbxC8cc"))

@client.event
async def on_message(message):

    if message.author.bot == True:
        return

    if isinstance(message.channel, disnake.DMChannel):

        if message.content in [f"<@{client.user.id}>", f"<@!{client.user.id}>"]:

            await message.channel.send(f"{message.author.mention} | O meu prefixo é `/`, use `/help` caso precise de ajuda!")

        else:
            await client.process_commands(message)

    else:

        if message.content in [f"<@{client.user.id}>", f"<@!{client.user.id}>"]:

            guild_db = await database.guild(message)

            if guild_db["language"] == "portugues":

                await message.channel.send(f"{message.author.mention} | O meu prefixo é `/`, use `/help` caso precise de ajuda!")

            else:

                await message.channel.send(f"{message.author.mention} | My prefix is ​​`/`, use `/help` if you need help!")

        else:
            await client.process_commands(message)

for filename in os.listdir("./cogs/commands/normal"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.commands.normal.{filename[:-3]}")

for filename in os.listdir("./cogs/commands/admin"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.commands.admin.{filename[:-3]}")

for filename in os.listdir("./cogs/commands/tags"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.commands.tags.{filename[:-3]}")

for filename in os.listdir("./cogs/errors"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.errors.{filename[:-3]}")

for filename in os.listdir("./cogs/custom"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.custom.{filename[:-3]}")

client.run(token)