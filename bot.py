import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os

# Carrega a planilha
df = pd.read_excel("produtos.xlsx", sheet_name="Produtos")
df.columns = df.columns.str.strip().str.lower()
df['codigo'] = df['codigo'].astype(str)

# Handler universal para processar os códigos
async def buscar_precos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.replace("/", "").strip()
    codigos = [c.strip() for c in texto.split(",") if c.strip()]

    respostas = []
    for codigo in codigos:
        resultado = df[df['codigo'] == codigo]
        if resultado.empty:
            respostas.append(f"Poxa, não encontramos o item com código {codigo}. Por favor, valide com o vendedor.")
        else:
            produto = resultado.iloc[0]
            nome = produto['descricao']
            atacado = produto['a']
            varejo = produto['v']
            respostas.append(
                f"Produto: {nome}\n"
                f"CODIGO: {codigo}\n"
                f"Preço atacado: R$ {atacado:.2f}\n"
                f"Preço varejo: R$ {varejo:.2f}"
            )

    await update.message.reply_text("\n\n".join(respostas))

# Inicializa o bot
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
app = ApplicationBuilder().token(TOKEN).build()

# Captura qualquer texto ou comando como /1234
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_precos))
app.add_handler(MessageHandler(filters.COMMAND, buscar_precos))  # inclusive comandos como /1234

app.run_polling()
