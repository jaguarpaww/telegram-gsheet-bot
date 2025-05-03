import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ambil token dari Environment Variable
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# Ambil GOOGLE_CREDS dari Environment Variable dan parsing jadi dict
google_creds_json = os.environ.get("GOOGLE_CREDS")
creds_dict = json.loads(google_creds_json)

# Setup akses Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("IP_Bot_Data").sheet1  # Ganti dengan nama spreadsheet Anda

# Fungsi untuk command /cek <ip> <slot>
async def cek_physical(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❗ Gunakan format: /cek <ip-address> <slot>\nContoh: /cek 172.28.195.204 1")
        return

    ip_dicari = context.args[0]
    slot_dicari = context.args[1]
    data = sheet.get_all_records()
    hasil = []

    for row in data:
        if str(row.get("IP")) == ip_dicari and str(row.get("SLOT")) == slot_dicari:
            physical = row.get("PHYSICAL", "N/A")
            hasil.append(f"- {physical}")

    if hasil:
        response = f"📦 PHYSICAL untuk IP {ip_dicari} dan SLOT {slot_dicari}:\n" + "\n".join(hasil)
    else:
        response = f"❌ Tidak ditemukan data untuk IP {ip_dicari} dengan SLOT {slot_dicari}."

    await update.message.reply_text(response)

# Jalankan bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("cek", cek_physical))
    app.run_polling()
