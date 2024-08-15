import discord
from discord.ext import commands
from views.mediator_views import MediatorConfigView, MediatorQueueView
from views.aposta_views import ApostaFilaView, GeloFilaView
from mediators.mediator_config import MediatorConfig
import config
import os

# Define as intenções do bot, incluindo o conteúdo das mensagens e membros
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Cria uma instância do bot com o prefixo '!' e as intenções definidas
bot = commands.Bot(command_prefix='!', intents=intents)

# Evento disparado quando o bot está pronto para ser usado
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Comando para adicionar um mediador
@bot.command()
async def mediador(ctx, id: int, nome: str):
    if ctx.author.guild_permissions.administrator:
        mediator = MediatorConfig()
        mediator.add_mediator(id, nome)
        await ctx.send(f"Mediador {nome} adicionado com sucesso!")
    else:
        await ctx.send("Você não tem permissão para executar este comando.")

# Comando para configurar o Pix do mediador
@bot.command()
@commands.has_permissions(administrator=True)
async def config_pix(ctx):
    view = MediatorConfigView()
    await ctx.send("Clique na opção abaixo para configurar o mediador.", view=view)

# Evento para salvar imagens enviadas como anexos
@bot.event
async def on_message(message):
    if message.attachments:
        attachment = message.attachments[0]
        file_path = os.path.join('images', 'mediador', attachment.filename)
        await attachment.save(file_path)
        await message.channel.send(f"Imagem {attachment.filename} salva com sucesso.")
    await bot.process_commands(message)

# Comando para exibir e interagir com a fila de mediadores
@bot.command()
@commands.has_permissions(administrator=True)
async def fila_mediador(ctx):
    view = MediatorQueueView()
    await ctx.send(embed=view.create_embed(), view=view)

# Comando para mostrar mediadores cadastrados
@bot.command()
async def mostrar_mediadores(ctx):
    mediator = MediatorConfig()
    mediators = mediator.get_mediators()
    if mediators:
        for m in mediators.values():
            embed = discord.Embed(
                title=f"{m['nome']}",
                description=f"Chave PIX: {m['chave_pix']}",
                color=0x00ff00
            )
            if m['qr_code_image']:
                file_path = m['qr_code_image']
                embed.set_image(url=f"attachment://{os.path.basename(file_path)}")
                await ctx.send(embed=embed, file=discord.File(file_path))
            else:
                await ctx.send(embed=embed)
    else:
        await ctx.send("Nenhum mediador cadastrado.")

# Comando para criar apostas
@bot.command()
async def aposta(ctx, tipo: str, valor: float):
    if tipo == '1x1':
        view = GeloFilaView(tipo, valor)
    else:
        view = ApostaFilaView(tipo, valor)
    await ctx.send(embed=view.create_embed(), view=view)

# Executa o bot usando o token definido no arquivo de configuração
bot.run(config.BOT_TOKEN)
