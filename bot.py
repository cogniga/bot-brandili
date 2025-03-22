import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Carrega a planilha com nome da aba "Produtos"
df = pd.read_excel("produtos.xlsx", sheet_name="Produtos")
df.columns = df.columns.str.strip().str.lower()
df['codigo'] = df['codigo'].astype(str)

# Função principal para busca de códigos
async def buscar_codigos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.replace("/", "").strip()
    codigos = [codigo.strip() for codigo in texto.split(',') if codigo.strip()]
    
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

# Inicialização do bot
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("codigo", buscar_codigos))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_codigos))
app.run_polling()
