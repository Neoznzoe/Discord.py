from ast import keyword
from tkinter import ACTIVE
import discord

from discord.ext import commands
from pip import main 

class Node:
    def __init__(self, question, keyword, child_list_node):
        self.question = question
        self.keyword = keyword
        self.child_list_node = child_list_node

    def user_response(self):
        for child in self.child_list_node:
            txt = input()
            if child.keyword == txt:
                child.user_response()


main_node = Node("Hello !! Comment puis-je vous aider ?","help",
    [Node("Avez vous des problèmes avec les cours ou vous avez peut être besoin d'un bon tuto ?", "cours",
        [Node("Sur quels languages de programmation voulez qu'on vous propose ?","fichier",[
            Node("Vous trouverez toute la documentation sur Python https://devdocs.io/python~3.10/","python",[]),
            Node("Vous trouverez toute la documentation sur PHP https://www.php.net/manual/fr/intro-whatis.php","php",[]),
            Node("Vous trouverez toute la documentation sur JS https://developer.mozilla.org/fr/docs/Web/JavaScript","js",[]),
            Node("Vous trouverez toute la documentation sur HTML https://developer.mozilla.org/fr/docs/Web/HTML","html",[]),
            Node("Vous trouverez toute la documentation sur CSS https://developer.mozilla.org/fr/docs/Web/CSS","css",[])
        ]),
        Node("Sur quels languages de programmation voulez qu'on vous propose ?","video",[
            Node("Vous trouverez toute la documentation sur Python en vidéo sur https://www.youtube.com/watch?v=psaDHhZ0cPs&list=PLMS9Cy4Enq5JmIZtKE5OHJCI3jZfpASbR","python",[]),
            Node("Vous trouverez toute la documentation sur PHP en vidéo sur https://www.youtube.com/watch?v=cWoq5znh0vw&list=PLjwdMgw5TTLVDv-ceONHM_C19dPW1MAMD","php",[]),
            Node("Vous trouverez toute la documentation sur JS en vidéo sur https://www.youtube.com/watch?v=VZLflMqC6dI&list=PLwLsbqvBlImFB8AuT6ENIg-s87ys4yGWI","js",[]),
            Node("Vous trouverez toute la documentation sur HTML en vidéo sur https://www.youtube.com/watch?v=oEAuNzWXRjM&list=PLjwdMgw5TTLUeixVGPNl1uZNeJy4UY6qX","html",[]),
            Node("Vous trouverez toute la documentation sur CSS en vidéo sur https://www.youtube.com/watch?v=PE8FQ6zihhw&list=PLjwdMgw5TTLVjTZQocrMwKicV5wsZlRpj","css",[])
        ])
        ]),
        ])

bot = commands.Bot(command_prefix="!")
@bot.command()
async def clear(ctx):
  await ctx.channel.purge()

@bot.event
async def on_ready():
    print("Ready")


Actual_node = main_node

@bot.event
async def on_message(message):
    global Actual_node

    message.content = message.content.lower()

    Help_channel = bot.get_channel(978558222812201060)

    if message.content == "help":
        await Help_channel.send(Actual_node.question)

    for child in Actual_node.child_list_node:
        if child.keyword in message.content:
            await Help_channel.send(child.question)
            Actual_node = child
            return
    await bot.process_commands(message)




bot.run("OTc4MjI5MDg3NjY5NzQzNjQ2.GEAa_n.fDa3FmomiSf8irAuZAbAwG_dGmHf2ph6UDAmBo")

