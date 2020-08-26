import traceback

import discord
from discord.ext import commands
from google.cloud import error_reporting


client = discord.Client()


class Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ERROR HANDLER
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        teams = [270848136006729728]
        error_return = f"Error: {error} (Command: {ctx.command})"
        etype = type(error)
        trace = error.__traceback__
        verbosity = 2
        exception = traceback.format_exception(etype, error, trace, verbosity)
        traceback_text = ''.join(exception)
        if isinstance(error, commands.CommandInvokeError) and not isinstance(error, discord.Forbidden):
            embed = discord.Embed(title="An Exception Occurred",
                                  description=f"Durning handling of this command, an unexpected error has occured \n This error has been sent to the bot dev and will get to it ASAP \n\n `{error}`")
            await ctx.send(embed=embed)
            client = error_reporting.Client()
            client.report('An Error Occurred')
            for me in teams:
                me = self.bot.get_user(me)
                await me.send(f"`New exception occurred in guild {ctx.guild} for command {ctx.command}`")
                await me.send(f"```py\n{traceback_text}```")
            return
        elif not isinstance(error, commands.CommandNotFound):
            await ctx.send(error_return)
            return


def setup(bot):
    bot.add_cog(Handler(bot))
