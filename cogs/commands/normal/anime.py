import disnake
import datetime
import animec

from disnake.ext import commands

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

class Anime(commands.Cog):
    """Comandos de animes"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def anime(self, ctx):

        pass

    @anime.sub_command(
        options = [
            disnake.Option(
                name = "anime",
                description = "anime you want to search",
                type = disnake.OptionType.string,
                required = True
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def search(self, ctx, anime):

        """
        [Anime] Search for an anime
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processando o comando...", color = disnake.Color.green())
            )

        else:

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processing the command...", color = disnake.Color.green())
            )

        try:
            anime = animec.Anime(anime)

            embed = disnake.Embed(
                description = f"**[{anime.name}]({anime.url})**\n{anime.description[:1000]}...",
                color = disnake.Color.blue()
            )

            embed.add_field(name="Episodes", value=anime.episodes)
            embed.add_field(name="Type", value=anime.type)

            if anime.genres:
                embed.add_field(name="Genres", value=f", ".join(anime.genres))

            embed.add_field(name="Anime rank", value=anime.ranked)
            embed.add_field(name="Anime popularity", value=anime.popularity)
            embed.add_field(name="Status", value=anime.status)
            embed.add_field(name="Anime rating", value=anime.rating)
            embed.add_field(name="Anime broadcast", value=anime.broadcast)
            embed.add_field(name="Anime teaser", value=f"Click [here]({anime.teaser}) to watch")

            embed.set_thumbnail(url=anime.poster)

            await ctx.edit_original_message(embed=embed)

        except:

            if guild_db["language"] == "portugues":

                return await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description="<:x_:956703878395625472> Não foi possível achar nada correspondente a sua busca!",
                        color = disnake.Color.red()
                    )
                )

            else:
                
                return await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description="<:x_:956703878395625472> Couldn't find anything matching your search!",
                        color = disnake.Color.red()
                    )
                )

    @anime.sub_command(
        options = [
            disnake.Option(
                name = "search",
                description = "character you want to search",
                type = disnake.OptionType.string,
                required = True
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def character(self, ctx, search):

        """
        [Anime] Search for a anime character
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processando o comando...", color = disnake.Color.green())
            )

        else:

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processing the command...", color = disnake.Color.green())
            )

        try:
            char = animec.Charsearch(search)

            embed = disnake.Embed(
                title= char.title,
                url = char.url,
                color = disnake.Color.green(),
                description=",\n".join(list(char.references.keys())[:2])
            )

            embed.set_image(url=char.image_url)

            await ctx.edit_original_message(embed=embed)

        except:

            if guild_db["language"] == "portugues":

                return await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description="<:x_:956703878395625472> Não foi possível achar nada correspondente a sua busca!",
                        color = disnake.Color.red()
                    )
                )

            else:
                
                return await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description="<:x_:956703878395625472> Couldn't find anything matching your search!",
                        color = disnake.Color.red()
                    )
                )

    @anime.sub_command(
        options = [
            disnake.Option(
                name = "amount",
                description = "amount of news you want to see",
                type = disnake.OptionType.integer,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def news(self, ctx, amount=3):

        """
        [Anime] See anime news
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processando o comando...", color = disnake.Color.green())
            )

        else:

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processing the command...", color = disnake.Color.green())
            )

        news = animec.Aninews(amount)
        links = news.links
        titles = news.titles
        descriptions = news.description

        embed = disnake.Embed(
            title="Animes News",
            color = disnake.Color.gold(),
            timestamp = datetime.datetime.utcnow()
        )

        embed.set_thumbnail(url=news.images[0])

        for i in range(amount):

            embed.add_field(name=f"{i+1} {titles[i]}", value=f"{descriptions[i][:300]}...\n[Read more]({links[i]})", inline=False)

        await ctx.edit_original_message(embed=embed)

    @anime.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def waifu(self, ctx):

        """
        [Anime] See the image of a random waifu
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        waifu  = animec.waifu.Waifu.random()

        embed = disnake.Embed(
            color = disnake.Color.magenta()
        )

        embed.set_image(url=waifu)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Anime(client))