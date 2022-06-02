import discord
from discord.ext import commands
import datetime


import defi.defi_tools as dft

#-----------------------------------------------------------------------------
#- Config:                                                                   -
#-      name_prj     - The name of the project                               -
#-      token_adr    - The address of the token                              -
#-      abbreviation - The abbreviation of the token                         -
#-      emoji        - Emoji for beautify purpose                            -
#-----------------------------------------------------------------------------

name_prj = ""
token_adr = ""
abbreviation = ""
emoji = ""


bot = commands.Bot(command_prefix='_', description="This is the LP & Impermanent Loss bot for "+name_prj+", best project in the DeFi world!", help_command=None)

def calcula_il(initial_price, end_price):

    ret = end_price / initial_price

    il_s = dft.iloss(ret)

    il = il_s.replace('%','')
    il = float(il)/100

    return il, il_s

def dissasemble_lp(initial_price, end_price, token_amount, token_value_init):


    il, il_s = calcula_il(initial_price, end_price)


    #token_value_init = initial_price * token_amount
    token_value_held = end_price * token_amount
    total_value_held = token_value_held + token_value_init

    total_value_lp = total_value_held + total_value_held * il

    new_amount_token = total_value_lp * 0.5 / end_price
    new_amount_stablecoin = total_value_lp * 0.5

    msg = """
        Impermanent Loss: {:s} 📊

        If {:g} ${:s} {:s} and {:g} BUSD were provided as liquidity and the LPs were disassembled with a new value of ${:g} for the ${:s} {:s} token, you would have:

        - {:g} ${:s} {:s} and {:g} BUSD
        - Value if providing liquidity ${:g}

        Their values if tokens were held: ${:g}
    """.format(il_s, token_amount, abbreviation, emoji, token_amount * initial_price, abbreviation, emoji,
                end_price, abbreviation, emoji, new_amount_token, new_amount_stablecoin, total_value_lp, total_value_held)

    return msg

@bot.command()
async def ILdollars(ctx, *args):

    embed = discord.Embed()

    if len(args) != 3:
        embed.description = "⛔You must provide 3 arguments: Amount in dollars of token, Initial price and End price."
        await ctx.send(embed=embed)
        return
    else:
        try:
            token_value_init = float(args[0])
            initial_price = float(args[1])
            end_price = float(args[2])
        except ValueError:
            embed.description = "⛔All arguments must be numbers!"
            await ctx.send(embed=embed)
            return

    if initial_price <= 0 or end_price <= 0:
        embed.description = "⛔Both prices must be greater than 0"
        await ctx.send(embed=embed)
        return
    if token_value_init <= 0:
        embed.description = "⛔Token amount in dollars must be greater than 0"
        await ctx.send(embed=embed)
        return

    token_amount = token_value_init / initial_price

    msg = dissasemble_lp(initial_price, end_price, token_amount, token_value_init)

    embed.description = msg

    await ctx.send(embed=embed)

@bot.command()
async def ILtokens(ctx, *args):

    embed = discord.Embed()

    if len(args) != 3:
        embed.description = "⛔You must provide 3 arguments: Amount of token, Initial price and End price."
        await ctx.send(embed=embed)
        return
    else:
        try:
            token_amount = float(args[0])
            initial_price = float(args[1])
            end_price = float(args[2])
        except ValueError:
            embed.description = "⛔All arguments must be numbers!"
            await ctx.send(embed=embed)
            return

    if initial_price <= 0 or end_price <= 0:
        embed.description = "⛔Both prices must be greater than 0"
        await ctx.send(embed=embed)
        return
    if token_amount <= 0:
        embed.description = "⛔Token amount must be greater than 0"
        await ctx.send(embed=embed)
        return

    token_value_init = initial_price * token_amount

    msg = dissasemble_lp(initial_price, end_price, token_amount, token_value_init)

    embed.description = msg

    await ctx.send(embed=embed)

@bot.command()
async  def  help(ctx):
    des = """
    Commands for CashCowProtocol LP & Impermanent Loss bot:

     **Prefix**:       _

     **_ILtokens**:       Get information about impermanent loss and tokens amounts/value if you disassembled LPs at a certain price.

                          You must provide the information in this order: amount of token, initial price and future price of the token

     **_ILdollars**:      Get information about impermanent loss and tokens amounts/value if you disassembled LPs at a certain price.

                          You must provide the information in this order: amount of dollars invested in the token, initial price and future price of the token


    """
    embed = discord.Embed(title="I'm the price bot for "+name_prj+", best project in the DeFi world!",url="###########",description= des,
    timestamp=datetime.datetime.utcnow(),
    color=discord.Color.blue())
    embed.set_footer(text="Made by v0st0k1")


    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="_help"))
    print('The LP & Impermanent Loss Calculator Bot is ready!')



bot.run('######################')
