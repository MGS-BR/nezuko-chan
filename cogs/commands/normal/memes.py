import disnake
import random
import praw

from disnake.ext import commands

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

class Memes(commands.Cog):
    """Comandos de memes"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def meme(self, ctx):

        """
        [Memes] Reddit memes
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        reddit = praw.Reddit(client_id="NJnCWhO95LeRLA",
                            client_secret="MkrthHwHMHED-yYwfMsjybhbVCnxzQ",
                            user_agent="NezukoBOT",
                            check_for_async=False)

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            pesquisa = "MemesBR", "DiretoDoZapZap", "HUEstation", "MemesBrasil", "memes_br"

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processando o comando...", color = disnake.Color.green())
            )

        else:

            pesquisa = "memes", "dankmemes", "funny"

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processing the command...", color = disnake.Color.green())
            )

        pesquisar = random.choice(pesquisa)

        memes_submission = reddit.subreddit(pesquisar).hot()

        post_to_pick = random.randint(1, 100)

        while True:

            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submission if not x.stickied)
                name = submission.title

            if submission.url.endswith(".png") or submission.url.endswith(".jpg") or submission.url.endswith(".jpeg"):
                break

        embed = disnake.Embed(
            description=f"**[{name}]({submission.url})**",
            color = disnake.Color.gold()
            )

        embed.set_footer(text=ctx.author)
        embed.set_image(url=submission.url)

        await ctx.edit_original_message(embed=embed)

def setup(client):
    client.add_cog(Memes(client))