import discord
from datetime import datetime
import matplotlib.pyplot as plt

import config
from req_helper import get_data


bot = discord.Client()

@bot.event
async def on_ready():
    print(f"Ingelogd als {bot.user}")
    game = discord.Game("!kamervanjens help")
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!kamervanjens'):
        args = message.content.lower().split(" ")[1:]
        if len(args) >= 1:
            if args[0] == "history":
                if len(args) >= 2:
                    data = get_data(route="history", params={"amount": int(args[1])})
                else:
                    data = get_data(route="history")
                all_data = []
                for data_point in data:
                    all_data.append(data_point["temperature"])
                plt.clf()
                plt.plot(all_data)
                plt.savefig("graph.png")
                await message.channel.send(file=discord.File(fp="./graph.png"))
            elif args[0] == "outside":
                data = get_data("outside")
                embed = discord.Embed(title="(niet meer) Jens' Kamer: Rotterdam", description="Voor als je moet fietsen.", colour=0x779bff)
                embed.set_footer(text="Jens de Ruiter", icon_url="https://cdn.discordapp.com/avatars/283554212019699722/6aef6a5e52d6420baf7d2a25274f562e.png?size=256")
                embed.add_field(name=f"{int(data['temperature'])}℃", value="Dit is de temperatuur in Rotterdam.")
                embed.add_field(name=f"{int(data['humidity'])}%", value="Dit is de luchtvochtigheid in Rotterdam.")
                embed.add_field(name=f"{int(data['wind'])}km\\h", value="Dit is de windsnelheid in Rotterdam.")
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Jens' Kamer: Help", description="Hoe werkt dit?", colour=0x779bff)
                embed.set_footer(text="Jens de Ruiter", icon_url="https://cdn.discordapp.com/avatars/283554212019699722/6aef6a5e52d6420baf7d2a25274f562e.png?size=256")
                embed.add_field(name=f"!kamervanjens", value="help\nhistory <aantal kwartier>\noutside")
                await message.channel.send(embed=embed)
        else:
            data = get_data()
            embed = discord.Embed(title="Jens' Kamer: Actuele data", description="Wat voor nut had dit ook alweer?", colour=0x779bff)
            embed.set_footer(text="Jens de Ruiter", icon_url="https://cdn.discordapp.com/avatars/283554212019699722/6aef6a5e52d6420baf7d2a25274f562e.png?size=256")
            embed.add_field(name=f"{int(data['temperature'])}℃", value="Dit is de temperatuur op mijn kamer.")
            embed.add_field(name=f"{int(data['humidity'])}%", value="Dit is de luchtvochtigheid op mijn kamer.")
            await message.channel.send(embed=embed)

bot.run(config.TOKEN)