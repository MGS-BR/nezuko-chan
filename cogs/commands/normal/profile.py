import disnake
import json
import os

from pymongo import MongoClient
from disnake.ext import commands
from easy_pil import Editor, load_image_async, Font

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

cluster = MongoClient(connection_url)
cluster_guilds = cluster["discord"]["guilds"]
cluster_users = cluster["discord"]["users"]

class Button(disnake.ui.View):

    def __init__(self):

        super().__init__()

        self.user = None

class Select(disnake.ui.View):

    def __init__(self):

        super().__init__()

    options = []

    for image in os.listdir("./cogs/images/assets/profile/"):

        options.append(
            disnake.SelectOption(
                label = image[:-4],
                value = image[:-4]
            )
        )

    @disnake.ui.select(
        placeholder = "Select your background - Selecione o seu background",
        custom_id = "background",
        max_values = 1,
        options = options
    )
    async def background(self, select: disnake.SelectOption, ctx: disnake.MessageInteraction):

        guild_db = await database.guild(ctx)

        user_db = await database.user(ctx)

        if select.values[0] in user_db["wallpapers"]:

            cluster_users.update_one(
                {
                    "id": ctx.author.id
                },
                {
                    "$set": {"wallpaper": f"{select.values[0]}.png"}
                }
            )

            file = disnake.File(f"./cogs/images/assets/profile/{select.values[0]}.png", filename=f"{select.values[0]}.png")

            embed = disnake.Embed(
                description = f"<:success:956703878412394546> O seu novo background é: `{select.values[0]}`",
                color = disnake.Color.green()
            )

            embed.set_image(url=f"attachment://{select.values[0]}.png")

            return await ctx.message.edit(
                embed = embed,
                file = file,
                view = None
            )

        if user_db["coins"] < 1000:

            if guild_db["language"] == "portugues":

                return await ctx.message.edit(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Ops, você não tem coins o suficiente para escolher um novo background!\nPara escolher um novo background é necessário ter **1K coins**!",
                        color = disnake.Color.red()
                    ),
                    attachments = [],
                    view = None
                )

            else:

                return await ctx.message.edit(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Oops, you don't have enough coins to choose a new background!\nTo choose a new background you need **1K coins**!",
                        color = disnake.Color.red()
                    ),
                    attachments = [],
                    view = None
                )         

        else:

            cluster_users.update_one(
                {
                    "id": ctx.author.id
                },
                {
                    "$inc": {"coins": -1000}
                }
            )

            cluster_users.update_one(
                {
                    "id": ctx.author.id
                },
                {
                    "$set": {"wallpaper": f"{select.values[0]}.png"}
                }
            )

            cluster_users.update_one(
                {
                    "id": ctx.author.id
                },
                {
                    "$push": {"wallpapers": select.values[0]}
                }
            )

            file = disnake.File(f"./cogs/images/assets/profile/{select.values[0]}.png", filename=f"{select.values[0]}.png")

            if guild_db["language"] == "portugues":

                embed = disnake.Embed(
                    description = f"<:success:956703878412394546> O seu novo background é: `{select.values[0]}`",
                    color = disnake.Color.green()
                )

                embed.set_image(url=f"attachment://{select.values[0]}.png")

                embed.set_footer(text="Compra efetuada com sucesso!")

            else:

                embed = disnake.Embed(
                    description = f"<:success:956703878412394546> Your new background is: `{select.values[0]}`",
                    color = disnake.Color.green()
                )

                embed.set_image(url=f"attachment://{select.values[0]}.png")

                embed.set_footer(text="Purchase made successfully!")      

            return await ctx.message.edit(
                embed = embed,
                file = file,
                view = None
            )

def human_format(num):
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format("{:f}".format(num).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude])

class Profile(commands.Cog):
    """Comandos de perfil"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        options = [
            disnake.Option(
                name = "user",
                description = "person you want to see profile",
                type = disnake.OptionType.user,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def profile(self, ctx, user: disnake.User = None):

        """
        [Profile] See your profile or that of another user
        """

        if not user:

            user = ctx.author

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        user_db = await database.user(ctx, user)

        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processando o comando...", color = disnake.Color.green())
            )

        else:

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processing the command...", color = disnake.Color.green())
            )

        user_global_lvl = 0

        while True:

            if user_db["xp"] < ((50*(user_global_lvl**2))+(50*user_global_lvl)):

                break
            
            user_global_lvl += 1

        user_reps = len(user_db["reps"])
        user_custom_status = user_db["status"]

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=25)
        poppins_ultra_small = Font.poppins(size=20)

        user_background = user_db["wallpaper"]

        background = Editor(f"./cogs/images/assets/profile/{user_background}")

        background.ellipse((525, 45), width = 200, height = 200, fill = "#17F3F6")

        profile = await load_image_async(str(user.avatar.url))

        profile = Editor(profile).resize((190, 190)).circle_image()

        background.paste(profile.image, (530, 50))

        background.text((25, 40), str((user.name)), font=poppins, color="white")
        
        background.text((25, 100), (f"Reps: {user_reps}"), font=poppins_small, color="white")
        
        if user_db["marry"]["stats"] == True:
        
            other_user = self.client.get_user(int(user_db["marry"]["user"]))
            
            background.text((25, 140), (f"Casado: Sim, {other_user.name}"), font=poppins_small, color="white")

        else:
        
            background.text((25, 140), (f"Casado: Não"), font=poppins_small, color="white") 

        user_xp = user_db["xp"]

        user_coins = user_db["coins"]

        background.text(
            (25, 200),
            f"Level: {user_global_lvl}  Xp: {human_format(user_xp)} / {human_format(int(200*((1/2)*user_xp)))}  Coins: {human_format(user_coins)}",
            font=poppins_small,
            color="white"
        )

        background.text((25, 260), (user_custom_status[:35]), font=poppins_ultra_small, color="white")
        background.text((25, 286), (user_custom_status[35:65]), font=poppins_ultra_small, color="white") 
        background.text((25, 308), (user_custom_status[65:95]), font=poppins_ultra_small, color="white") 

        background.rectangle((25, 80), width=400, height=2, fill="#17F3F6")
        
        background.rectangle((25, 180), width=400, height=2, fill="#17F3F6")

        background.rectangle((25, 240), width=400, height=2, fill="#17F3F6")

        emoji_guild = self.client.get_guild(863538221366509578)

        if user_db["xp"] >= 1990000: # lvl 200

            emoji = disnake.utils.get(emoji_guild.emojis, id = 896767281663729715)

            emoji_canva = await load_image_async(str(emoji.url))

            emoji_canva = Editor(emoji_canva).resize((50, 50)).circle_image()

            background.paste(emoji_canva.image, (600, 260))

        elif user_db["xp"] >= 495000: # lvl 100
            
            emoji = disnake.utils.get(emoji_guild.emojis, id = 896767281940557875)

            emoji_canva = await load_image_async(str(emoji.url))

            emoji_canva = Editor(emoji_canva).resize((50, 50)).circle_image()

            background.paste(emoji_canva.image, (600, 260))

        elif user_db["xp"] >= 122500: #lvl 50
            
            emoji = disnake.utils.get(emoji_guild.emojis, id = 896767282032832522)

            emoji_canva = await load_image_async(str(emoji.url))

            emoji_canva = Editor(emoji_canva).resize((50, 50)).circle_image()

            background.paste(emoji_canva.image, (600, 260))

        elif user_db["xp"] >= 4500: # lvl 10
            
            emoji = disnake.utils.get(emoji_guild.emojis, id = 896767281705652226)

            emoji_canva = await load_image_async(str(emoji.url))

            emoji_canva = Editor(emoji_canva).resize((50, 50)).circle_image()

            background.paste(emoji_canva.image, (600, 260))

        else:

            emoji = disnake.utils.get(emoji_guild.emojis, id = 906162056120647690)

            emoji_canva = await load_image_async(str(emoji.url))

            emoji_canva = Editor(emoji_canva).resize((50, 50)).circle_image()

            background.paste(emoji_canva.image, (600, 260))

        file = disnake.File(fp = background.image_bytes, filename = "card.png")

        if guild_db["language"] == "portugues":

            content = f"📝 **|** Perfil de: `{user}`"

        else:

            content = f"📝 **|** `{user}` profile"

        button = Button()

        button.add_item(
            disnake.ui.Button(
                label = "Top gg upvote (100% + xp)",
                emoji = "<:topgg_icon:928011852984774716>",
                url = "https://top.gg/bot/783035541611610113/vote"
            )
        )

        button.add_item(
            disnake.ui.Button(
                label = "Dbl upvote (100% + xp)",
                emoji = "<:dbl_icon:928011810907512863>",
                url = "https://discordbotlist.com/bots/nezuko-chan/upvote"
            )
        )

        await ctx.edit_original_message(
            embed = None,
            file = file,
            content = content,
            view = button
        )

    @commands.slash_command()
    async def profilechange(self, ctx):
        pass

    @profilechange.sub_command(
        options = [
            disnake.Option(
                name = "text",
                description = "new text for your profile description",
                type = disnake.OptionType.string,
                required = True
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def description(self, ctx, text: str):

        """
        [Profile] Change your profile description text
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        user_db = await database.user(ctx)

        if len(text) > 95:

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> O texto da descrição não pode ultrapassar **95 caracteres**!",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> Description text cannot exceed **95 characters**!",
                        color = disnake.Color.red()
                    )
                )       

        cluster_users.update_one({"id": ctx.author.id}, {"$set": {"status": text}})

        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(
                    description = f"📝 A sua descrição foi alterada para:\n`{text}`",
                    color = disnake.Color.green()
                )
            )

        else:

            await ctx.send(
                embed = disnake.Embed(
                    description = f"📝 Your description has been changed to:\n`{text}`",
                    color = disnake.Color.green()
                )
            )

    @profilechange.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def background(self, ctx):

        """
        [Profile] Change your profile background
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        user_db = await database.user(ctx)

        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processando o comando...", color = disnake.Color.green())
            )

        else:

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processing the command...", color = disnake.Color.green())
            )

        valid_images = []

        embeds = []

        files = []

        if guild_db["language"] == "portugues":

            text_embed = disnake.Embed(
                    description = "⬇️ Confira abaixo todos os wallpapers disponíveis para o seu perfil.\n┕ Cada background novo custa 1k coins!",
                    color = disnake.Color.green()
                )

            embeds.append(text_embed)

        else:

            text_embed = disnake.Embed(
                    description = "⬇️ Check out all the wallpapers available for your profile below.\n┕ Each new background costs 1k coins!",
                    color = disnake.Color.green()
                )

            embeds.append(text_embed)

        for image in os.listdir("./cogs/images/assets/profile/"):

            file = disnake.File(f"./cogs/images/assets/profile/{image}", filename=image)

            valid_images.append(image[:-4])

            image_embed = disnake.Embed(
                description = image[:-4],
                color = disnake.Color.blue()
            )

            image_embed.set_image(url=f"attachment://{image}")

            embeds.append(image_embed)
            files.append(file)

        select = Select()

        await ctx.edit_original_message(embeds = embeds, files = files, view = select)

def setup(client):
    client.add_cog(Profile(client))