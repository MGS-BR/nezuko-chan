import disnake
import datetime
import json

from pymongo import MongoClient
from disnake.ext import commands
from easy_pil import Editor, load_image_async, Font

from cogs.utilities.commandChannel import commandChannel
from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

def human_format(num):
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format("{:f}".format(num).rstrip("0").rstrip("."), ["", "K", "M", "B", "T"][magnitude])

cluster = MongoClient(connection_url)
cluster_users = cluster["discord"]["users"]
cluster_guilds = cluster["discord"]["guilds"]
cluster_guilds_xp = cluster["discord"]["guilds_xp"]

class Level(commands.Cog):
    """Comandos de level"""

    def __init__(self, client):
        self.client = client
        
    @commands.slash_command()
    async def xp(self, ctx):

        pass

    @xp.sub_command_group()
    async def leaderboard(self, ctx):

        pass

    @leaderboard.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def globals(self, ctx):

        """
        [Level] Global xp leadboard
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        global_ranks = cluster_users.find().sort("xp", -1)

        i = 1

        embed = disnake.Embed(
            title = "Global xp leaderboard",
            color = disnake.Color.blurple(),
            timestamp = datetime.datetime.utcnow()
            )

        for x in global_ranks:

            try:

                if i == 1:
                    posicao = f"🥇 {i}" # primeiro lugar
                elif i == 2:
                    posicao = f"🥈 {i}" # segundo lugar
                elif i == 3:
                    posicao = f"🥉 {i}" # terceiro lugar
                else:
                    posicao = i

                temp = self.client.get_user(x["id"])
                tempxp = x["xp"]

                lvl = 0
                while True:
                    if tempxp < ((50*(lvl**2))+(50*lvl)):
                        break
                    lvl +=1

                embed.add_field(name=f"{posicao}º {temp.name}",
                value=f"Xp: {human_format(tempxp)}\nLevel: {lvl}", inline=False)

                i +=1
            except:
                pass
            if i == 11:
                break

        global_ranks = cluster_users.find().sort("xp", -1)

        user_global_rank = await database.user(ctx)

        user_rank = 1

        for i in global_ranks:

            if user_global_rank["id"] == i["id"]:

                break

            if self.client.get_user(i["id"]) != None:

                user_rank +=1

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            embed.set_footer(text=f"Seu ranking: {user_rank}º \u200b")

        else:

            embed.set_footer(text=f"Your ranking: {user_rank}º \u200b")

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/326/326887.png")
        await ctx.send(embed=embed)

    @leaderboard.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def local(self, ctx):

        """
        [Level] Local xp leadboard
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        user_guild_db = await database.level_guild(ctx)

        local_ranks = cluster_guilds_xp.find({"guild": ctx.guild.id}).sort("xp", -1)

        i = 1

        embed = disnake.Embed(
            title = "Local xp leaderboard",
            color = disnake.Color.blurple(),
            timestamp = datetime.datetime.utcnow()
            )

        for x in local_ranks:

            try:

                if i == 1:
                    posicao = f"🥇 {i}" # primeiro lugar
                elif i == 2:
                    posicao = f"🥈 {i}" # segundo lugar
                elif i == 3:
                    posicao = f"🥉 {i}" # terceiro lugar
                else:
                    posicao = i

                temp = ctx.guild.get_member(x["user"])
                tempxp = x["xp"]

                lvl = 0
                while True:
                    if tempxp < ((50*(lvl**2))+(50*lvl)):
                        break
                    lvl +=1

                embed.add_field(name=f"{posicao}º {temp.name}",
                value=f"Xp: {human_format(tempxp)}\nLevel: {lvl}", inline=False)

                i +=1
                
            except:
                pass
            if i == 11:
                break

        local_ranks = cluster_guilds.find({"guild": ctx.guild.id}).sort("xp", -1)

        user_local_rank = cluster_guilds.find_one({"guild": ctx.guild.id, "user": ctx.author.id})

        user_rank = 1

        for i in local_ranks:

            if user_local_rank["user"] == i["user"]:

                break

            if self.client.get_user(i["user"]) != None:

                user_rank +=1

        if guild_db["language"] == "portugues":

            embed.set_footer(text=f"Seu ranking: {user_rank}º \u200b")

        else:

            embed.set_footer(text=f"Your ranking: {user_rank}º \u200b")

        embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @xp.sub_command(
        options = [
            disnake.Option(
                name = "user",
                description = "User to view xp stats",
                type = disnake.OptionType.user,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stats(self, ctx, user: disnake.Member = None):

        """
        [Level] Show all XP stats
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        if not user:
            user = ctx.author

        guild_db = await database.guild(ctx)

        if guild_db["language"] == "portugues":

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processando o comando...", color = disnake.Color.green())
            )

        else:

            await ctx.send(
                embed = disnake.Embed(description="<a:loading:957418002821824542> Processing the command...", color = disnake.Color.green())
            )

        if ctx.guild.get_member(user.id) == None:

            if guild_db["language"] == "portugues":

                return await ctx.edit_original_message(
                    embed = disnake.Embed(description="<:x_:956703878395625472> Opa, parece que esse usuário não está no servidor!", color = disnake.Color.red())
                )

            else:

                return await ctx.edit_original_message(
                    embed = disnake.Embed(description="<:x_:956703878395625472> I'm sorry but it looks like this user is not on the server!", color = disnake.Color.red())
                )

        else:

            if ctx.guild.get_member(user.id) != None:

                user_guild_db = await database.level_guild(ctx, user=user)

                xp_local = user_guild_db["xp"]
                lvl_local = 0

                while True:
                    if xp_local < ((50*(lvl_local**2))+(50*lvl_local)):
                        break
                    lvl_local +=1

                xp_local -= ((50*((lvl_local-1)**2))+(50*(lvl_local-1)))

                local_rank = 1

                rankings_local = cluster_guilds.find({"guild":ctx.guild.id}).sort("xp",-1)

                for x in rankings_local:

                    if user_guild_db["user"] == x["user"]:
                        break

                    if ctx.guild.get_member(x["user"]) != None:
                        local_rank +=1

            xp_have = xp_local / int(200*((1/2)*lvl_local))

            percentage = xp_have * 100
            
            if percentage < 5:
                percentage = 3

            background = Editor("./cogs/images/assets/level/bg_level.png")

            background.ellipse((27, 27), width=156, height=156, fill="#17F3F6")

            profile = await load_image_async(str(user.avatar.url))

            profile = Editor(profile).resize((150, 150)).circle_image()

            poppins = Font.poppins(size=40)
            poppins_small = Font.poppins(size=30)

            background.paste(profile.image, (30, 30))

            background.rectangle((30, 220), width=650, height=40, fill="white", radius=20)

            background.bar(
                (30, 220),
                max_width=650,
                height=40,
                percentage=percentage,
                fill="#FF56B2",
                radius=20,
            )

            background.text((200, 40), f'{str(user)} ', font=poppins, color="white")

            background.rectangle((200, 100), width=600, height=2, fill="#17F3F6")

            background.text(
                (200, 130),
                f"Rank: #{local_rank} / {len(ctx.guild.members)}",
                font=poppins_small,
                color="white",
            )

            background.text(
                (200, 170),
                f"Level: {lvl_local}  XP: {human_format(xp_local)} / {human_format(int(200*((1/2)*lvl_local)))}",
                font=poppins_small,
                color="white",
            )

            file = disnake.File(fp=background.image_bytes, filename="card.png")
            
            await ctx.edit_original_message(embed=None, file=file)

def setup(client):
    client.add_cog(Level(client))