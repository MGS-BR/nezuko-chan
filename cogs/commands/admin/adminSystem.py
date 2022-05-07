import disnake
import json
import datetime

from pymongo import MongoClient
from disnake.ext import commands

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

cluster = MongoClient(connection_url)
cluster_languages = cluster["discord"]["idioma"]

class Admin(commands.Cog):
    """Comandos de admin"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "channel",
                description = "chat that will be locked",
                type = disnake.OptionType.channel,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: disnake.TextChannel = None):

        """
        [Admin] Lock the chat to prevent everyone from talking
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if not channel:

            channel = ctx.channel

        channel_permissions = channel.overwrites_for(ctx.guild.default_role)

        await channel.set_permissions(
            ctx.guild.default_role,
            read_messages = channel_permissions.read_messages,
            send_messages = False
            )
        
        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(
                    description = f"O chat {channel.mention} foi trancado com sucesso!",
                    color = disnake.Color.green()
                )
            )

        else:

            await ctx.send(
                embed = disnake.Embed(
                    description = f"Chat {channel.mention} has been successfully locked!",
                    color = disnake.Color.green()
                )
            )

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "channel",
                description = "chat that will be unlocked",
                type = disnake.OptionType.channel,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: disnake.TextChannel = None):

        """
        [Admin] Unlock chat and make everyone able to talk again
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if not channel:

            channel = ctx.channel

        channel_permissions = channel.overwrites_for(ctx.guild.default_role)

        await channel.set_permissions(
            ctx.guild.default_role,
            read_messages = channel_permissions.read_messages,
            send_messages = True
            )
        
        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(
                    description = f"O chat {channel.mention} foi destrancado com sucesso!",
                    color = disnake.Color.green()
                )
            )

        else:

            await ctx.send(
                embed = disnake.Embed(
                    description = f"Chat {channel.mention} has been successfully unlocked!",
                    color = disnake.Color.green()
                )
            )

    @commands.slash_command()
    async def lockdown(self, ctx):
        pass

    @lockdown.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True) 
    async def start(self, ctx):

        """
        [Admin] Start a server lockdown preventing everyone from talking in all chats
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
    
        for channel in ctx.guild.text_channels:

            channel_permissions = channel.overwrites_for(ctx.guild.default_role)

            await channel.set_permissions(
                ctx.guild.default_role,
                read_messages = channel_permissions.read_messages,
                send_messages = False
                )

        if guild_db["language"] == "portugues":

            await ctx.edit_original_message(
                embed = disnake.Embed(
                    description = "Lockdown executado com sucesso!",
                    color = disnake.Color.green()
                )
            )

        else:

            await ctx.edit_original_message(
                embed = disnake.Embed(
                    description = "Lockdown successfully executed!",
                    color = disnake.Color.green()
                )
            )

    @lockdown.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def end(self, ctx):

        """
        [Admin] End the lockdown and make everyone speak in all chats again
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
    
        for channel in ctx.guild.text_channels:

            channel_permissions = channel.overwrites_for(ctx.guild.default_role)

            await channel.set_permissions(
                ctx.guild.default_role,
                read_messages = channel_permissions.read_messages,
                send_messages = True
                )

        if guild_db["language"] == "portugues":

            await ctx.edit_original_message(
                embed = disnake.Embed(
                    description = "Lockdown encerrado com sucesso!",
                    color = disnake.Color.green()
                )
            )

        else:

            await ctx.edit_original_message(
                embed = disnake.Embed(
                    description = "Lockdown ended successfully!",
                    color = disnake.Color.green()
                )
            )

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "amount",
                description = "number of messages to be deleted",
                type = disnake.OptionType.integer,
                required = True
            ),
            disnake.Option(
                name = "user",
                description = "user who will have the messages deleted",
                type = disnake.OptionType.user,
                required = False
            ),
            disnake.Option(
                name = "message",
                description = "only messages equal to the defined ones will be deleted",
                type = disnake.OptionType.string,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int, user: disnake.User = None, message: str = None):

        """
        [Admin] Delete chat messages
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

        if amount > 300:

            if guild_db["language"] == "portugues":

                return await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> Vai com calma aí! Eu só posso limpar até `300` mensagens, por favor digite um valor menor!",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> Oops, calm down there! I can only clear up to `300` messages, please enter a lower value!",
                        color = disnake.Color.red()
                    )
                )        

        else:

            if not user and not message:

                deleted = await ctx.channel.purge(limit=amount, after=datetime.datetime.utcnow()-datetime.timedelta(days=16))

            else:

                if user and message:

                    def check(message_deleted):
                        return message_deleted.author == user and message_deleted.content == message    

                elif not user:

                    def check(message_deleted):
                        return message_deleted.content == message

                elif not message:

                    def check(message_deleted):
                        return message_deleted.author == user

                deleted = await ctx.channel.purge(limit=amount, after=datetime.datetime.utcnow()-datetime.timedelta(days=16), check=check)

            if guild_db["language"] == "portugues":

                await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description = f"*{len(deleted):,}* mensagens foram apagadas por {ctx.author.mention}",
                        color = disnake.Color.green()
                    )
                )

            else:

                await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description = f"*{len(deleted):,}* messages were deleted by {ctx.author.mention}",
                        color = disnake.Color.green()
                    )
                )

def setup(client):
    client.add_cog(Admin(client))