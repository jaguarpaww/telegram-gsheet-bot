from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json  # Gunakan json, bukan eval

# Ganti dengan token dari BotFather
TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Setup akses Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Ambil kredensial dari environment variable dengan aman
creds_json = os.environ.get('GOOGLE_CREDS')
if not creds_json:
    raise Exception("❌ Environment variable GOOGLE_CREDS belum diset.")

creds_dict = json.loads(creds_json)  # ✅ Aman, tidak pakai eval
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Buka sheet
sheet = client.open("IP_Bot_Data").sheet1  # Ganti jika nama spreadsheet beda

# Fungsi untuk command /cek <ip> <slot>
def cek_physical(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        update.message.reply_text("❗ Gunakan format: /cek <ip-address> <slot>\nContoh: /cek 172.28.195.204 1")
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

    update.message.reply_text(response)

# Jalankan bot
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Tambahkan handler untuk command /cek
    dispatcher.add_handler(CommandHandler("cek", cek_physical))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
