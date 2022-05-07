import disnake

from disnake.ext import commands

from cogs.utilities.databaseUsage import database

class GeneralErrors(commands.Cog):
    """General errors"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):

        print(error)

        error = getattr(error, "original", error)

        guild_db = await database.guild(ctx)

        if isinstance(error, commands.MemberNotFound) or isinstance(error, commands.UserNotFound):

            if guild_db["language"] == "portugues":

                await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> Não foi possível encontrar o usuário especificado!",
                        color = disnake.Color.red()
                    )
                )

            else:

                await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> The specified user could not be found!",
                        color = disnake.Color.red()
                    )
                )

        if isinstance(error, commands.GuildNotFound):

            if guild_db["language"] == "portugues":

                await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> Não foi possível encontrar o servidor especificado!",
                        color = disnake.Color.red()
                    )
                )

            else:

                await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> The specified server could not be found!",
                        color = disnake.Color.red()
                    )
                )       

def setup(client):
    client.add_cog(GeneralErrors(client))