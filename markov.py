"""A Markov chain generator that can tweet random messages."""

import sys
from random import choice
import os
import discord
import secrets

def open_and_read_file(file_path):
    """Take file path as string; return text as string."""

    input_text = open(file_path)
    string = ''
    for line in input_text:
        line = " ".join(line.split())
        string = f'{string} {line}'
        string = string.strip()
    input_text.close()
    return string

def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains."""
    
    chains = {}
    words = text_string.split(' ')      #########
    words.append(None)
    for i in range(len(words)-2):
        key = (words[i], words[i+1])
        word = words[i+2]

        if key not in chains:
            chains[key] = []

        chains[key].append(word)


    return chains


def make_text(chains):
    """Return text from chains."""
    keys = list(chains.keys())
    random_start = choice(keys)

    words = [random_start[0], random_start[1]]
    key = (random_start[0], random_start[1])
    word = choice(chains[key])
    
    while word is not None:
        key = (key[1], word)
        words.append(word)                   ########original document was 
        word = choice(chains[key])           ########in the wrong order here.
        if len(' '.join(words)) > 1980:
            return ' '.join(words)           
    
    return ' '.join(words)


def randomness():
    text = open_and_read_file(choice(['ToBe.txt', 'battle_hymn.txt', 'green-eggs.txt', 'concerning-hobbits.txt']))
    chains = make_chains(text)
    output_text = make_text(chains)
    return output_text


client = discord.Client()

@client.event
async def on_ready():
    print(f'Successfully conected master! logged in as {client.user}')

# manually add files to the possibilities
# file_list = ['ToBe.txt', 'battle_hymn.txt']
# filename = choice(file_list)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('bot'):
        await message.channel.send(randomness())

# python markov.py green-eggs.txt shakespeare.txt
# filenames = sys.argv[1:]

client.run(os.environ['DISCORD_TOKEN'])

#print(os.environ['DISCORD_TOKEN'])