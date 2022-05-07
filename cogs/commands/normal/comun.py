import disnake
import datetime
import emoji as _emoji
import calendar
import pytz

from disnake.ext import commands

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

class Button(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.user = None

class Emoji():

    async def convert(self, ctx, argument):

        if _emoji.is_emoji(argument):
            return ["normal", argument]

        try:
            emoji_ = await commands.EmojiConverter().convert(ctx, argument)
            return ["custom", emoji_]

        except commands.EmojiNotFound:
            return "Emoji não encontrado"

class Comun(commands.Cog):
    """Comandos de comuns"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def server(self, ctx):
        
        pass

    @commands.slash_command()
    async def user(self, ctx):

        pass

    @commands.slash_command()
    async def emoji(self, ctx):

        pass

    @commands.slash_command()
    async def bot(self, ctx):

        pass   

    @server.sub_command(
        options = [
            disnake.Option(
                name = "server",
                description = "server you want to see the information",
                required = False
            )
        ]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def info(self, ctx, server: disnake.Guild = None):

        """
        [Discord] View a server's information
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if not server:

            server = ctx.guild

        users = {
            "online": 0,
            "offline": 0,
            "dnd": 0,
            "idle": 0,
            "mobile": 0,
            "streaming": 0
        }

        for user in server.members:

            if isinstance(user.activity, disnake.Streaming):

                users["streaming"] += 1

            elif user.is_on_mobile() == True:

                users["mobile"] += 1

            elif str(user.status) == "idle":

                users['idle'] += 1

            elif str(user.status) == "dnd":

                users['dnd'] += 1

            elif str(user.status) == "offline":
                
                users['offline'] += 1

            elif str(user.status) == "online":

                users['online'] += 1

        embed = disnake.Embed(
            title = f"<:rimuru:906162056120647690> {server.name}",
            color = disnake.Color.blue()
        )

        embed.set_thumbnail(url = server.icon.url)

        if server.description:

            embed.description = server.description

        if server.banner:

            embed.set_image(url = server.banner.url)

        if guild_db["language"] == "portugues":

            translate_verification_level = {
                "none": "Nenhuma",
                "low": "Baixo",
                "medium": "Média",
                "high": "Alta",
                "highest": "Muito alta"
            }

            users_text = f"<:status_online:896767281865031711> {users['online']} **•** <:status_offline:896767281911177247> {users['offline']} **•** <:status_dnd:896767281680506941> {users['dnd']}\n <:status_mobile:898779448667680828> {users['mobile']} **•** <:status_afk:896767281873420299> {users['idle']} **•** <:status_streaming:896767281714040875> {users['streaming']}"

            embed.add_field(
                name = f"🪧 ID do servidor",
                value = f"`{server.id}`",
                inline = True
            )

            embed.add_field(
                name = "👑 Dono",
                value = f"{server.owner}\n`{server.owner_id}`",
                inline = True
            )

            embed.add_field(
                name = f"👥 Membros ({len(server.members)})",
                value = users_text,
                inline = True
            )

            embed.add_field(
                name = f"💬 Canais ({len(server.text_channels) + len(server.voice_channels) + len(server.threads)})",
                value = f"<:channel_text:898784271437803580> **• Texto**: {len(server.text_channels)}\n<:channel_voice:898784271597178920> **• Voz**: {len(server.voice_channels)}\n<:channel_thread:962131453276217364> **• Threads**: {len(server.threads)}",
                inline = True
            )

            if server.premium_subscriber_role:
                premium_role = server.premium_subscriber_role.mention
            else:
                premium_role = "Não definido"

            embed.add_field(
                name = f"💎 Impulsos ({server.premium_subscription_count})",
                value = f"**• Nível**: {server.premium_tier}\n**• Usuários**: {len(server.premium_subscribers)}\n**• Cargo**: {premium_role}",
                inline = True
            )

            embed.add_field(
                name = "🛡️ Verificação",
                value = translate_verification_level[str(server.verification_level)],
                inline = True
            )

            embed.add_field(
                name = f"🏷️ Informações gerais",
                value = f"**• Cargos**: {len(server.roles)}\n**• Emojis**: {len(server.emojis)}/{server.emoji_limit}\n**• Figurinhas**: {len(server.stickers)}/{server.sticker_limit}",
                inline = False
            )

            server_bot = server.get_member(ctx.bot.user.id)

            embed.add_field(
                name = "🗓️ Criado em",
                value = f"<t:{calendar.timegm(server.created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(server.created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                inline = False
            )

            embed.add_field(
                name = "🤖 Entrei no servidor em",
                value = f"<t:{calendar.timegm(server_bot.joined_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(server_bot.joined_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                inline = False
            )

        else:

            translate_verification_level = {
                "none": "None",
                "low": "Low",
                "medium": "Medium",
                "high": "High",
                "highest": "Highest"
            }

            users_text = f"<:status_online:896767281865031711> {users['online']} **•** <:status_offline:896767281911177247> {users['offline']} **•** <:status_dnd:896767281680506941> {users['dnd']}\n <:status_mobile:898779448667680828> {users['mobile']} **•** <:status_afk:896767281873420299> {users['idle']} **•** <:status_streaming:896767281714040875> {users['streaming']}"

            embed.add_field(
                name = f"🪧 Server ID",
                value = f"`{server.id}`",
                inline = True
            )

            embed.add_field(
                name = "👑 Owner",
                value = f"{server.owner}\n`{server.owner_id}`",
                inline = True
            )

            embed.add_field(
                name = f"👥 Members ({len(server.members)})",
                value = users_text,
                inline = True
            )

            embed.add_field(
                name = f"💬 Channels ({len(server.text_channels) + len(server.voice_channels) + len(server.threads)})",
                value = f"<:channel_text:898784271437803580> **• Text**: {len(server.text_channels)}\n<:channel_voice:898784271597178920> **• Voice**: {len(server.voice_channels)}\n<:channel_thread:962131453276217364> **• Threads**: {len(server.threads)}",
                inline = True
            )

            if server.premium_subscriber_role:
                premium_role = server.premium_subscriber_role.mention
            else:
                premium_role = "Undefined"

            embed.add_field(
                name = f"💎 Boosts ({server.premium_subscription_count})",
                value = f"**• Level**: {server.premium_tier}\n**• Users**: {len(server.premium_subscribers)}\n**• Role**: {premium_role}",
                inline = True
            )

            embed.add_field(
                name = "🛡️ Verification",
                value = translate_verification_level[str(server.verification_level)],
                inline = True
            )

            embed.add_field(
                name = f"🏷️ General information",
                value = f"**• Roles**: {len(server.roles)}\n**• Emojis**: {len(server.emojis)}/{server.emoji_limit}\n**• Stickers**: {len(server.stickers)}/{server.sticker_limit}",
                inline = False
            )

            server_bot = server.get_member(ctx.bot.user.id)

            embed.add_field(
                name = "🗓️ Created at",
                value = f"<t:{calendar.timegm(server.created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(server.created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                inline = False
            )

            embed.add_field(
                name = "🤖 I joined the server at",
                value = f"<t:{calendar.timegm(server_bot.joined_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(server_bot.joined_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                inline = False
            )

        await ctx.send(embed=embed)

    @server.sub_command(
        options = [
            disnake.Option(
                name = "server",
                description = "server you want to see icon",
                required = False
            )
        ]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def icon(self, ctx, server: disnake.Guild = None):

        """
        [Discord] See a server icon
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if not server:

            server = ctx.guild

        embed = disnake.Embed(
            title = f"🖼️ {server.name}",
            color = disnake.Color.blue()
        )

        embed.set_image(url = server.icon.url)

        button = Button()

        if guild_db["language"] == "portugues":

            button.add_item(
                disnake.ui.Button(
                    label = "Clique aqui para abrir o ícone no navegador",
                    url = server.icon.url
                )
            )

        else:

            button.add_item(
                disnake.ui.Button(
                    label = "Click here to open the icon in the browser",
                    url = server.icon.url
                )
            )

        await ctx.send(
            embed = embed,
            view = button
        )

    @server.sub_command(
        options = [
            disnake.Option(
                name = "server",
                description = "server you want to see the banner",
                required = False
            )
        ]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def banner(self, ctx, server: disnake.Guild = None):

        """
        [Discord] See a server banner
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if not server:

            server = ctx.guild

        if not server.banner:

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Puts, parece que o servidor não tem um banner!",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Oops, looks like the server doesn't have a banner!",
                        color = disnake.Color.red()
                    )
                )

        else:

            embed = disnake.Embed(
                title = f"🖼️ {server.name}",
                color = disnake.Color.blue()
            )

            embed.set_image(url = server.banner.url)

            button = Button()

            if guild_db["language"] == "portugues":

                button.add_item(
                    disnake.ui.Button(
                        label = "Clique aqui para abrir o banner no navegador",
                        url = server.banner.url
                    )
                )

            else:

                button.add_item(
                    disnake.ui.Button(
                        label = "Click here to open the banner in the browser",
                        url = server.banner.url
                    )
                )

            await ctx.send(
                embed = embed,
                view = button
            )

    @user.sub_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user you want to see the information",
                type = disnake.OptionType.user,
                required = False
            )
        ]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def info(self, ctx, user: disnake.User = None):

        """
        [Discord] View a user's information
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if not user:

            user = ctx.author

        embed = disnake.Embed(
            title = f"<:discord_user:896767281412050966> {user}",
            color = disnake.Color.blue()
        )

        embed.set_thumbnail(url = user.avatar.url)

        user_badges = []

        if ctx.guild.owner == user:
            user_badges.append("<:owner:896767281831485520>")

        if user.bot:
            user_badges.append("<:bot:896767281667903509>")

        if user.public_flags.hypesquad == True:
            user_badges.append("<:hypesquad:896778374662467594>")

        if user.public_flags.hypesquad_bravery == True :
            user_badges.append("<:hypesquad_bravery:896767281646936106>")

        if user.public_flags.hypesquad_brilliance == True:
            user_badges.append("<:hypesquad_brilliance:896767281818918952>")

        if user.public_flags.hypesquad_balance == True:
            user_badges.append("<:hypesquad_balance:896767281894412328>")

        if user.public_flags.early_supporter == True:
            user_badges.append("<:early_supporter:896767281663713301>")

        if user.public_flags.verified_bot_developer == True or user.public_flags.early_verified_bot_developer == True:
            user_badges.append("<:verifiedbotdev:896767281923780608>")

        if user.public_flags.staff == True:
            user_badges.append("<:discord_staff:896767281776951386>")

        if user.public_flags.partner == True:
            user_badges.append("<:discord_partner:896767281789558804>")

        if user.public_flags.bug_hunter == True:
            user_badges.append("<:bughunter:896767281726627911>")

        if user.public_flags.bug_hunter_level_2 == True:
            user_badges.append("<:bughunter_gold:896767281974112286>")

        if guild_db["language"] == "portugues":

            embed.add_field(
                name = "📝 Tag do usuário",
                value = str(user),
                inline = True
            )

            embed.add_field(
                name = "🪧 ID do usuário",
                value = f"`{user.id}`"
            )

            guild_user = ctx.guild.get_member(user.id)

            if guild_user:

                embed.add_field(
                    name  = "📃 Cargo mais alto",
                    value = f"{guild_user.top_role.mention}\n`{guild_user.top_role.id}`"
                )

            text = ""

            if guild_user:

                if guild_user.activities:

                    for item in guild_user.activities:

                        if isinstance(item, disnake.CustomActivity):

                            text += f"**• Status customizado**: {item}\n"

                        if isinstance(item, disnake.Spotify):

                            text += f"**• Spotify**: [{item.title} - {', '.join(item.artists)}]({item.track_url})\n"

                        if isinstance(item, disnake.Game):

                            text += f"**• Jogando**: {item.name}"

                        if isinstance(item, disnake.Streaming):

                            text += f"**• Transmitindo**: [{item.name} - {item.twitch_name}]({item.url})"

                        if item.type == disnake.ActivityType.listening:

                            text += f"**• Ouvindo**: {item.name}\n"

                        if item.type == disnake.ActivityType.watching:

                            text += f"**• Assistindo**: {item.name}\n"

            embed.add_field(
                name = "🏷️ Informações gerais",
                value = f"**• Badges**: {' '.join(user_badges)}\n{text}",
                inline = False
            )

            embed.add_field(
                name = "📅 Conta criada em",
                value = f"<t:{calendar.timegm(user.created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(user.created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                inline = False
            )

            if guild_user:

                embed.add_field(
                    name = "🗓️ Entrou no servidor em",
                    value = f"<t:{calendar.timegm(guild_user.joined_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(guild_user.joined_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                    inline = False
                )

        else:

            embed.add_field(
                name = "📝 User Tag",
                value = str(user),
                inline = True
            )

            embed.add_field(
                name = "🪧 User ID",
                value = f"`{user.id}`"
            )

            guild_user = ctx.guild.get_member(user.id)

            if guild_user:

                embed.add_field(
                    name  = "📃 Highest role",
                    value = f"{guild_user.top_role.mention}\n`{guild_user.top_role.id}`"
                )

            text = ""

            if guild_user:

                if guild_user.activities:

                    for item in guild_user.activities:

                        if isinstance(item, disnake.CustomActivity):

                            text += f"**• Custom status**: {item}\n"

                        if isinstance(item, disnake.Spotify):

                            text += f"**• Spotify**: [{item.title} - {', '.join(item.artists)}]({item.track_url})\n"

                        if isinstance(item, disnake.Game):

                            text += f"**• Playing**: {item.name}"

                        if isinstance(item, disnake.Streaming):

                            text += f"**• Transmitting**: [{item.name} - {item.twitch_name}]({item.url})"

                        if item.type == disnake.ActivityType.listening:

                            text += f"**• Listening**: {item.name}\n"

                        if item.type == disnake.ActivityType.watching:

                            text += f"**• Watching**: {item.name}\n"

            embed.add_field(
                name = "🏷️ General informations",
                value = f"**• Badges**: {' '.join(user_badges)}\n{text}",
                inline = False
            )

            embed.add_field(
                name = "📅 Account created at",
                value = f"<t:{calendar.timegm(user.created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(user.created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                inline = False
            )

            if guild_user:

                embed.add_field(
                    name = "🗓️ Joined the server at",
                    value = f"<t:{calendar.timegm(guild_user.joined_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(guild_user.joined_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                    inline = False
                )

        await ctx.send(embed = embed)

    @user.sub_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user you want to see the avatar",
                type = disnake.OptionType.user,
                required = False
            )
        ]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def avatar(self, ctx, user: disnake.User = None):

        """
        [Discord] See a user's avatar
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if not user:

            user = ctx.author

        embed = disnake.Embed(
            title = f"🖼️ {user.name}",
            color = disnake.Color.blue()
        )

        embed.set_image(url = user.avatar.url)

        button = Button()

        if guild_db["language"] == "portugues":

            button.add_item(
                disnake.ui.Button(
                    label = "Clique aqui para abrir o avatar no navegador",
                    url = user.avatar.url
                )
            )

        else:

            button.add_item(
                disnake.ui.Button(
                    label = "Click here to open the avatar in the browser",
                    url = user.avatar.url
                )
            )

        await ctx.send(
            embed = embed,
            view = button
        )

    @user.sub_command(
        options = [
            disnake.Option(
                name = "user",
                description = "user you want to see the banner",
                type = disnake.OptionType.user,
                required = False
            )
        ]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def banner(self, ctx, user: disnake.User = None):

        """
        [Discord] See a user banner
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        if not user:

            user = ctx.author

        user = await self.client.fetch_user(user.id)

        if not user.banner:

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Eita, parece que o usuário não tem um banner!",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Jeez, it looks like the user doesn't have a banner!",
                        color = disnake.Color.red()
                    )
                )

        else:

            embed = disnake.Embed(
                title = f"🖼️ {user.name}",
                color = disnake.Color.blue()
            )

            embed.set_image(url = user.banner.url)

            button = Button()

            if guild_db["language"] == "portugues":

                button.add_item(
                    disnake.ui.Button(
                        label = "Clique aqui para abrir o banner no navegador",
                        url = user.banner.url
                    )
                )

            else:

                button.add_item(
                    disnake.ui.Button(
                        label = "Click here to open the banner in the browser",
                        url = user.banner.url
                    )
                )

            await ctx.send(
                embed = embed,
                view = button
            )

    @emoji.sub_command(
        options = [
            disnake.Option(
                name = "emoji",
                description = "emoji you want to see information",
                type = disnake.OptionType.string,
                required = True
            )
        ]
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def info(self, ctx, emoji):

        """
        [Discord] View information about an emoji
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        emoji_obj = await Emoji().convert(ctx, emoji)

        if emoji_obj[0] == "normal":

            emoji = emoji_obj[1]

        elif emoji_obj[0] == "custom":

            emoji = f"<:{emoji_obj[1].name}:{emoji_obj[1].id}>"

        else:

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> Foi mal aí mas esse é um emoji inválido!",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> Sorry but this is an invalid emoji!",
                        color = disnake.Color.red()
                    )
                )         

        button = Button()

        if guild_db["language"] == "portugues":

            embed = disnake.Embed(
                title = f"{emoji} Sobre o emoji",
                color = disnake.Color.blue()
            )

            if emoji_obj[0] == "normal":

                try:

                    emoji_unicode = (('{:X}'.format(ord(str(emoji)))).lower())

                    embed.add_field(
                        name = "📝 Nome do emoji",
                        value = f"`{_emoji.demojize(emoji)}`",
                        inline = True
                    )

                    embed.add_field(
                        name = "🖥️ Unicode",
                        value = f"`{emoji_unicode}`",
                        inline = True
                    )

                    embed.add_field(
                        name = f"📃 Menção",
                        value = f"`{emoji}`"
                    )

                    embed.set_thumbnail(url = f"https://twemoji.maxcdn.com/2/72x72/{emoji_unicode}.png")

                    button.add_item(
                        disnake.ui.Button(
                            label = "Clique aqui para abrir o emoji no navegador",
                            url = f"https://twemoji.maxcdn.com/2/72x72/{emoji_unicode}.png"
                        )
                    )

                except:

                    if guild_db["language"] == "portugues":

                        return await ctx.send(
                            embed = disnake.Embed(
                                description = f"<:x_:956703878395625472> Sinto muito más eu não consegui encontrar o emoji `{emoji}`!",
                                color = disnake.Color.red()
                            )
                        )

                    else:

                        return await ctx.send(
                            embed = disnake.Embed(
                                description = f"<:x_:956703878395625472> I'm sorry but I couldn't find the emoji `{emoji}`!",
                                color = disnake.Color.red()
                            )
                        )

            else:

                embed.add_field(
                    name = "📝 Nome do emoji",
                    value = f"{emoji_obj[1].name}",
                    inline = True
                )

                embed.add_field(
                    name = "🪧 ID do emoji",
                    value = f"`{emoji_obj[1].id}`",
                    inline = True
                )

                embed.add_field(
                    name = "📃 Menção",
                    value = f"`{emoji}`",
                    inline = True
                )

                embed.add_field(
                    name = "🏷️ Informações gerais",
                    value = f"**• Servidor**: {emoji_obj[1].guild.name}, `{emoji_obj[1].guild.id}`",
                    inline = False
                )

                embed.add_field(
                    name = "🗓️ Criado em",
                    value = f"<t:{calendar.timegm(emoji_obj[1].created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(emoji_obj[1].created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                    inline = False
                )

                embed.set_thumbnail(url = emoji_obj[1].url)

                button.add_item(
                    disnake.ui.Button(
                        label = "Clique aqui para abrir o emoji no navegador",
                        url = emoji_obj[1].url
                    )
                )

        else:

            embed = disnake.Embed(
                title = f"{emoji} About emoji",
                color = disnake.Color.blue()
            )

            if emoji_obj[0] == "normal":

                try:

                    emoji_unicode = (('{:X}'.format(ord(str(emoji)))).lower())

                    embed.add_field(
                        name = "📝 Emoji name",
                        value = f"`{_emoji.demojize(emoji)}`",
                        inline = True
                    )

                    embed.add_field(
                        name = "🖥️ Unicode",
                        value = f"`{emoji_unicode}`",
                        inline = True
                    )

                    embed.add_field(
                        name = f"📃 Mention",
                        value = f"`{emoji}`"
                    )

                    embed.set_thumbnail(url = f"https://twemoji.maxcdn.com/2/72x72/{emoji_unicode}.png")

                    button.add_item(
                        disnake.ui.Button(
                            label = "Click here to open emoji in browser",
                            url = f"https://twemoji.maxcdn.com/2/72x72/{emoji_unicode}.png"
                        )
                    )

                except:

                    if guild_db["language"] == "portugues":

                        return await ctx.send(
                            embed = disnake.Embed(
                                description = f"<:x_:956703878395625472> Sinto muito más eu não consegui encontrar o emoji `{emoji}`!",
                                color = disnake.Color.red()
                            )
                        )

                    else:

                        return await ctx.send(
                            embed = disnake.Embed(
                                description = f"<:x_:956703878395625472> I'm sorry but I couldn't find the emoji `{emoji}`!",
                                color = disnake.Color.red()
                            )
                        )

            else:

                embed.add_field(
                    name = "📝 Emoji name",
                    value = f"{emoji_obj[1].name}",
                    inline = True
                )

                embed.add_field(
                    name = "🪧 Emoji ID",
                    value = f"`{emoji_obj[1].id}`",
                    inline = True
                )

                embed.add_field(
                    name = "📃 Mention",
                    value = f"`{emoji}`",
                    inline = True
                )

                embed.add_field(
                    name = "🏷️ General information",
                    value = f"**• Server**: {emoji_obj[1].guild.name}, `{emoji_obj[1].guild.id}`",
                    inline = False
                )

                embed.add_field(
                    name = "🗓️ Created at",
                    value = f"<t:{calendar.timegm(emoji_obj[1].created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:F>, <t:{calendar.timegm(emoji_obj[1].created_at.astimezone(pytz.timezone('America/Sao_Paulo')).utctimetuple())}:R>",
                    inline = False
                )

                embed.set_thumbnail(url = emoji_obj[1].url)

                button.add_item(
                    disnake.ui.Button(
                        label = "Click here to open emoji in browser",
                        url = emoji_obj[1].url
                    )
                )

        await ctx.send(embed = embed, view = button)

def setup(client):
    client.add_cog(Comun(client))