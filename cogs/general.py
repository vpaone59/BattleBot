import discord
import time
import json
import os
from discord.ext import commands
from discord.utils import get

# Vincent Paone
# Cogs for BattleBot


class general(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['hi'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hello(self, ctx):
        user_id = ctx.author
        await ctx.send(f'Hello {user_id.mention}')

    @commands.command(aliases=['hiall'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def helloO(self, ctx):
        user_id = ctx.author
        await ctx.send(f'Hello {ctx.message.guild.default_role}')

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        client_latency = round(self.client.latency * 1000, 2)
        await ctx.send(f'ObamaPong! {client_latency}ms')

        if client_latency > 100:
            time.sleep(1)
            await ctx.send('YIKES!')
        elif client_latency < 100 and client_latency >= 60:
            time.sleep(1)
            await ctx.send('Sloooow')
        elif client_latency < 60 and client_latency >= 30:
            time.sleep(1)
            await ctx.send('Average')
        else:
            time.sleep(1)
            await ctx.send('Get a load of this guy!')

    # list the roles of the user
    @commands.command(aliases=['ia'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def isAmerican(self, ctx, user: discord.Member):
        role = discord.utils.find(
            lambda r: r.name == 'American', ctx.message.guild.roles)
        if role in user.roles:
            await ctx.send(f"User {user.mention} is a PATRIOT!!")
        else:
            await ctx.send(f"User {user.mention} is NOT A TRUE CHRISTIAN AMERICAN!!")

    # @commands.command(aliases=['makerole'])
    # @commands.cooldown(1, 3, commands.BucketType.user)
    # async def createrole(self, ctx, role):
    #     if get(ctx.guild.roles, name=role):
    #         await ctx.send("Role already exists!")
    #     else:
    #         await ctx.guild.create_role(name="American", color=discord.Color(0x0062ff))

    # @commands.command()
    # async def list(self, ctx):
    #     # for command in self.client.command:
    #     #     await ctx.send(f'{command}')
    #     command_list = []
    #     all_commands = [command.name for command in self.client.commands]
    #     for c in all_commands:
    #         command_name = c
    #         command_list = command_list + "\n" + command_name
    #     if not command_list:
    #         await ctx.send(f'no commands available')
    #     else:
    #         await ctx.send(f'{command_list}')


def setup(client):
    client.add_cog(general(client))
