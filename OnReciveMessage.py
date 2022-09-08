import discord
import requests
client = discord.Client()
from scholarly import scholarly
import json

NUM_ARTICLES= 3

@client.event
async def on_ready():
    print("ready to bring the truth")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if len(message.content.split(' ')) < 3:
        return

    if (message.content.split(' ')[0] + message.content.split(' ')[1]).lower() == 'provethat':
        requestString = ""
        for word in message.content.split(' ')[2:]:
            requestString += word + " "
        print(requestString)
        search_query = scholarly.search_pubs(requestString)
        disc_res = ''
        for x in range(NUM_ARTICLES):
            article = next(search_query)
            print(article)
            a_title = article['bib']['title']
            a_abstract = article['bib']['abstract']
            a_date = article['bib']['pub_year']
            a_auth = "".join([x + ', ' for x in article['bib']['author'] if x != ''])

            try:
                a_link = article['eprint_url']
            except:
                a_link = article['pub_url']
            disc_res += str(x + 1) + '. ' + a_title + " (" + a_date + ")\n\n" + 'Abstract: '+ a_abstract + '... ' + '\nAuthors: ' + a_auth + '\nLink: ' + a_link + '\n\n'


        await message.channel.send(disc_res)






client.run("MTAxNzQzMjM2MDc0MjAzNTQ3Ng.GtpfN7.LgXmZl4Yh3lpYfQrVVr27PofAjinexrDR4gy78")

