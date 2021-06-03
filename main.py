from discord.ext.commands import Bot
from discord import Embed
import json
from discord_components import DiscordComponents, Button

bot=Bot(command_prefix=";")
with open("config.json",'r') as file:
    config=json.load(file)
    token=config["token"]
@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"Logged in as {bot.user}!")
def genEmbed(calc):
    em=Embed(title="Calculator",description=f"```{calc}```")
    em.set_footer(text="❌ - Stop listening for button presses")
    return em
@bot.command()
async def calc(ctx):
    exit=False
    empty="Type a calculation, the result will show up here!"
    calculation=""
    msg=await ctx.send(
        embed=genEmbed(empty),
        components = [
            [Button(label="1"),Button(label="2"),Button(label="3"),Button(label="4")],
            [Button(label="5"),Button(label="6"),Button(label="7"),Button(label="8")],
            [Button(label="7"),Button(label="8"),Button(label="9"),Button(label="0")],
            [Button(label="+"),Button(label="-"),Button(label="*"),Button(label="/")],
            [Button(label="="),Button(label="❌"),Button(label="Clear")]

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
                except:
                    await msg.edit(embed=genEmbed("Invalid calculation!"))
            elif label=="❌":
                exit=True
            elif label=="Clear":
                calculation=""
                await msg.edit(embed=genEmbed(empty))
            else:
                calculation+=i.component.label
                await msg.edit(embed=genEmbed(calculation))
            await i.respond(type=6)


bot.run(token)
