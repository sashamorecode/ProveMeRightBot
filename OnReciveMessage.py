import discord
from scholarly import scholarly, ProxyGenerator
import re
#need to load key seperatly becuse discord will detect if the api is on the web, just make a key.txt file and write the discord API key in it


with open('key.txt') as f:
    KEY = f.readline()
print(KEY)

pg = ProxyGenerator()
success = pg.FreeProxies()
scholarly.use_proxy(pg)

client = discord.Client()
tempDB = {}
NUM_ARTICLES= 3






@client.event
async def on_ready():
    print("ready to bring the truth")

@client.event
async def on_message(message):
    message.content = sanatize(message.content)

    if message.author == client.user:
        return
    if len(message.content.split(' ')) < 3:
        if message.content.split(' ')[0].lower() == 'cite':
            if 0 < int(message.content.split(' ')[1]) <= 4:
                if message.author not in tempDB.keys():
                    await message.author.send("You have no recently searched articles to source search an article with prove that and then cite it by its number eg. cite 1")
                    return
                else:
                    bib = scholarly.bibtex(tempDB[message.author][int(message.content.split(' ')[1])-1])
                    await message.author.send(str(bib))
            print(tempDB)
            print("t")

        return
    if (message.content.split(' ')[0] + message.content.split(' ')[1]).lower() == 'provethat':
        requestString = ""
        for word in message.content.split(' ')[2:]:
            requestString += word + " "
        print(requestString)
        if len(requestString) == 0:
            message.channel.send("request cannot be empty")
        try:
            search_query = scholarly.search_pubs(requestString)
            disc_res = ''
            a_all = []
            for x in range(NUM_ARTICLES):
                article = next(search_query)
                a_all.append(article)
                a_title = article['bib']['title']
                a_abstract = article['bib']['abstract']
                a_date = article['bib']['pub_year']
                a_auth = "".join([x + ', ' for x in article['bib']['author'] if x != ''])

                try:
                    a_link = article['eprint_url']
                except:
                    a_link = article['pub_url']
                disc_res += str(x + 1) + '. ' + a_title + " (" + a_date + ")\n\n" + 'Abstract: '+ a_abstract + '... ' + '\nAuthors: ' + a_auth + '\nLink: ' + a_link + '\n\n'

            tempDB[message.author] = a_all
        except:
            disc_res = "We encountered an error try removing special sybols or refomulating your question."

        await message.channel.send(disc_res)


    return




def sanatize(s):
    s = re.sub('\\\\', '', s)
    s = re.sub(r'([_^$%&#{}])', r'\\\1', s)
    s = re.sub(r'\~', r'\\~{}', s)
    return s

client.run(KEY)

