import os
import discord
import logging
import pandas as pd
from decouple import config

#Configurando o nível de log para INFO
logging.basicConfig(level=logging.INFO)

#Configurando as intenções do bot
intents = discord.Intents.default()
intents.message_content = True  # Permitir o acesso ao conteúdo da mensagem
client = discord.Client(intents=intents)
guild = discord.Guild

#Evento on_ready: Chamado quando o bot está pronto
@client.event
async def on_ready():
    print('Logado como: {0.user}'.format(client))
    await client.change_presence(activity=discord.Game('_scan help'))

#Evento on_message: Chamado sempre que uma mensagem é recebida
@client.event
async def on_message(message):
    #Se a mensagem for feita pelo bot, não analisar
    if message.author == client.user:
        return
    #Se não observar se a mensagem começa com o caracter de ativação Underline '_'
    elif message.content.startswith('_'):

        # Analisando o comando e seus parâmetros
        cmd = message.content.split()[0].replace("_","")
        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]

        # Se tiver a palavra scan, gerar o arquivo.
        if cmd == 'scan':

            data = pd.DataFrame(columns=['content', 'time', 'author'])

            # Adquirindo o canal através do comando do bot
            if len(message.channel_mentions) > 0:
                channel = message.channel_mentions[0]
            else:
                channel = message.channel

            # Adquirindo o número de mensagens a serem coletadas através do comando do bot
            if (len(message.content.split()) > 1 and len(message.channel_mentions) == 0) or len(message.content.split()) > 2:
                for parameter in parameters:
                    if parameter == "help":
                        # Enviando uma mensagem de ajuda
                        answer = discord.Embed(title="Formatação do Comando",
                                               description="""
                                               `_scan <canal> <numero_de_mensagens>`\n\n
                                                `<canal>`: **o canal que você deseja escanear**\n
                                                `<numero_de_mensagens>`: **o número de mensagens que você deseja escanear**\n\n
                                                *A ordem dos parâmetros não importa.*
                                                """,
                                               colour=0x1a7794) 
                        await message.channel.send(embed=answer)
                        return
                    elif parameter[0] != "<": # Os canais são delimitados por "<>" como strings
                        limit = int(parameter)
            else:
                limit = 100

            # Enviando uma mensagem informando que o arquivo de histórico de mensagens está sendo criado
            answer = discord.Embed(title="Criando o seu arquivo de histórico de mensagens",
                                   description="Por favor aguarde. O arquivo será enviado para você em um chat particular.",
                                   colour=0x1a7794) 

            await message.channel.send(embed=answer)

            # Função para verificar se uma mensagem é um comando
            def is_command (message):
                if len(msg.content) == 0:
                    return False
                elif msg.content.split()[0] == '_scan':
                    return True
                else:
                    return False

            data = pd.DataFrame(columns=['content', 'time', 'author'])
            
            # Coletando mensagens do canal
            async for msg in channel.history(limit=limit + 1000):
                if msg.author != client.user:
                    if not is_command(msg):
                        new_data = pd.DataFrame({'content': [msg.content],
                                                'time': [msg.created_at],
                                                'author': [msg.author.name]})
                        data = pd.concat([data, new_data], ignore_index=True)
                    if len(data) == limit:
                        break

            # Convertendo o dataframe pandas em um arquivo .csv e enviando-o para o usuário

            file_location = f"{str(channel.guild.id) + '_' + str(channel.id)}.csv" # Determinando nome e local do arquivo
            data.to_csv(file_location) # Salvando o arquivo como .csv usando o pandas

            answer = discord.Embed(title="Aqui está o seu arquivo .CSV",
                                   description=f"""\n\n`Server` : **{message.guild.name}**\n`Channel` : **{channel.name}**\n`Messages Read` : **{limit}**""",
                                   colour=0x1a7794) 
            # Enviando a resposta com o arquivo .csv anexado
            await message.author.send(embed=answer)
            await message.author.send(file=discord.File(file_location, filename='data.csv')) # Sending the file
            os.remove(file_location) # Excluindo o arquivo
            
# Iniciando o bot com o token obtido a partir de um arquivo de configuração
client.run(config('TOKEN'))