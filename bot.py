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

import requests
import random as rand
from bs4 import BeautifulSoup as bs
from itertools import permutations 

import nest_asyncio
import asyncio
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


################### Bot Commands  ######################


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Discord server! FAQ!'
    )

@bot.command(name='Fubuki_is_Cat', help='Responds with a random quote from Fubuki')
async def Fubuki_Cat(ctx):
    Fubuki_quotes = [
        'No no cat! I\'m Fox', 
        'Kitsune jyaa!', 
        'Nyaajyanee!'
    ]
    response = random.choice(Fubuki_quotes)
    await ctx.send(response)
    
    
@bot.command(name='dctdl', help='Returns SV Portal link from deckcode')
async def svcodetostatic(ctx, deck_code, lang='en', mode='u'):
    
    response = createlinkfromcode(deck_code, lang, mode)
    await ctx.send(response)
    
    
@bot.command(name='dbtdl', help='Turns SV builder links into static links')
async def svbuildtostatic(ctx, link, lang='en', mode='u'):

    response = createlinkfrombuilder(link, lang, mode)
    await ctx.send(response)


@bot.command(name='mull', help='Test out a mulligan')
async def openingmull(ctx, deck_code, lang='en', mode='u'):
    
    link = createlinkfromcode(deck_code, lang, mode)
    card_list = decklist(link)
       
    draw_count = 3
    
    while True:
        opening_hand = rand.sample(card_list,draw_count)
        description = f' 1. {opening_hand[0]}\n 2. {opening_hand[1]}\n 3. {opening_hand[2]}'
        response = discord.Embed(title="Opening_Hand", description = description, color=0xffb7c5)
        response.set_footer(text='Type card nos. to mull. (Type n if keep hand): ')
        await ctx.send(embed=response)
        
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        try:
            msg = await bot.wait_for("message", check=check, timeout=20)
            opening_hand = mulliganfunction(msg.content, card_list, opening_hand)
        except asyncio.TimeoutError:
            await ctx.send("Time's yp! FAQ! (Mulligan Ended)")
        
        description = f' 1. {opening_hand[0]}\n 2. {opening_hand[1]}\n 3. {opening_hand[2]}'
        response = discord.Embed(title="Final_Hand", description = description, color=0xffb7c5)
        response.set_footer(text='Try Again. (Type y if yes): ')
        await ctx.send(embed=response)
        
        try:
            msg = await bot.wait_for("message", check=check, timeout=10)
            if msg.content.lower() == "y":
                continue
            else:
                await ctx.send("Mulligan Ended")
                break
        except asyncio.TimeoutError:
            await ctx.send("Time's up! FAQ! (Mulligan Ended)")
            break


#################### Functions ######################


def createlinkfrombuilder(deck_builder_url, lang, mode):
    sv_format = {'R':'3', 'U':'1'}
    languages = ['en', 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es']            

    if 'shadowverse-portal.com/deckbuilder/create/' not in deck_builder_url:
        response = "Invalid link"
    elif mode.upper() not in sv_format:
        response = "Invalid deck format"
    elif lang.lower() not in languages:
        response = "Invalid language"
    else:      
        deck_hash = deck_builder_url.split("hash=")[1].split("&")[0]
        deck_hash = deck_hash.replace("1",str(sv_format[mode.upper()]),1)
        deck_list_url = "https://shadowverse-portal.com/deck/" + str(deck_hash) + "?lang=" + str(lang)
        #response = discord.Embed(title="Sample Embed", url=deck_list_url)
        response = deck_list_url
    return response


def createlinkfromcode(deck_code, lang, mode):
    sv_format = {'R':'3', 'U':'1'}
    languages = ['en', 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es']
    
    deck_code_url = "https://shadowverse-portal.com/api/v1/deck/import?format=json&deck_code=" + deck_code + "&lang=en"
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
    return response


def mullcards(card_list, opening_hand, card_to_mull):
    mull_count = len(card_to_mull)
    for num in range (1,len(opening_hand)+1):
        if num in card_to_mull:
            opening_hand[num-1] = 'Empty'
        else:
            card_list.remove(opening_hand[num-1])
        counter = 0
        
    mull_hand = rand.sample(card_list,mull_count)
    counter = 0
    
    for num in range (1,len(opening_hand)+1):
        if opening_hand[num-1] == 'Empty':
            opening_hand[num-1] = mull_hand[counter]
            counter += 1
    return opening_hand


def decklist(link):
    source = requests.get(link).text
    soup = bs(source, 'lxml')
    
    card_name = soup.find_all('span', class_="el-card-list-info-name-text")
    card_qty = soup.find_all('p', class_="el-card-list-info-count")

    card_list = []
    for unique_card in range(0,len(card_name)):
        for copies in range(0,int(card_qty[unique_card].text[1])):
            card_list.append(card_name[unique_card].text)
    
    return card_list


def mulliganfunction(mulligan, card_list, opening_hand):
    x = '123'
    if mulligan.lower() == 'n':
        pass
    elif mulligan in [''.join(j) for i in range(1,len(x) + 1) for j in  permutations(x, i)]:
        if mulligan == '1':
            card_to_mull = [1]
        elif mulligan == '2':
            card_to_mull = [2]
        elif mulligan == '3':
            card_to_mull = [3]
        elif mulligan in [''.join(p) for p in permutations('12')]:
            card_to_mull = [1,2]
        elif mulligan in [''.join(p) for p in permutations('23')]:
            card_to_mull = [2,3]
        elif mulligan in [''.join(p) for p in permutations('13')]:
            card_to_mull = [1,3]
        elif mulligan in [''.join(p) for p in permutations('123')]:
            card_to_mull = [1,2,3]
        opening_hand = mullcards(card_list, opening_hand, card_to_mull)
    
    return opening_hand
    
bot.run(TOKEN)
