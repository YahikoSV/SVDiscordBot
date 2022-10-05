# -*- coding: utf-8 -*-
"""
Created on Mon May 30 14:24:23 2022

@author: Potatsu
"""
from email.message import Message
from lib2to3.pgen2.token import ASYNC
import discord
import random
import asyncio
from discord.ext import commands
import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint 


#Keys
Token = 'OTYzMTI2ODI5MDg0OTg3NDcz.YlRjwg.MonSFXQq5mcKQhttsN7QGfm1Vwo'
Giphy_api_key = 'P9qw4uhc7VMND8hIsV8RHResufNRvPsi'
youtube_API = 'AIzaSyA90DCPaxXxl_n9sn13Kmt9igVyLJFgqgI'
client = commands.Bot(command_prefix='!')
bunny_gifs = ['https://media.giphy.com/media/ejIRH33RxAJl9Aumdf/giphy.gif', 'https://media.giphy.com/media/J4D9ZWn4zQlvOWIpiq/giphy.gif']
suzumiya = ['Haruhi Time']
singing_gifs = ['https://media.giphy.com/media/BQwu1mSFrgSBSAAHrf/giphy.gif', 'https://media.giphy.com/media/QRC0qUZ7uxQVHRJNCS/giphy.gif']
sing = ['Lets sing']
party_gifs = ['https://media.giphy.com/media/HnS4Y64oonm3C/giphy.gif', 'https://media.giphy.com/media/QRC0qUZ7uxQVHRJNCS/giphy.gif']
dance = ['Lets Dance']
punch_gifs = ['https://media.giphy.com/media/1Bgr0VaRnx3pCZbaJa/giphy.gif', 'https://media.giphy.com/media/S8nGEQ0yR8z6M/giphy.gif', 'https://media.giphy.com/media/DuVRadBbaX6A8/giphy.gif']
punch = ['Fuck you']
playlist = ['https://youtube.com/playlist?list=PL8lZieNFgOdmrNGTqwjqYJpJ_2nw_O_M2', 'https://youtube.com/playlist?list=PLOpYIT5ND76ILBX-Yxpo34Doqs8IpQfVH']
DJ = ['listen to some tunes']
#list for responses 
Responses = ['Yes ', 'No', 'Maybe','Bad Idea', 'Good Idea', 'Reroll',"Go get isekai'd  "]

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

        def setup(client):
            client.add_Cog(music(client))

#Greeting in terminal
@client.event
async def on_ready():
    print('What is it {0.user}?'.format(client))
       
#command for asking questions
@client.command()
async def ask(ctx):
    username = str(ctx.author).split('#')[0]
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    try:
        await ctx.channel.send(f'What is your question {username} ?')
        question = await client.wait_for("message", check=check,timeout=30) 
        await ctx.channel.send(f'why are you asking this question {username} ?')
        reason = await client.wait_for("message", check=check,timeout=30) 
        await ctx.channel.send(random.choice(Responses))
    except asyncio.TimeoutError:
        await ctx.channel.send("Sorry, you didn't reply in time, !")

#command for where are people
@client.command()
async def where(ctx, user):
    await ctx.send(f'{user} doko?')

#commands for gifs
@client.command()
async def party(ctx):
    embed = discord.Embed(
        colour=(discord.Colour.random()),
        description = f'{ctx.author.mention} {(random.choice(dance))}'

    )
    embed.set_image(url=(random.choice(party_gifs)))

    await ctx.send(embed=embed)

@client.command()
async def singing(ctx, user : discord.Member):
    embed = discord.Embed(
        colour=(discord.Colour.random()),
        description = f'{user.mention} {(random.choice(sing))}'

    )
    embed.set_image(url=(random.choice(singing_gifs)))

    await ctx.send(embed=embed)

@client.command()
async def bunny(ctx, user : discord.Member):
    embed = discord.Embed(
        colour=(discord.Colour.random()),
        description = f'{user.mention} {(random.choice(suzumiya))}'

    )
    embed.set_image(url=(random.choice(bunny_gifs)))

    await ctx.send(embed=embed)

@client.command()
async def fight(ctx, user : discord.Member):
    embed = discord.Embed(
        colour=(discord.Colour.random()),
        description = f'{user.mention} {(random.choice(punch))}'

    )
    embed.set_image(url=(random.choice(punch_gifs)))

    await ctx.send(embed=embed)


#command for videos
@client.command()
async def DJ(ctx):
    embed = discord.Embed(
        colour=(discord.Colour.random()),
        description = f'{ctx.author.mention} {(random.choice(DJ))}'

    )
    embed.set_url(ctx.url==(random.choice(playlist)))

    await ctx.send(embed=embed)
    
client.run(Token)

client = commands.Bot(command_prefix="!")

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


client.run('AIzaSyA90DCPaxXxl_n9sn13Kmt9igVyLJFgqgI')