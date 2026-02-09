import discord
from discord.ext import commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        """A simple command to test if the Cog is loaded."""
        await ctx.send(f"Pong! Economy module is active. {round(self.bot.latency * 1000)}ms")

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx):
        """Template command for checking balance."""
        # For now, we'll hardcode a response. 
        # Later, we will connect this to a database.
        await ctx.send(f"💰 **{ctx.author.name}**, your current balance is **$1,000** (Template Default).")

async def setup(bot):
    await bot.add_cog(Economy(bot))