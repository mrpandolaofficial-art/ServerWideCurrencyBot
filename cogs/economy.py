import discord
import random
from discord.ext import commands
from database import db

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        """Check your global balance or someone else's."""
        member = member or ctx.author
        user_data = db.get_user(member.id)
        wallet, bank = user_data[1], user_data[2]
        
        embed = discord.Embed(title=f"💰 {member.display_name}'s Balance", color=discord.Color.green())
        embed.add_field(name="Wallet", value=f"`${wallet:,}`", inline=True)
        embed.add_field(name="Bank", value=f"`${bank:,}`", inline=True)
        embed.set_footer(text="GlobEx — Global Economy")
        await ctx.send(embed=embed)

    @commands.command(name="beg")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        amount = random.randint(10, 100)
        db.update_wallet(ctx.author.id, amount)
        await ctx.send(f"🪙 A kind stranger gave you **${amount}**!")

    @commands.command(name="work")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        jobs = ["Software Developer", "Digital Artist", "Burger Flipper", "Discord Mod"]
        job = random.choice(jobs)
        pay = random.randint(500, 1500)
        db.update_wallet(ctx.author.id, pay)
        await ctx.send(f"💼 You worked as a **{job}** and earned **${pay:,}**!")

    @commands.command(name="pay", aliases=["send"])
    async def pay(self, ctx, member: discord.Member, amount: int):
        if member.id == ctx.author.id: return await ctx.send("❌ You can't pay yourself!")
        if amount <= 0: return await ctx.send("❌ You must pay at least $1.")
        
        sender_data = db.get_user(ctx.author.id)
        if sender_data[1] < amount: return await ctx.send("❌ Insufficient funds!")

        db.update_wallet(ctx.author.id, -amount)
        db.update_wallet(member.id, amount)
        await ctx.send(f"✅ Sent **${amount:,}** to **{member.display_name}**!")

    @commands.command(name="slots")
    async def slots(self, ctx, amount: int):
        user_data = db.get_user(ctx.author.id)
        if user_data[1] < amount: return await ctx.send("❌ Insufficient funds!")
        if amount <= 0: return await ctx.send("❌ Bet at least $1.")

        emojis = "🍎🍊🍇💎"
        result = [random.choice(emojis) for _ in range(3)]
        machine = " | ".join(result)

        if len(set(result)) == 1:
            winnings = amount * 5
            db.update_wallet(ctx.author.id, winnings)
            await ctx.send(f"🎰 **{machine}** 🎰\nJACKPOT! You won **${winnings:,}**!")
        elif len(set(result)) == 2:
            winnings = amount * 2
            db.update_wallet(ctx.author.id, winnings)
            await ctx.send(f"🎰 **{machine}** 🎰\nNice! You won **${winnings:,}**!")
        else:
            db.update_wallet(ctx.author.id, -amount)
            await ctx.send(f"🎰 **{machine}** 🎰\nLost **${amount:,}**.")

    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx):
        top_users = db.get_leaderboard()
        description = ""
        for i, (user_id, total) in enumerate(top_users, start=1):
            user = self.bot.get_user(user_id)
            name = f"User {user_id}" if user is None else user.display_name
            description += f"**{i}. {name}** — ${total:,}\n"

        embed = discord.Embed(title="🌍 Global Leaderboard", description=description, color=discord.Color.gold())
        await ctx.send(embed=embed)

    # Cooldown Error Handler
    @cog_app_command_error # This handles errors for all commands in this Cog
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Slow down! Try again in **{error.retry_after:.1f}s**.")

async def setup(bot):
    await bot.add_cog(Economy(bot))