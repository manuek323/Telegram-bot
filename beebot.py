from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from io import BytesIO
import logging

# Desenvolvido por: Bee Solutions
# Autor: Fernando Almondes
# Data: 20/06/2025 22:10

from decouple import Config, RepositoryEnv

#env_path = '/opt/bee/beebot/.env'
env_path = '.env'
config = Config(RepositoryEnv(env_path))

TOKEN_BOT = config('TELEGRAM_TOKEN_BOT') # Chatid que pode requisitar no Beebot
CHAT_ID = config('TELEGRAM_CHAT_ID')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

from consulta_grafana import gera_img, consulta_lista_dashboards
        
async def dash(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(CHAT_ID) == str(update.effective_chat.id):

        if not context.args:
            await update.message.reply_text('--> Use: /dash uid')
            return
        
        await update.message.reply_text('--> Executando, por favor aguarde...')

        argumentos = " ".join(context.args)
        
        args = argumentos.split(' ')

        resultado = ''

        try:
            uid = args[0] # UID do Dashboard
            resultado = gera_img(uid=uid)
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='--> Argumentos invalidos ou erro na consulta!')
            return

        if resultado:
            # Criando um arquivo como imagem na memoria e enviando como anexo
            file = BytesIO(resultado)
            file.name = f'beebot-{uid}.png'
            await context.bot.send_photo(chat_id=update.effective_chat.id, caption=f'Relatorio Beebot - ({uid})', photo=file)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='--> Erro ao consultar informações!')
            return
        
async def dashs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(CHAT_ID) == str(update.effective_chat.id):

        #if not context.args:
        #    await update.message.reply_text('--> Use: /dashs')
        #    return
        
        await update.message.reply_text('--> Executando, por favor aguarde...')

        resultado = ''

        try:
            resultado = consulta_lista_dashboards()
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='--> Argumentos invalidos ou erro na consulta!')
            return
        if resultado:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'--> *Lista de Dashboards*:\n\n{resultado}*Relatorio Beebot - Grafana*', parse_mode='Markdown')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='--> Erro ao consultar informações!')
            return

async def chatid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #if str(CHAT_ID) == str(update.effective_chat.id):
    await update.message.reply_text(f'{update.effective_chat.id}')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menu = f'''*Olá {update.effective_user.first_name}, esse é o Beebot 🤖*!\n
--> *Lista de comandos*:\n
/*help* - Informações sobre o que o Beebot pode fazer!
/*chatid* - Verificar ChatID!
/*dashs* - Verificar lista de Dashboards do Grafana!
/*dash* uid - Receber gráfico de um Dashboard do Grafana!
\n*Desenvolvido por: Bee Solutions*
'''
    if str(CHAT_ID) == str(update.effective_chat.id):
        await update.message.reply_text(f'{menu}', parse_mode="Markdown")

app = ApplicationBuilder().token(TOKEN_BOT).build()

app.add_handler(CommandHandler("help", help))

app.add_handler(CommandHandler("chatid", chatid))

app.add_handler(CommandHandler(f'dash', dash))

app.add_handler(CommandHandler(f'dashs', dashs))

app.run_polling()