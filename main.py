import asyncio

import discord
from discord.ext import commands
import a2s
import steam
import requests
from steam import game_servers as gs

client = commands.Bot(command_prefix='g9.')

@client.event
async def on_ready():
    await client.change_presence(status= discord.Status.online, activity = discord.Game('g9.findpayers') )


def clear_name(name):
    for ch in ['^0','^1','^2','^3','^4','^5','^6','^7','^8','^9']:
        if ch in name:
            name = name.replace(ch,"")
    return name

def get_server_info(response_server_address): #получение информации о сервере
    players_sv = a2s.players(response_server_address,1.0)
    sv_info = a2s.info(response_server_address)
    list_of_players = []
    for player in players_sv:
        list_of_players.append([player.score, clear_name(player.name)])
    list_of_players.sort(reverse=True)
    server_ip = '{0[0]}:{0[1]}'.format(response_server_address)
    embed=discord.Embed(title=str("**%s** Map: %s Players: %i/%i IP:%s" % (sv_info.server_name, sv_info.map_name, sv_info.player_count, sv_info.max_players, server_ip)), color=0x1100ff)
    for row in list_of_players:
        embed.add_field(name = row[1], value = row[0], inline=True)
    return embed #возвращает ембед с названием сервера, его ип, картой и списком игроков

@client.command()
async def findplayers(ctx):
    Servercount = 0
    Playercount = 0
    Serversnotresp = 0
    Serversnotresplist = ""
    for server_addr in gs.query_master(r'\appid\70\gamedir\ag\empty\1', max_servers=100): #ищет все сервера где есть игроки
        try:
            Servercount += 1
            Playercount += a2s.info(server_addr).player_count
            await ctx.send(embed = get_server_info(server_addr))
        except OSError as err:
            server_ip = '{0[0]}:{0[1]}'.format(server_addr)
            Serversnotresplist += f"\n{server_ip}"
            Serversnotresp += 1
                #print(f"Network problem: {err}")
        except asyncio.TimeoutError:
            print("Operation timed out")
    if(Playercount!=0):
            await ctx.send(f"Total of {Playercount} players on {Servercount} servers")
    if(Serversnotresp!=0):
        await ctx.send(f"{Serversnotresp} servers aren't responding, but there are players there - {Serversnotresplist}")

    await ctx.send("**Bot invate link: https://discord.gg/sKrmadaTWJ **")
    await ctx.send("**Ag community server: https://discord.gg/nVP3NPZeqR **")


client.run('token')