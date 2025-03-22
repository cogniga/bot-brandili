import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

df = pd.read_excel("produtos.xlsx", sheet_name="Produtos")
df['codigo'] = df['codigo'].astype(str)

async def buscar_preco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /codigo <código do produto>")
        return

    codigo = context.args[0]
    resultado = df[df['codigo'] == codigo]

    if resultado.empty:
        await update.message.reply_text(f"Código {codigo} não encontrado.")
    else:
        nome = resultado.iloc[0]['descricao']
        preco = resultado.iloc[0]['preco']
        await update.message.reply_text(f"Produto: {nome}\nPreço: R$ {preco:.2f}")

# Token do bot vindo do Railway (como variável de ambiente)
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("codigo", buscar_preco))
app.run_polling()
