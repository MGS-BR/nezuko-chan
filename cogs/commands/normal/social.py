import disnake
import animec

from disnake.ext import commands

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

class HugButton(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.user = None

    @disnake.ui.button(
        emoji = "🔄",
        style = disnake.ButtonStyle.green
    )
    async def hug(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        if ctx.user == self.user:

            guild_db = await database.guild(ctx)

            if guild_db["language"] == "portugues":

                text = f"**{self.user.mention} abraçou {ctx.author.mention}!**"
            
            else:

                text = f"**{self.user.mention} hugged {ctx.author.mention}!**"

            embed = disnake.Embed(
                description = text,
                color = disnake.Color.purple()
            )

            embed.set_image(animec.waifu.Waifu.hug())

            await ctx.send(embed=embed)

            await ctx.message.edit(view=None)

            self.stop

class KissButton(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.user = None

    @disnake.ui.button(
        emoji = "🔄",
        style = disnake.ButtonStyle.green
    )
    async def kiss(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        if ctx.user == self.user:

            guild_db = await database.guild(ctx)

            if guild_db["language"] == "portugues":

                text = f"**{self.user.mention} beijou {ctx.author.mention}!**"
            
            else:

                text = f"**{self.user.mention} kissed {ctx.author.mention}!**"

            embed = disnake.Embed(
                description = text,
                color = disnake.Color.magenta()
            )

            embed.set_image(animec.waifu.Waifu.kiss())

            await ctx.send(embed=embed)

            await ctx.message.edit(view=None)

            self.stop

class SlapButton(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.user = None

    @disnake.ui.button(
        emoji = "🔄",
        style = disnake.ButtonStyle.green
    )
    async def slap(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        if ctx.user == self.user:

            guild_db = await database.guild(ctx)

            if guild_db["language"] == "portugues":

                text = f"**{self.user.mention} de um tapa em {ctx.author.mention}!**"
            
            else:

                text = f"**{self.user.mention} slapped {ctx.author.mention}!**"

            embed = disnake.Embed(
                description = text,
                color = disnake.Color.red()
            )

            embed.set_image(animec.waifu.Waifu.slap())

            await ctx.send(embed=embed)

            await ctx.message.edit(view=None)

            self.stop

class AttackButton(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.user = None

    @disnake.ui.button(
        emoji = "🔄",
        style = disnake.ButtonStyle.green
    )
    async def attack(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        if ctx.user == self.user:

            guild_db = await database.guild(ctx)

            if guild_db["language"] == "portugues":

                text = f"**{self.user.mention} atacou {ctx.author.mention}!**"
            
            else:

                text = f"**{self.user.mention} attacked {ctx.author.mention}!**"

            embed = disnake.Embed(
                description = text,
                color = disnake.Color.red()
            )

            embed.set_image(animec.waifu.Waifu.kick())

            await ctx.send(embed=embed)

            await ctx.message.edit(view=None)

            self.stop

class DanceButton(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.user = None

    @disnake.ui.button(
        emoji = "🔄",
        style = disnake.ButtonStyle.green
    )
    async def dance(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        if ctx.user == self.user:

            guild_db = await database.guild(ctx)

            if guild_db["language"] == "portugues":

                text = f"**{self.user.mention} dançou com {ctx.author.mention}!**"
            
            else:

                text = f"**{self.user.mention} danced with {ctx.author.mention}!**"

            embed = disnake.Embed(
                description = text,
                color = disnake.Color.gold()
            )

            embed.set_image(animec.waifu.Waifu.dance())

            await ctx.send(embed=embed)

            await ctx.message.edit(view=None)

            self.stop

class PatButton(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.user = None

    @disnake.ui.button(
        emoji = "🔄",
        style = disnake.ButtonStyle.green
    )
    async def pat(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        if ctx.user == self.user:

            guild_db = await database.guild(ctx)

            if guild_db["language"] == "portugues":

                text = f"**{self.user.mention} fez um cafuné em {ctx.author.mention}!**"
            
            else:

                text = f"**{self.user.mention} stroked {ctx.author.mention}!**"

            embed = disnake.Embed(
                description = text,
                color = disnake.Color.blue()
            )

            embed.set_image(animec.waifu.Waifu.pat())

            await ctx.send(embed=embed)

            await ctx.message.edit(view=None)

            self.stop

class Social(commands.Cog):
    """Comandos sociais"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "person you want to hug",
                type = disnake.OptionType.user,
                required = True
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hug(self, ctx, user: disnake.Member):

        """
        [Social] Hug someone
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            text = f"**{ctx.author.mention} abraçou {user.mention}!**"
        
        else:

            text = f"**{ctx.author.mention} hugged {user.mention}!**"

        embed = disnake.Embed(
            description = text,
            color = disnake.Color.purple()
        )

        embed.set_image(animec.waifu.Waifu.hug())

        button = HugButton()

        button.user = user

        await ctx.send(embed=embed, view=button)

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "person you want to kiss",
                type = disnake.OptionType.user,
                required = True
            )
        ]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kiss(self, ctx, user: disnake.Member):

        """
        [Social] Kiss someone
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            text = f"**{ctx.author.mention} beijou {user.mention}!**"
        
        else:

            text = f"**{ctx.author.mention} kissed {user.mention}!**"

        embed = disnake.Embed(
            description = text,
            color = disnake.Color.magenta()
        )

        embed.set_image(animec.waifu.Waifu.kiss())

        button = KissButton()

        button.user = user

        await ctx.send(embed=embed, view=button)

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "person you want to slap",
                type = disnake.OptionType.user,
                required = True
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slap(self, ctx, user: disnake.Member):

        """
        [Social] Slap someone
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            text = f"**{ctx.author.mention} deu um tapa em {user.mention}!**"
        
        else:

            text = f"**{ctx.author.mention} slapped {user.mention}!**"

        embed = disnake.Embed(
            description = text,
            color = disnake.Color.red()
        )

        embed.set_image(animec.waifu.Waifu.slap())

        button = SlapButton()

        button.user = user

        await ctx.send(embed=embed, view=button)

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "person you want to attack",
                type = disnake.OptionType.user,
                required = True
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def attack(self, ctx, user: disnake.Member):

        """
        [Social] Attack someone
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            text = f"**{ctx.author.mention} atacou {user.mention}!**"
        
        else:

            text = f"**{ctx.author.mention} attacked {user.mention}!**"

        embed = disnake.Embed(
            description = text,
            color = disnake.Color.red()
        )

        embed.set_image(animec.waifu.Waifu.kick())

        button = AttackButton()

        button.user = user

        await ctx.send(embed=embed, view=button)

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "person you want to dance",
                type = disnake.OptionType.user,
                required = True
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dance(self, ctx, user: disnake.Member):

        """
        [Social] Dance with someone
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            text = f"**{ctx.author.mention} dançou com {user.mention}!**"
        
        else:

            text = f"**{ctx.author.mention} danced with {user.mention}!**"

        embed = disnake.Embed(
            description = text,
            color = disnake.Color.gold()
        )

        embed.set_image(animec.waifu.Waifu.dance())

        button = DanceButton()

        button.user = user

        await ctx.send(embed=embed, view=button)

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "person you want to pat",
                type = disnake.OptionType.user,
                required = True
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pat(self, ctx, user: disnake.Member):

        """
        [Social] Pat someone
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            text = f"**{ctx.author.mention} fez um cafuné em {user.mention}!**"
        
        else:

            text = f"**{ctx.author.mention} stroked {user.mention}!**"

        embed = disnake.Embed(
            description = text,
            color = disnake.Color.blue()
        )

        embed.set_image(animec.waifu.Waifu.pat())

        button = PatButton()

        button.user = user

        await ctx.send(embed=embed, view=button)

def setup(client):
    client.add_cog(Social(client))