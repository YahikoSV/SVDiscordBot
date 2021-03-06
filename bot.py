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
    
    response, valid_input = createlinkfromcode(deck_code, lang, mode)
    await ctx.send(response)
    
    
@bot.command(name='dbtdl', help='Turns SV builder links into static links')
async def svbuildtostatic(ctx, link, lang='en', mode='u'):

    response, valid_input = createlinkfrombuilder(link, lang, mode)
    await ctx.send(response)


@bot.command(name='mull', help='Test out a mulligan')
async def openingmull(ctx, deck_code, lang='en', mode='u'):
    
    response, valid_input = createlinkfromcode(deck_code, lang, mode)
    
    if valid_input == False:
            await ctx.send(response)
    else:
       
        card_list = decklist(response)     
        draw_count = 3
        time_out = False
        while time_out == False:
            author = ctx.author.name
            txt_response =  f"**{author}**, choose cards that you want to mulligan."
            await ctx.send(txt_response)
            opening_hand = rand.sample(card_list,draw_count)
            description = f' Ooo {opening_hand[0]}\n \
                             oOo {opening_hand[1]}\n \
                             ooO {opening_hand[2]}'
                             
            embed_response = discord.Embed(title="Opening Hand", description = description, color=0xffb7c5)
            embed_response.set_footer(text='x = mull, o = keep (eg. xox, oxx, ooo)')
            await ctx.send(embed=embed_response) 
    
            
            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            
            valid_mull = False
            while valid_mull == False:
                try:
                    msg = await bot.wait_for("message", check=check, timeout=60)
                    opening_hand, valid_mull = mulliganfunction(ctx, msg.content, card_list, opening_hand, valid_mull)
                except asyncio.TimeoutError:
                    await ctx.send(f"**{author}**, Time's yp! FAQ! (Mulligan Ended)")
                    valid_mull = True
                    time_out = True
                
                if valid_mull == False:
                    await ctx.send(f"**{author}**, Invalid Mulligan please enter a valid mulligan (eg. oxo, xoo, xxx)")
                
            if time_out == False:
                description = f' {opening_hand[0]}\n \
                                 {opening_hand[1]}\n \
                                 {opening_hand[2]}'
                embed_response = discord.Embed(title="Final Hand", description = description, color=0x92ddf7)
                embed_response.set_footer(text='Try Again? (Enter y if yes): ')
                await ctx.send(embed=embed_response)
                
                try:
                    msg = await bot.wait_for("message", check=check, timeout=10)
                    if msg.content.lower() == "y":
                        continue
                    else:
                        await ctx.send(f"**{author}**, Mulligan Ended")
                        break
                except asyncio.TimeoutError:
                    await ctx.send(f"**{author}**, Time's up! FAQ! (Mulligan Ended)")
                    break

bot.remove_command('help')            
@bot.command(name='help')
async def help(ctx):
    
    author = ctx.message.author
    
    embed1 = discord.Embed(color = discord.Color.orange())
    embed1.set_author(name='SV FAQ Bot Commands \n')
    embed1.add_field(name="__dctdl <deck_code> <language> <mode>__",
                    value="Transforms deck code into SV Portal link. \n\n \
                    Inputs: \n \
                    deck_code: 4 character deck_code \n \
                    language: Options: {'en'(default), 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es'}  \n \
                    mode: Rotation, Unlimited {'r', 'u' (default)} \n\n",
                    inline=False
                    )
        
    embed1.add_field(name="__dbtdl <builder_link> <language> <mode>__",
                    value="Transforms deck builder link into SV Portal link. \n\n \
                    Inputs: \n \
                    builder_link: Deck builder link from SV Portal \n \
                    language: Options: {'en'(default), 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es'}  \n \
                    mode: Rotation, Unlimited {'r', 'u' (default)} \n\n",
                    inline=False
                    )
        
    embed1.add_field(name="__mull <builder_link> <language> <mode>__",
                    value="Simulates Mulligan with the given deck code. \n\n \
                    Inputs: \n \
                    deck_code: 4 character deck_code \n \
                    language: Options: {'en'(default), 'ja', 'ko', 'zh-tw' , 'fr', 'it', 'de', 'es'}  \n \
                    mode: Rotation, Unlimited {'r', 'u' (default)} \n\n \
                    Choose which cards you want to mull based on their positions with...\n \
                    x: Mull card, o: Keep card (e.g. xxo, oxo) \n\n",
                    inline=False
                    )    
    
    embed2 = discord.Embed(color = discord.Color.blue())
    embed2.set_author(name='Other Commands (for testing) \n')
    embed2.add_field(name="__Fubuki_Cat__",
                    value="Responses with a random quote of what Fubuki would say \n \
                          Try out what quote you got hehehe",
                    inline=False
                    )
    
    
        
    
    await author.send(embed=embed1)
    await author.send(embed=embed2)


# @bot.event
# async def on_message(message):
#     # No infinite bot loops
#     if message.author == bot.user or message.author.bot:
#         return

#     if message.content == 'great':
#         mention = message.author.mention
#         response = f"hey {mention}, you're great!"
#         await message.channel.send(response)

# @bot.event
# async def on_message2(message):
#     if message.content.startswith('$greet'):
#         channel = message.channel
#         await channel.send('Say hello!')

#         def check(m):
#             return m.content == 'hello' and m.channel == channel

#         msg = await bot.wait_for('message', check=check)
#         await channel.send('Hello {.author}!'.format(msg))
        
@bot.command(name='greet')
async def on_message3(ctx):
    # No infinite bot loops
    if ctx.author == bot.user or ctx.author.bot:
        return

    mention = ctx.author.name
    response = f"hey {mention}, you're great!"
    await ctx.channel.send(response)
#################### Functions ######################


def createlinkfrombuilder(deck_builder_url, lang, mode, valid_input = False):
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
        valid_input = True
    return response, valid_input


def createlinkfromcode(deck_code, lang, mode, valid_input = False):
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
        valid_input = True
    return response, valid_input 


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
    card_cost = soup.select('i[class*="icon-cost is-cost-"]')
    card_stats = soup.find_all('a', class_="el-icon-search is-small tooltipify")
    card_atk = [card['data-card-atk'] for card in card_stats]
    card_def = [card['data-card-life'] for card in card_stats]
    card_type = [card['data-card-char-type'] for card in card_stats]
    
    card_info = []
    for card in range (0,len(card_type)):
        if card_type[card] == '1': #follower
            card_info.append(f'{card_cost[card].text}pp {card_atk[card]}/{card_def[card]}')
        elif card_type[card] == '3': #amulet
            card_info.append(f'{card_cost[card].text}pp Amulet')
        elif card_type[card] == '4': #spell
            card_info.append(f'{card_cost[card].text}pp Spell')
    
    card_list = []
    for unique_card in range(0,len(card_name)):

        for copies in range(0,int(card_qty[unique_card].text[1])):
            card_list.append(f'{card_name[unique_card].text} ({card_info[unique_card]})')
            
    
    return card_list


# def mulliganfunction(mulligan, card_list, opening_hand):
#     x = '123'
#     if mulligan.lower() == 'n':
#         pass
#     elif mulligan in [''.join(j) for i in range(1,len(x) + 1) for j in  permutations(x, i)]:
#         if mulligan == '1':
#             card_to_mull = [1]
#         elif mulligan == '2':
#             card_to_mull = [2]
#         elif mulligan == '3':
#             card_to_mull = [3]
#         elif mulligan in [''.join(p) for p in permutations('12')]:
#             card_to_mull = [1,2]
#         elif mulligan in [''.join(p) for p in permutations('23')]:
#             card_to_mull = [2,3]
#         elif mulligan in [''.join(p) for p in permutations('13')]:
#             card_to_mull = [1,3]
#         elif mulligan in [''.join(p) for p in permutations('123')]:
#             card_to_mull = [1,2,3]
#         opening_hand = mullcards(card_list, opening_hand, card_to_mull)
    
#     return opening_hand

def mulliganfunction(ctx, mulligan, card_list, opening_hand, valid_mull):
    answer = 'oooxxx'
    if mulligan.lower() not in set([''.join(p) for p in permutations(answer,3)]):
        pass
    else:
        card_to_mull = [card + 1 for card in range (0,len(mulligan)) if mulligan[card] == 'x']
        opening_hand = mullcards(card_list, opening_hand, card_to_mull)
        valid_mull = True
        
    return opening_hand, valid_mull

    
    
bot.run(TOKEN)
