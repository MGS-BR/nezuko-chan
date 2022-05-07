import disnake
import json

from pymongo import MongoClient
from disnake.ext import commands

from cogs.utilities.databaseUsage import database

class commandChannel():

    async def checkChannel(ctx):

        guild_db = await database.guild(ctx)

        if ctx.channel.id in guild_db["ch_command"]:

            if guild_db["alerts"]["command_usage"]["stats"] == True:

                await ctx.send(guild_db["alerts"]["command_usage"]["message"])

                return True

        return False

