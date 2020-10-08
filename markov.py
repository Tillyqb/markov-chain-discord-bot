"""A Markov chain generator that can tweet random messages."""

import sys
from random import choice
import os
import discord
import secrets
# import battle_hymn

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # Open the file and turn it into one long string
    #input_text = open_and_read_file(input_path)
    input_text = open(file_path)
    string = ''
    for line in input_text:
        line = " ".join(line.split())
        string = f'{string} {line}'
        string = string.strip()
    input_text.close()
    return string

def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """
    
    chains = {}
    words = text_string.split(' ')
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
        words.append(word)
        word = choice(chains[key])
    
    return ' '.join(words)


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
# filenames = sys.argv[1:]

# Open the files and turn them into one long string
# text = open_and_read_file('battle_hymn.txt')

# Get a Markov chain
# chains = make_chains(text)
# 
# output_text = make_text(chains)

client = discord.Client()

def randomness():
    text = open_and_read_file('ToBe.txt')
    chains = make_chains(text)
    output_text = make_text(chains)
    if len(output_text) > 1990:
        return output_text
    return output_text


@client.event
async def on_ready():
    print(f'Successfully conected master! logged in as {client.user}')

# channel = discord.utils.get(client.get_channel("bot-party"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('bot'):
        await message.channel.send(randomness())

    # await message.channel.send(randomness('ToBe.txt'))



client.run(os.environ['DISCORD_TOKEN'])

#print(os.environ['DISCORD_TOKEN'])