# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 22:23:16 2020

@author: Potatsu
"""

# bot.py
import os
import random

import discord
from discord.ext import tasks, commands
from itertools import cycle
from dotenv import load_dotenv

import nest_asyncio
nest_asyncio.apply()

from flask import Flask
from threading import Thread
import urllib.request
import json

app = Flask('')


@app.route('/')
def main():
    return "Your Bot Is Ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!faq ', case_insensitive=True, intents=intents)
status = cycle(['with Python', 'MikoHub'])


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))



@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Discord server! FAQ!'
    )

@bot.command(name='Fubuki_is_Cat', help='Responds with a random quote from Fubuki')
async def Fubuki_Cat(ctx):
    Fubuki_quotes = [
        'No not cat! I\'m Fox', 'Kitsune jyaa!', 'Nyaa~'
    ]
    response = random.choice(Fubuki_quotes)
    await ctx.send(response)
    
@bot.command(name='deckcode', help='Returns SV Portal link from deckcode')
async def svdeckcode(ctx, code, mode='R', lang='en'):
    deck_code = code
    deck_code_url = "https://shadowverse-portal.com/api/v1/deck/import?format=json&deck_code=" + deck_code + "&lang=en"
    sv_format = {'R':'3', 'U':'1'}
    languages = ['en', 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es']
    
    with urllib.request.urlopen(deck_code_url) as response:
            source = response.read()
            
    deck_json = json.loads(source)
    if len(deck_json['data']['errors']) != 0:
        response = "Deck code invalid or does not exist"
    elif mode.upper() not in sv_format:
        response = "Invalid deck format"
    elif lang.lower() not in languages:
        response = "Invalid language"
    else:      
        deck_hash = deck_json['data']['hash']
        deck_hash = deck_hash.replace("1",str(sv_format[mode.upper()]),1)
        
        deck_list_url = "https://shadowverse-portal.com/deck/" + str(deck_hash) + "?lang=" + str(lang)
        response = deck_list_url
    await ctx.send(response)


bot.run(TOKEN)
