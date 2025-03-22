import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Lê a planilha e padroniza colunas
df = pd.read_excel("produtos.xlsx", sheet_name="Produtos")
df.columns = df.columns.str.strip().str.lower()
df['codigo'] = df['codigo'].astype(str)

# Handler que espera o código como argumento
async def buscar_preco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /codigo <código do produto>")
        return

    codigo = context.args[0]
    resultado = df[df['codigo'] == codigo]

    if resultado.empty:
        await update.message.reply_text(f"Poxa, não encontramos o item com código {codigo}. Por favor, valide com o vendedor.")
    else:
        nome = resultado.iloc[0]['descricao']
        atacado = resultado.iloc[0]['a']
        varejo = resultado.iloc[0]['v']
        await update.message.reply_text(
            f"Produto: {nome}\n"
            f"CODIGO: {codigo}\n"
            f"Preço atacado: R$ {atacado:.2f}\n"
            f"Preço varejo: R$ {varejo:.2f}"
        )

# Inicialização
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("codigo", buscar_preco))
app.run_polling()
