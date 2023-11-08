import io
import discord
import psycopg2
from discord.ext import commands
from app import db_config

# Token do seu bot do Discord
TOKEN = "TOKEN_BOT"

# Criar um objeto intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# Criar um bot com um prefixo de comando
bot = commands.Bot(command_prefix="/", intents=intents)


# Comando para obter dados do banco e enviá-los para o Discord
@bot.command(name="dados")
async def obter_dados(ctx):
    # Verificar o conteúdo da mensagem
    if ctx.message.content != "/dados":
        await ctx.send("Comando inválido. Digite /dados para obter os dados.")

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Consulta SQL para obter os dados desejados, incluindo a imagem
    cursor.execute(
        "SELECT quantity, observation, code, price, description, category, photo FROM data"
    )
    data = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    if data:
        for datas in data:
            (
                quantity,
                observation,
                code,
                price,
                description,
                category,
                photo,
            ) = datas
            response = f"**Descrição:** {description}\n**Preço:** {price}\n**Quantidade:** {quantity}\n**Código:** {code}\n**Categoria:** {category}\n**Observação:** {observation}\n"

            await ctx.send("----------------------------------------")

            # Enviar a mensagem de resposta para o canal do Discord
            await ctx.send(response)

            # Enviar a imagem como arquivo anexo
            if photo:
                await ctx.send(
                    file=discord.File(io.BytesIO(photo), filename="imagem.png")
                )

    else:
        await ctx.send("Nenhum dado cadastrado.")


# Iniciar o bot com o token
bot.run(TOKEN)
