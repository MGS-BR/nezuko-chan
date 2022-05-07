import disnake

from easy_pil import Editor, load_image_async
from disnake.ext import commands

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

class Image(commands.Cog):
    """Comandos de imagens"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def memes(self, ctx):
        pass

    @memes.sub_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user to make the montage",
                type = disnake.OptionType.user,
                required = False
            ),
            disnake.Option(
                name = "image",
                description = "image to make the montage",
                type = disnake.OptionType.attachment,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bolsonaro(self, ctx, user: disnake.User = None, image: disnake.Attachment = None):

        """
        [Image] Bolsonaro montage
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

            if user:

                bolsonaro = Editor("./cogs/images/custom/bolsonaro.png")
                asset = await load_image_async(str(user.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((450, 240))
                bolsonaro.paste(pfp, (429, 41))

                file = disnake.File(fp=bolsonaro.image_bytes, filename="bolsonaro_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if image:

                bolsonaro = Editor("./cogs/images/custom/bolsonaro.png")
                asset = await load_image_async(str(image.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((450, 240))
                bolsonaro.paste(pfp, (429, 41))

                file = disnake.File(fp=bolsonaro.image_bytes, filename="bolsonaro_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if not user and not image:

                bolsonaro = Editor("./cogs/images/custom/bolsonaro.png")
                asset = await load_image_async(str(ctx.author.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((450, 240))
                bolsonaro.paste(pfp, (429, 41))

                file = disnake.File(fp=bolsonaro.image_bytes, filename="bolsonaro_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

        except:

            await ctx.edit_original_message(
                embed = disnake.Embed(description="<:x_:956703878395625472> Error", color = disnake.Color.red())
            )

    @memes.sub_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user to make the montage",
                type = disnake.OptionType.user,
                required = False
            ),
            disnake.Option(
                name = "image",
                description = "image to make the montage",
                type = disnake.OptionType.attachment,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def perfeito(self, ctx, user: disnake.User = None, image: disnake.Attachment = None):

        """
        [Image] Perfeito montage
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

            if user:

                perfeito = Editor("./cogs/images/custom/perfeito.jpg")
                asset = await load_image_async(str(user.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((258, 236))
                perfeito.paste(pfp, (222, 82))

                file = disnake.File(fp=perfeito.image_bytes, filename="perfeito_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if image:

                perfeito = Editor("./cogs/images/custom/perfeito.jpg")
                asset = await load_image_async(str(image.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((258, 236))
                perfeito.paste(pfp, (222, 82))

                file = disnake.File(fp=perfeito.image_bytes, filename="perfeito_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if not user and not image:

                perfeito = Editor("./cogs/images/custom/perfeito.jpg")
                asset = await load_image_async(str(ctx.author.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((258, 236))
                perfeito.paste(pfp, (222, 82))

                file = disnake.File(fp=perfeito.image_bytes, filename="perfeito_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

        except:

            await ctx.edit_original_message(
                embed = disnake.Embed(description="<:x_:956703878395625472> Error", color = disnake.Color.red())
            )

    @memes.sub_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user to make the montage",
                type = disnake.OptionType.user,
                required = False
            ),
            disnake.Option(
                name = "image",
                description = "image to make the montage",
                type = disnake.OptionType.attachment,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def morrepraga(self, ctx, user: disnake.User = None, image: disnake.Attachment = None):

        """
        [Image] Morre praga montage
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

            if user:

                praga = Editor("./cogs/images/custom/praga.png")
                asset = await load_image_async(str(user.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((188, 166))
                praga.paste(pfp, (78, 137))

                file = disnake.File(fp=praga.image_bytes, filename="praga_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if image:

                praga = Editor("./cogs/images/custom/praga.png")
                asset = await load_image_async(str(image.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((188, 166))
                praga.paste(pfp, (78, 137))

                file = disnake.File(fp=praga.image_bytes, filename="praga_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if not user and not image:

                praga = Editor("./cogs/images/custom/praga.png")
                asset = await load_image_async(str(ctx.author.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((188, 166))
                praga.paste(pfp, (78, 137))

                file = disnake.File(fp=praga.image_bytes, filename="praga_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

        except:

            await ctx.edit_original_message(
                embed = disnake.Embed(description="<:x_:956703878395625472> Error", color = disnake.Color.red())
            )

    @memes.sub_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user to make the montage",
                type = disnake.OptionType.user,
                required = False
            ),
            disnake.Option(
                name = "image",
                description = "image to make the montage",
                type = disnake.OptionType.attachment,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rip(self, ctx, user: disnake.User = None, image: disnake.Attachment = None):

        """
        [Image] Rip montage
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

            if user:

                rip = Editor("./cogs/images/custom/rip.jpg")
                asset = await load_image_async(str(user.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((135, 110))
                rip.paste(pfp, (161, 301))

                file = disnake.File(fp=rip.image_bytes, filename="rip_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if image:

                rip = Editor("./cogs/images/custom/rip.jpg")
                asset = await load_image_async(str(image.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((135, 110))
                rip.paste(pfp, (161, 301))

                file = disnake.File(fp=rip.image_bytes, filename="rip_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if not user and not image:

                rip = Editor("./cogs/images/custom/rip.jpg")
                asset = await load_image_async(str(ctx.author.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((135, 110))
                rip.paste(pfp, (161, 301))

                file = disnake.File(fp=rip.image_bytes, filename="rip_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

        except:

            await ctx.edit_original_message(
                embed = disnake.Embed(description="<:x_:956703878395625472> Error", color = disnake.Color.red())
            )

    @memes.sub_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user to make the montage",
                type = disnake.OptionType.user,
                required = False
            ),
            disnake.Option(
                name = "image",
                description = "image to make the montage",
                type = disnake.OptionType.attachment,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wanted(self, ctx, user: disnake.User = None, image: disnake.Attachment = None):

        """
        [Image] Wanted montage
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

            if user:

                wanted = Editor("./cogs/images/custom/wanted.jpg")
                asset = await load_image_async(str(user.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((410, 318))
                wanted.paste(pfp, (23, 208))

                file = disnake.File(fp=wanted.image_bytes, filename="wanted_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if image:

                wanted = Editor("./cogs/images/custom/wanted.jpg")
                asset = await load_image_async(str(image.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((410, 318))
                wanted.paste(pfp, (23, 208))

                file = disnake.File(fp=wanted.image_bytes, filename="wanted_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

            if not user and not image:

                wanted = Editor("./cogs/images/custom/wanted.jpg")
                asset = await load_image_async(str(ctx.author.avatar.url))
                data = Editor(asset)

                pfp = Editor(data)
                pfp = pfp.resize((410, 318))
                wanted.paste(pfp, (23, 208))

                file = disnake.File(fp=wanted.image_bytes, filename="wanted_discord.png")

                return await ctx.edit_original_message(embed=None, file=file)

        except:

            await ctx.edit_original_message(
                embed = disnake.Embed(description="<:x_:956703878395625472> Error", color = disnake.Color.red())
            )

def setup(client):
    client.add_cog(Image(client))