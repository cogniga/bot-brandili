import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

# Carrega planilha de produtos
df_produtos = pd.read_excel("produtos.xlsx", sheet_name="Produtos")
df_produtos.columns = df_produtos.columns.str.strip().str.lower()
df_produtos['codigo'] = df_produtos['codigo'].astype(str)

# Carrega planilha de fotos
df_fotos = pd.read_excel("fotos.xlsx", sheet_name=0)
df_fotos.columns = df_fotos.columns.str.strip().str.lower()
df_fotos['codigo'] = df_fotos['codigo'].astype(str)

# Handler universal para processar códigos e enviar foto + info
async def buscar_precos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.replace("/", "").strip()
    codigos = [c.strip() for c in texto.split(",") if c.strip()]

    for codigo in codigos:
        produto = df_produtos[df_produtos['codigo'] == codigo]
        if produto.empty:
            await update.message.reply_text(f"Poxa, não encontramos o item com código {codigo}. Por favor, valide com o vendedor.")
            continue

        p = produto.iloc[0]
        nome = p['descricao']
        atacado = p['a']
        varejo = p['v']

        texto_mensagem = (
            f"Produto: {nome}\n"
            f"CODIGO: {codigo}\n"
            f"Preço atacado: R$ {atacado:.2f}\n"
            f"Preço varejo: R$ {varejo:.2f}"
        )

        foto = df_fotos[df_fotos['codigo'] == codigo]
        if not foto.empty:
            link_foto = foto.iloc[0]['linkdireto']
            await update.message.reply_photo(photo=link_foto, caption=texto_mensagem)
        else:
            await update.message.reply_text(texto_mensagem)

# Inicialização do bot
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
app = ApplicationBuilder().token(TOKEN).build()

# Captura comandos e mensagens diretas como /1234
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_precos))
app.add_handler(MessageHandler(filters.COMMAND, buscar_precos))

app.run_polling()
