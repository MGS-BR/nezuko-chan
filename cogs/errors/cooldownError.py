import disnake
import json

from pymongo import MongoClient
from disnake.ext import commands

from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

class CooldownError(commands.Cog):
    """Cooldown error"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):

        error = getattr(error, "original", error)

        print(error)

        if isinstance(error, commands.CommandOnCooldown):

            guild_db = await database.guild(ctx)

            if guild_db["language"] == "portugues":

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Aguarde **{error.retry_after:.1f}s** para usar o comando novamente.",
                        color = disnake.Color.red()
                    ),
                    ephemeral = True
                )

            else:

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Wait **{error.retry_after:.1f}s** to use the command again.",
                        color = disnake.Color.red()
                    ),
                    ephemeral = True
                )

def setup(client):
    client.add_cog(CooldownError(client))