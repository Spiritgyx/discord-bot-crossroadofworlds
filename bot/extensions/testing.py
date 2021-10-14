import logging

import discord.ext.commands
from discord.ext import commands, tasks
from discord import Permissions
import bot.mybot
from bot.mylogger import MyLogger
from typing import List, Iterator
import random
import bot.utils.posts as posts


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
        e.set_thumbnail(url=target.avatar_url)
        # member.avatar_url
        # target.roles
        await ctx.send(embed=e)

    @commands.command()
    async def post(self, ctx: commands.Context, post_name: str = None):
        if post_name is None:
            await ctx.send(f"Please enter correct post name.")
            return None
        post = posts.get_post(post_name)
        if post is None:
            await ctx.send(f"Post not exists.")
            return None

        def _get_color(chex: str) -> int:
            import re
            c = chex.upper()
            m = re.findall(r'[0-9A-F]{6}', c)
            if len(m) > 0:
                m = m[0]
                return int('0x'+m, 16)
            else:
                return 0xFFFFFF
        # Start create Embed post
        kwargs_title = {}
        title = post.get('title', None)
        description = post.get('description', None)
        url = post.get('url', None)
        colour = post.get('colour', None)
        if title:
            kwargs_title['title'] = title
            if description:
                kwargs_title['description'] = description
            if url and url.startswith('http'):
                kwargs_title['url'] = url
            if colour:
                kwargs_title['colour'] = _get_color(colour)
        e = discord.Embed(**kwargs_title)

        # Set author if exists
        kwargs_author = post.get('author', None)
        if kwargs_author:
            name = kwargs_author.get('name', None)
            icon_url = kwargs_author.get('icon_url', None)
            url = kwargs_author.get('url', None)
            if icon_url and not icon_url.startswith('http'):
                kwargs_author.pop('icon_url')
                icon_url = None
            if url and not url.startswith('http'):
                kwargs_author.pop('url')
                url = None
            if not kwargs_author.get('optional', None) is None:
                kwargs_author.pop('optional')
            if name or icon_url or url:
                e.set_author(**kwargs_author)

        # Set thumbnail image if exists
        kwargs_thumbnail = post.get("thumbnail", None)
        if kwargs_thumbnail:
            url = kwargs_thumbnail.get('url', None)
            if url and not url.startswith('http'):
                kwargs_thumbnail.pop('url')
                url = None
            if not kwargs_thumbnail.get('optional', None) is None:
                kwargs_thumbnail.pop('optional')
            if url:
                e.set_thumbnail(**kwargs_thumbnail)

        # Set footer if exists
        kwargs_footer = post.get("footer", None)
        if kwargs_footer:
            text = kwargs_footer.get('text', None)
            icon_url = kwargs_footer.get('icon_url', None)
            if icon_url and not icon_url.startswith('http'):
                kwargs_footer.pop('icon_url')
                icon_url = None
            if not kwargs_footer.get('optional', None) is None:
                kwargs_footer.pop('optional')
            if text or icon_url:
                e.set_footer(**kwargs_footer)

        # Set image if exists
        kwargs_image = post.get("image", None)
        if kwargs_image:
            url = kwargs_image.get('url', None)
            if url and not url.startswith('http'):
                kwargs_image.pop('url')
                url = None
            if not kwargs_image.get('optional', None) is None:
                kwargs_image.pop('optional')
            if url:
                e.set_image(**kwargs_image)

        # Set fields
        list_fields = post.get("fields", [])
        for i, field in enumerate(list_fields):
            if not type(field) is dict:
                logging.warning(
                    f"Post {post['name']}; {i}) type is error [{type(field)}] not [dict]")
                continue
            name = field.get("name", None)
            value = field.get("value", None)
            if name == "":
                field["name"] = "noname"
            if value == "":
                field["value"] = "no value"
            inline = field.get("inline", False)
            if not name and not value:
                logging.warning(
                    f"Post {post['name']}; {i}) NAME and VALUE is empty")
                continue
            e.add_field(**field)
        await ctx.send(embed=e)



def setup(client: bot.mybot.Bot):
    client.add_cog(Testing(client))
