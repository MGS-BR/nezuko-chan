import disnake
import json

from pymongo import MongoClient
from disnake.ext import commands

from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

cluster = MongoClient(connection_url)
cluster_guilds = cluster["discord"]["guilds"]
cluster_users = cluster["discord"]["users"]
cluster_guilds_xp = cluster["discord"]["guilds_xp"]

class LevelSystem(commands.Cog):
    """Cooldown error"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author.bot:

            return

        if isinstance(message.channel, disnake.DMChannel):

            return

        guild_db = await database.guild(message)
        user_db = await database.user(message)

        if message.channel.id in guild_db["ch_xp"]:

            return

        if len(message.content) < 10:

            return

        calc = int(len(message.content) / 5)

        if calc > 40:

            local_earn_xp = 40

            if user_db["xp_boost"] > 0:

                global_earn_xp = 40 * 2

            else:

                global_earn_xp = 40

        else:

            local_earn_xp = calc

            if user_db["xp_boost"] > 0:

                global_earn_xp = calc * 2

            else:

                global_earn_xp = calc

        user_level_guild_db = await database.level_guild(message)

        cluster_guilds_xp.update_one(
            {
                "guild": message.guild.id,
                "user": message.author.id
            },
            {"$inc": {"xp": local_earn_xp}}
        )

        cluster_users.update_one(
            {
                "id": message.author.id
            },
            {"$inc": {"xp": global_earn_xp}}
        )

def setup(client):
    client.add_cog(LevelSystem(client))