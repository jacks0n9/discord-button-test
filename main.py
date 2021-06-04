from logging import exception
from discord.ext.commands import Bot
from discord import Embed
from random import choice
import discord
import json
from discord_components import DiscordComponents, Button,ButtonStyle
bot=Bot(command_prefix=";")
with open("config.json",'r') as file:
    config=json.load(file)
    token=config["token"]
@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}!")

@bot.command()
async def calc(ctx):
    def genEmbed(calc):
        em=Embed(title="Calculator",description=f"```-                              {calc}```",color=discord.Color.teal())
        return em
    exit=False

    calculation=""
    msg=await ctx.send(
        embed=genEmbed("0"),
        components = [
            [Button(label="1"),Button(label="2"),Button(label="3"),Button(label="4"),Button(label="5")],
            [Button(label="6"),Button(label="7"),Button(label="8"),Button(label="9"),Button(label="8")],
            [Button(label="9" ),Button(label="0"),Button(label="."),Button(label="Done",style=ButtonStyle.red),Button(label="Clear",style=ButtonStyle.green)],
            [Button(label="/",style=ButtonStyle.blue),Button(label="+",style=ButtonStyle.blue),Button(label="-",style=ButtonStyle.blue),Button(label="*",style=ButtonStyle.blue),Button(label="=",style=ButtonStyle.blue)]
        ]
    )

    while not exit:
        i=await bot.wait_for("button_click")
        if i.message==msg:
            label=i.component.label
            if label=="=":
                try:
                    calculation=str(eval(calculation))
                    await msg.edit(embed=genEmbed(calculation))
                except exception as e:
                    await msg.edit(embed=genEmbed("Invalid calculation!"))
                    print(e)
            elif label=="Done":
                exit=True
            elif label=="Clear":
                calculation=""
                await msg.edit(embed=genEmbed("0"))
            else:
                calculation+=i.component.label
                await msg.edit(embed=genEmbed(calculation))
            await i.respond(type=6)

@bot.command()
async def clicker(ctx):
    exit=False
    num=0
    print("hi")
    msg=await ctx.send(
        "0",
        components=[
            [Button(label="+"),Button(label="-"),Button(label="Reset"),Button(label="Done")]
        ]
    )
    while not exit:
        i=await bot.wait_for("button_click")
        label=i.component.label
        if label=="+":
            num+=1
        elif label=="-":
            num-=1
        elif label=="Reset":
            num=0
        elif label=="Done":
            exit=True
        await msg.edit(content=str(num))
        await i.respond(type=6)


bot.run(token)
