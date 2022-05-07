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
cluster_guilds_tags = cluster["discord"]["guilds_tags"]

class Tags(commands.Cog):
    """Comandos de tag"""

    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def tag(self, ctx):
        pass

    @tag.sub_command(
        options = [
            disnake.Option(
                name = "name",
                description = "tag name",
                type = disnake.OptionType.string,
                required = True
            ),
            disnake.Option(
                name = "category",
                description = "tag category",
                type = disnake.OptionType.string,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def view(self, ctx, name: str, category: str = None):

        """
        [Tag] See a tag
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        tag_db = cluster_guilds_tags.find_one(
            {"guild": ctx.guild.id, "name": name, "category": category}
        )

        if not tag_db:

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Não foi possível achar a tag `{name}`.",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Could not find {name} tag.",
                        color = disnake.Color.red()
                    )
                )                

        else:

            await ctx.send(tag_db["content"])

    @tag.sub_command(
        options = [
            disnake.Option(
                name = "name",
                description = "tag name",
                type = disnake.OptionType.string,
                required = True
            ),
            disnake.Option(
                name = "content",
                description = "tag content",
                type = disnake.OptionType.string,
                required = True
            ),
            disnake.Option(
                name = "category",
                description = "tag category",
                type = disnake.OptionType.string,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def create(self, ctx, name:str, content:str, category: str = None):

        """
        [Tag] Create a tag
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        tag_db = cluster_guilds_tags.find_one(
            {"guild": ctx.guild.id, "name": name, "category": category}
        )

        if tag_db:

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> Não foi possível criar a tag pois já existe uma com o mesmo nome.",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> it was not possible to create the tag because there is already one with the same name.",
                        color = disnake.Color.red()
                    )
                )                

        else:

            cluster_guilds_tags.insert_one(
                {
                    "guild": ctx.guild.id,
                    "name": name,
                    "category": category,
                    "content": content
                }
            )

            if guild_db["language"] == "portugues":

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:success:956703878412394546> A tag `{name}` foi criada com sucesso!",
                        color = disnake.Color.green()
                    )
                )

            else:

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:success:956703878412394546> The `{name}` tag has been successfully created!",
                        color = disnake.Color.green()
                    )
                )

    @tag.sub_command(
        options = [
            disnake.Option(
                name = "name",
                description = "tag name",
                type = disnake.OptionType.string,
                required = True
            ),
            disnake.Option(
                name = "category",
                description = "tag category",
                type = disnake.OptionType.string,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def delete(self, ctx, name: str, category = None):

        """
        [Tag] Delete a tag
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        tag_db = cluster_guilds_tags.find_one_and_delete(
            {
                "guild": ctx.guild.id,
                "name": name,
                "category": category
            }
        )

        if not tag_db:

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Não foi possível achar a tag `{name}`.",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Could not find {name} tag.",
                        color = disnake.Color.red()
                    )
                )    

        else:

            if guild_db["language"] == "portugues":

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:success:956703878412394546> A tag `{name}` foi deletada com sucesso.",
                        color = disnake.Color.green()
                    )
                )

            else:

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:success:956703878412394546> The `{name}` tag was successfully deleted.",
                        color = disnake.Color.green()
                    )
                )           

    @tag.sub_command(
        options = [
            disnake.Option(
                name = "name",
                description = "tag name",
                type = disnake.OptionType.string,
                required = True
            ),
            disnake.Option(
                name = "content",
                description = "new tag content",
                type = disnake.OptionType.string,
                required = True
            ),
            disnake.Option(
                name = "category",
                description = "tag category",
                type = disnake.OptionType.string,
                required = False
            )
        ]
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(manage_messages = True)
    async def edit(self, ctx, name: str, content: str, category: str = None):

        """
        [Tag] Edit a tag
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        tag_db = cluster_guilds_tags.find_one(
            {
                "guild": ctx.guild.id,
                "name": name,
                "category": category
            }
        )

        if not tag_db:

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Não foi possível achar a tag `{name}`.",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Could not find {name} tag.",
                        color = disnake.Color.red()
                    )
                )    

        else:

            cluster_guilds_tags.update_one(
                {
                    "guild": ctx.guild.id,
                    "name": name
                },
                {
                    "$set": {"content": content}
                }
            )

            if guild_db["language"] == "portugues":

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:success:956703878412394546> O conteúdo da tag `{name}` foi alterada com sucesso.",
                        color = disnake.Color.green()
                    )
                )

            else:

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:success:956703878412394546> The content of the `{name}` tag has been successfully changed.",
                        color = disnake.Color.green()
                    )
                )                

    @tag.sub_command()
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def list(self, ctx):

        """
        [Tags] Show server tags
        """

        commandChannelCheck = await commandChannel.checkChannel(ctx)

        if commandChannelCheck == True:
           return

        guild_db = await database.guild(ctx)

        guild_tags = cluster_guilds_tags.find(
            {"guild": ctx.guild.id}
        )

        if not guild_tags:

            if guild_db["language"] == "portugues":

                return await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> Este servidor não possui nenhuma tag no momento.",
                        color = disnake.Color.red()
                    )
                )

            else:

                return await ctx.send(
                    embed = disnake.Embed(
                        description = "<:x_:956703878395625472> This server does not currently have any tags.",
                        color = disnake.Color.red()
                    )
                )            

        else:

            tags_all = []

            for tag in guild_tags:

                if tag["category"]:

                    name = tag["name"]
                    category = tag["category"]

                    tags_all.append(f"{category} {name}")

                else:

                    tags_all.append(tag["name"])

            full_text = ", ".join(tags_all)

            await ctx.send(
                embed = disnake.Embed(
                    title = f"{ctx.guild} tags ({len(tags_all)})",
                    description = full_text,
                    color = disnake.Color.blue()
                )
            )

def setup(client):
    client.add_cog(Tags(client))