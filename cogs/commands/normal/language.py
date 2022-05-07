import disnake
import json

from pymongo import MongoClient
from disnake.ext import commands

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

cluster = MongoClient(connection_url)
cluster_guilds = cluster["discord"]["guilds"]

class Button(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.choice = None

    @disnake.ui.button(
        label = "English US",
        emoji = "🇺🇸",
        style = disnake.ButtonStyle.green
    )
    async def enus(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        self.choice = "enus"

        cluster_guilds.update_one({"id": ctx.guild.id}, {"$set":{"language": "english"}})

        embed = disnake.Embed(
            description = "🇺🇸 You changed the server language! (EN)",
            color = disnake.Color.green()
        )

        await ctx.message.edit(embed=embed, view=None)

        self.stop


    @disnake.ui.button(
        label = "Português BR",
        emoji = "🇧🇷",
        style = disnake.ButtonStyle.green
    )
    async def ptbr(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        self.choice = "ptbr"

        cluster_guilds.update_one({"id": ctx.guild.id}, {"$set":{"language": "portugues"}})

        embed = disnake.Embed(
            description = "🇧🇷 Você alterou o idioma do servidor (PTBR)!",
            color = disnake.Color.green()
        )

        await ctx.message.edit(embed=embed, view=None)

        self.stop

class Language(commands.Cog):
    """Comandos de idioma"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def language(self, ctx):

        pass

    @language.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def change(self, ctx):

        """
        [Language] Change bot language
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        embed = disnake.Embed(title=ctx.guild.name)

        embed.add_field(name = "🇺🇸 English(USA)", value = "React to change the language to English!")
        embed.add_field(name = "🇧🇷 Português(BR)", value = "Reaja para alterar o idioma para Português!")

        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.color = disnake.Color.blue()

        button = Button()

        await ctx.send(embed=embed, view=button)

        await button.wait()

    @language.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def info(self, ctx):

        """
        [Language] See the current bot language on the server
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            embed = disnake.Embed(
                description = "O idioma atual do servidor é ptbr 🇧🇷",
                color = disnake.Color.green()
            )

            await ctx.send(embed=embed)

        else:

            embed = disnake.Embed(
                description = "The current server language is english us 🇺🇸",
                color = disnake.Color.green()
            )

            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Language(client))