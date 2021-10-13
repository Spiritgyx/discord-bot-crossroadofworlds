import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.mybot
from bot.mylogger import MyLogger
from typing import List, Iterator
import random


class Testing(commands.Cog):
    def __init__(self, client: bot.mybot.Bot):
        self.client = client
        self.sql = self.client.sql
        self.logger = MyLogger('testing', 'testing.log', levels=(client.level, 20))

    @commands.command()
    async def get_current_members(self, ctx: commands.Context):
        sql_members = self.sql.get_members(ctx.guild.id)
        self.logger.debug(str(sql_members))
        await ctx.send('\n'.join(map(str, sql_members)))

    @commands.command()
    async def pifpaf(self, ctx: commands.Context):
        e = discord.Embed(title="BAM", description="Pif puf paf", colour=random.randint(0x00, 0xffffff))
        await ctx.send(embed=e)

    @commands.command()
    async def me(self, ctx: commands.Context, member: discord.Member=None):
        if member is None:
            target = ctx.message.author
        else:
            target = member

        e = discord.Embed(title=f"{target.name}#{target.discriminator}",
                          description=f"{target.display_name or target.name}",
                          colour=random.randint(0x00, 0xffffff),
                          url='https://discord.gg/qMMskt4Z')
        e.add_field(name="Mention", value=f"{target.mention}", inline=False)
        e.add_field(name="Joined", value=f"{target.joined_at}", inline=True)
        e.add_field(name="GuildID", value=f"{target.guild.id}", inline=True)
        e.add_field(name="MemberID", value=f"{target.id}", inline=True)
        e.add_field(name="voice?", value=f"{target.voice}", inline=False)
        e.add_field(name="color?", value=f"{target.color}")
        e.add_field(name="colour?", value=f"{target.colour}")
        e.add_field(name="desktop_status?", value=f"{target.desktop_status}")
        e.add_field(name="guild_permissions?", value=f"{target.guild_permissions}")
        e.add_field(name="activity?", value=f"{target.activity}")
        e.add_field(name="roles?", value=f"{target.roles}")
        e.add_field(name="top_role?", value=f"{target.top_role}")
        e.add_field(name="avatar_url?", value=f"{target.avatar_url}")
        e.set_footer(text=f"Down information", icon_url=target.avatar_url)
        e.set_image(url=target.avatar_url)
        e.set_author(name=f"{target.name}#{target.discriminator}",
                     url="https://discord.gg/qMMskt4Z",
                     icon_url=target.avatar_url)
        # member.avatar_url
        # target.roles
        await ctx.send(embed=e)

def setup(client: bot.mybot.Bot):
    client.add_cog(Testing(client))
