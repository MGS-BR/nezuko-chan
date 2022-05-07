import disnake
import json
import datetime
import calendar

from pymongo import MongoClient
from disnake.ext import commands

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

cluster = MongoClient(connection_url)
cluster_ban_time_db = cluster["discord"]["guilds_bans"]

def convert(time):

    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    try:
        int(time[:-1])
    except:
        return -1

    if unit not in pos:
        return -2

    calc = int(time[:-1]) * time_dict[unit]

    if calc < 60:
        return -3

    else:
        return calc

class BanButton(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.author = None

        self.user = None

        self.reason = None

    @disnake.ui.button(
        emoji = "<:success:956703878412394546>",
        style = disnake.ButtonStyle.green
    )
    async def ban_accept(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        if ctx.user == self.author:

            guild_db = await database.guild(ctx)

            if any(word in self.reason.lower() for word in ["spam", "span", "scam", "scan"]):

                await ctx.guild.ban(self.user, reason=self.reason, delete_messages_days=7)

            else:

                await ctx.guild.ban(self.user, reason=self.reason)

            if guild_db["language"] == "portugues":

                guild_embed = disnake.Embed(
                    title = "Usuário banido 🚫",
                    description = f"Usuário Banido: {self.user.name}\nTempo de banimento: Permanente\nMotivo do banimento: {self.reason}\nAutor do banimento: {ctx.author}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.red()
                    )

                guild_embed.set_footer(text = f"User id: {self.user.id} \u200b")

                user_embed = disnake.Embed(
                    title = "Banido",
                    description = f"Você foi banido do servidor: {ctx.guild}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.red()
                    )

                user_embed.add_field(name="Autor do banimento:", value=ctx.author, inline=False)
                user_embed.add_field(name="Motivo:", value=self.reason, inline=False)
                user_embed.add_field(name="Tempo de banimento:", value="Permanente", inline=False)

                user_embed.set_thumbnail(url=ctx.guild.icon.url)

                user_embed.set_footer(text=f"\u200b")

            else:

                guild_embed = disnake.Embed(
                    title = "User banned 🚫",
                    description = f"User banned: {self.user.name}\nBan time: Permanent\nReason for banishment: {self.reason}\nBanisher: {ctx.author}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.red()
                    )

                guild_embed.set_footer(text = f"User id: {self.user.id} \u200b")

                user_embed = disnake.Embed(
                    title = "Banned",
                    description = f"You got banned from: {ctx.guild}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.red()
                    )

                user_embed.add_field(name="Banisher:", value=ctx.author, inline=False)
                user_embed.add_field(name="Reason:", value=self.reason, inline=False)
                user_embed.add_field(name="Ban time:", value="Permanent", inline=False)

                user_embed.set_thumbnail(url=ctx.guild.icon.url)

                user_embed.set_footer(text=f"\u200b")

            await ctx.message.edit(embed=guild_embed, view=None)

            try:

                channel = await self.user.create_dm()

                await channel.send(embed=user_embed)

            except:

                pass   

            try:

                cluster_ban_time_db.find_one_and_delete({"id": ctx.guild.id, "user": self.user.id})

            except:

                pass

            self.stop

    @disnake.ui.button(
        emoji = "<:x_:956703878395625472>",
        style = disnake.ButtonStyle.red
    )
    async def ban_deny(self, button: disnake.Button, ctx: disnake.MessageInteraction):

        if ctx.user == self.author:

            guild_db = await database.guild(ctx)

            if guild_db["language"] == "portugues":

                await ctx.message.edit(
                    embed = disnake.Embed(
                        description = "Banimento cancelado!",
                        color = disnake.Color.red()
                    ),
                    view = None
                )

            else:

                await ctx.message.edit(
                    embed = disnake.Embed(
                        description = "Ban canceled!",
                        color = disnake.Color.red()
                    ),
                    view = None
                )

            self.stop

class Ban(commands.Cog):
    """Comandos de banimento"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user to be banned",
                type = disnake.OptionType.user,
                required = True
            ),
            disnake.Option(
                name = "time",
                description = "ban time (ex: 4d) (s|m|h|d)",
                type = disnake.OptionType.string,
                required = False
            ),
            disnake.Option(
                name = "reason",
                description = "reason for banishment",
                type = disnake.OptionType.string,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: disnake.User, time = None, reason = None):

        """
        [Admin] Ban someone from the server
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

        button = BanButton()

        if not reason:

            if guild_db["language"] == "portugues":

                reason = "Sem motivo especificado"

            else:

                reason = "No reason specified"

        if not time:

            button.author = ctx.author
            button.user = user
            button.reason = reason

            if guild_db["language"] == "portugues":

                await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description=f"Você gostaria de banir o usuário `{user}` permanentemente?",
                        color = disnake.Color.red()
                    ),
                    view = button
                )

            else:

                await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description=f"Would you like to ban user `{user}` permanently?",
                        color = disnake.Color.red()
                    ),
                    view = button
                )

        else:

            time = convert(time)

            if time == -3:

                if guild_db["language"] == "portugues":

                    return await ctx.edit_original_message(
                        embed = disnake.Embed(
                            description = "<:x_:956703878395625472> O tempo mínimo de banimento é de 1 minuto, por favor insira um valor maior!",
                            color = disnake.Color.red()
                        )
                        )

                else:

                    return await ctx.edit_original_message(
                        embed = disnake.Embed(
                            description = "<:x_:956703878395625472> The minimum ban time is 1 minute, please enter a higher amount!",
                            color = disnake.Color.red()
                        )
                        )

            elif time == -2:

                if guild_db["language"] == "portugues":

                    return await ctx.edit_original_message(
                        embed = disnake.Embed(
                            description = "<:x_:956703878395625472> Por favor insira um valor válido para o tempo do banimento!",
                            color = disnake.Color.red()
                        )
                        )

                else:

                    return await ctx.edit_original_message(
                        embed = disnake.Embed(
                            description = "<:x_:956703878395625472> Please enter a valid ban time value!",
                            color = disnake.Color.red()
                        )
                        )

            elif time == -1:


                if guild_db["language"] == "portugues":

                    return await ctx.edit_original_message(
                        embed = disnake.Embed(
                            description = "<:x_:956703878395625472> Por favor insira um valor válido para o tempo do banimento!",
                            color = disnake.Color.red()
                        )
                        )

                else:

                    return await ctx.edit_original_message(
                        embed = disnake.Embed(
                            description = "<:x_:956703878395625472> Please enter a valid ban time value!",
                            color = disnake.Color.red()
                        )
                        )

            if any(word in reason.lower() for word in ["spam", "span", "scam", "scan"]):

                await ctx.guild.ban(user, reason=reason, delete_messages_days=7)

            else:

                await ctx.guild.ban(user, reason=reason)

            time_now = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)

            time_ban = calendar.timegm(time_now.utctimetuple())

            time_message = f"<t:{time_ban}:f>"

            if guild_db["language"] == "portugues":

                guild_embed = disnake.Embed(
                    title = "Usuário banido 🚫",
                    description = f"Usuário Banido: {user.name}\nTempo de banimento: {time_message}\nMotivo do banimento: {reason}\nAutor do banimento: {ctx.author}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.red()
                    )

                guild_embed.set_footer(text = f"User id: {user.id} \u200b")

                user_embed = disnake.Embed(
                    title = "Banido",
                    description = f"Você foi banido do servidor: {ctx.guild}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.red()
                    )

                user_embed.add_field(name="Autor do banimento:", value=ctx.author, inline=False)
                user_embed.add_field(name="Motivo:", value=reason, inline=False)
                user_embed.add_field(name="Tempo de banimento:", value=f"Acaba em {time_message}", inline=False)

                user_embed.set_thumbnail(url=ctx.guild.icon.url)

                user_embed.set_footer(text=f"\u200b")

                ban_user_db = cluster_ban_time_db.find_one({"id": ctx.guild.id, "user": user.id})

                if not ban_user_db:

                    cluster_ban_time_db.insert_one({"id": ctx.guild.id, "user": user.id, "tempo": time_ban})
                    
                else:

                    cluster_ban_time_db.update_one({"id":ctx.guild.id, "user":user.id}, {"$set":{"tempo": time_ban}})

                    guild_embed.add_field(name="Observações:", value="O usuário já possuia um banimento temporário, porém agora o tempo de banimento foi alterado para o novo banimento afetuado!", inline=False)

                    user_embed.add_field(name="Observações:", value="Você já possuia um banimento temporário, porém agora o tempo de banimento foi alterado para o novo banimento efetuado!", inline=False)

            else:

                guild_embed = disnake.Embed(
                    title = "User banned 🚫",
                    description = f"User banned: {user.name}\nBan time: {time_message}\nReason for banishment: {reason}\nBanisher: {ctx.author}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.red()
                    )

                guild_embed.set_footer(text = f"User id: {user.id} \u200b")

                user_embed = disnake.Embed(
                    title = "Banned",
                    description = f"You got banned from: {ctx.guild}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.red()
                    )

                user_embed.add_field(name="Banisher:", value=ctx.author, inline=False)
                user_embed.add_field(name="Reason:", value=reason, inline=False)
                user_embed.add_field(name="Ban time:", value=f"The ban ends in {time_message}", inline=False)

                user_embed.set_thumbnail(url=ctx.guild.icon.url)

                user_embed.set_footer(text=f"\u200b")

                ban_user_db = cluster_ban_time_db.find_one({"id": ctx.guild.id, "user": user.id})

                if not ban_user_db:

                    cluster_ban_time_db.insert_one({"id": ctx.guild.id, "user": user.id, "tempo": time_ban})
                    
                else:

                    cluster_ban_time_db.update_one({"id":ctx.guild.id, "user":user.id}, {"$set":{"tempo": time_ban}})

                    guild_embed.add_field(name="Comments:", value="The user already has a temporary ban, but now the ban time has been changed to the new affected ban!", inline=False)

                    user_embed.add_field(name="Comments:", value="You already have a temporary ban, but now the ban time has been changed to the new affected ban!", inline=False)

            await ctx.edit_original_message(embed=guild_embed)

            try:

                channel = await user.create_dm()

                await channel.send(embed=user_embed)

            except:

                pass   

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user to be unbanned",
                type = disnake.OptionType.user,
                required = True
            ),
            disnake.Option(
                name = "reason",
                description = "reason for unban",
                type = disnake.OptionType.string,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: disnake.User, reason = None):

        """
        [Admin] Unban someone from the server
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if not reason:

            if guild_db["language"] == "portugues":

                reason = "Sem motivo especificado"

            else:

                reason = "No reason specified"

        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processando o comando...", color = disnake.Color.green())
            )

        else:

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processing the command...", color = disnake.Color.green())
            )

        guild_bans = await ctx.guild.bans()

        def check_ban(user):

            ban_list = []

            for ban in guild_bans:

                ban_list.append(ban.user.id)

            if user.id in ban_list:

                return True

            else:
                return False

        if check_ban(user) == False:

            try:

                cluster_ban_time_db.find_one_and_delete({"id": ctx.guild.id, "user": user.id})

            except:

                pass

            if guild_db["language"] == "portugues":

                return await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> O usuário não está banido do servidor!",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.edit_original_message(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> The user is not banned from the server!",
                        color = disnake.Color.red()
                    )
                )

        else:

            await ctx.guild.unban(user=user, reason=reason)

            if guild_db["language"] == "portugues":

                guild_embed = disnake.Embed(
                    title = "Usuário Desbanido ❕",
                    description = f"Usuário desbanido: {user}\nMotivo do desbanimento: {reason}\nAutor do desbanimento: {ctx.author}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.green()
                )

                guild_embed.set_footer(text=f"User id: {user.id} \u200b")

                user_embed = disnake.Embed(
                    title = "Desbanido",
                    description = f"Você foi desbanido do servidor: {ctx.guild}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.green()
                    )

                user_embed.add_field(name="Autor do desbanimento:", value=ctx.author, inline=False)
                user_embed.add_field(name="Motivo:", value=reason, inline=False)

                user_embed.set_thumbnail(url=ctx.guild.icon.url)

                user_embed.set_footer(text=f"\u200b")

            else:

                guild_embed = disnake.Embed(
                    title = "Unbanned user ❕",
                    description = f"Unbanned user: {user}\nReason for unban: {reason}\nAuthor of unban: {ctx.author}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.green()
                )

                guild_embed.set_footer(text=f"User id: {user.id} \u200b")

                user_embed = disnake.Embed(
                    title = "Unbanned",
                    description = f"You got unbanned from server: {ctx.guild}",
                    timestamp = datetime.datetime.utcnow(),
                    color = disnake.Color.green()
                    )

                user_embed.add_field(name="Author of unban:", value=ctx.author, inline=False)
                user_embed.add_field(name="Reason:", value=reason, inline=False)

                user_embed.set_thumbnail(url=ctx.guild.icon.url)

                user_embed.set_footer(text=f"\u200b")

            await ctx.edit_original_message(embed=guild_embed)

            try:

                channel = await user.create_dm()

                await channel.send(embed=user_embed)

            except:

                pass  

            try:

                cluster_ban_time_db.find_one_and_delete({"id": ctx.guild.id, "user": user.id})

            except:

                pass

def setup(client):
    client.add_cog(Ban(client))