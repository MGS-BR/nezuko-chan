import disnake
import json

from pymongo import MongoClient
from disnake.ext import commands

from cogs.utilities.databaseUsage import database

with open("config.json") as w:
    infos = json.load(w)
    connection_url = infos["mongo"]

translate_permissions = {
    "ban_members": "banir membros",
    "kick_members": "expulsar membros",
    "administrator": "adminstrador",
    "manage_messages": "gerenciar mensagens",
    "manage_channels": "gerenciar canais",
    "manage_guild": "gerenciar o servidor",
    "manage_roles": "gerenciar cargos",
    "manage_nicknames": "gerenciar apelidos",
    "manage_emojis": "gerenciar emojis",
    "moderate_members": "moderar membros"
}

class PermissionError(commands.Cog):
    """Permission error"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):

        error = getattr(error, "original", error)

        guild_db = await database.guild(ctx)

        if isinstance(error, commands.BotMissingPermissions):

            if guild_db["language"] == "portugues":

                missing_permissions_translate = [translate_permissions[permission] for permission in error.missing_permissions]

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Parece que eu não tenho as permissões necessárias para executar este comando, por favor verifique se eu tenho todas as permissões necessárias para o comando: `{', '.join(missing_permissions_translate)}`",
                        color = disnake.Color.red()
                    )
                )

            else:

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> It looks like I don't have the required permissions to run this command, please make sure I have all the required permissions for the command: `{', '.join(error.missing_permissions)}`",
                        color = disnake.Color.red()
                    )
                )    

        elif isinstance(error, commands.MissingPermissions):

            if guild_db["language"] == "portugues":

                missing_permissions_translate = [translate_permissions[permission] for permission in error.missing_permissions]

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Ops, parece que você não tem as permissões necessárias para executar este comando: `{', '.join(missing_permissions_translate)}`",
                        color = disnake.Color.red()
                    ),
                    ephemeral = True
                )

            else:

                await ctx.send(
                    embed = disnake.Embed(
                        description = f"<:x_:956703878395625472> Oops, it looks like you don't have the necessary permissions to run this command: `{', '.join(error.missing_permissions)}`",
                        color = disnake.Color.red()
                    ),
                    ephemeral = True
                )    
 
def setup(client):
    client.add_cog(PermissionError(client))