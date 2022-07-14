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
        await ctx.send(f'Pong! {client_latency}ms')

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

def setup(client):
    client.add_cog(general(client))
