# Nihai Çözüm: Her şeyi yakalayan evrensel dinleyici
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- DEĞİŞKENLER ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
KAYNAK_GRUP_ID = -4809397519
HEDEF_GRUP_ID = -4938013083
AYIRICI_SATIR = "⸻⸻⸻⸻⸻⸻"
ANAHTAR_KELIME = "8877"
# --- DEĞİŞKENLER SONU ---

def linkleri_temizle(metin: str) -> str:
    """Verilen metin içindeki linkleri temizler."""
    metin = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', metin)
    metin = re.sub(r'(https|http|ftp)://[a-zA-Z0-9./?=&_ -]+', '', metin)
    metin = re.sub(r'www\.[a-zA-Z0-9./?=&_ -]+', '', metin)
    metin = metin.replace('()', '').strip()
    return metin

async def universal_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Kaynak gruptaki HER TÜRLÜ aktiviteyi yakalar, metin içerenleri işler.
    Bu fonksiyon hem normal mesajları hem de kanal gönderilerini yakalayabilir.
    """
    mesaj_metni = ""
    guncelleme_tipi = "Bilinmeyen"

    # Gelen aktivitenin ne olduğunu anlamaya çalış ve metni çıkar
    if update.message and update.message.text:
        mesaj_metni = update.message.text
        guncelleme_tipi = "Normal Mesaj"
    elif update.channel_post and update.channel_post.text:
        mesaj_metni = update.channel_post.text
        guncelleme_tipi = "Kanal Gönderisi"

    # Eğer metin içeren bir aktivite değilse, hiçbir şey yapma
    if not mesaj_metni:
        return

    # Terminale ne yakaladığımızı yazalım
    print("\n" + "="*50)
    print(f"GÜNCELLEME YAKALANDI! TÜRÜ: {guncelleme_tipi}")
    print(f"Mesajın ilk satırı: {mesaj_metni.splitlines()[0]}")
    print("="*50)

    # Ana mantığı çalıştır
    if ANAHTAR_KELIME in mesaj_metni.splitlines()[0]:
        print(f"✔ KOŞUL SAĞLANDI: '{ANAHTAR_KELIME}' bulundu.")
        
        ayrac_index = mesaj_metni.find(AYIRICI_SATIR)
        gonderilecek_metin = mesaj_metni[:ayrac_index].strip() if ayrac_index != -1 else mesaj_metni.strip()
        gonderilecek_metin = linkleri_temizle(gonderilecek_metin)

        try:
            await context.bot.send_message(
                chat_id=HEDEF_GRUP_ID,
                text=gonderilecek_metin,
                disable_web_page_preview=True
            )
            print("✔ Mesaj başarıyla hedef gruba gönderildi.")
        except Exception as e:
            print(f"❌ HATA: Mesaj gönderilemedi: {e}")
    else:
        print("✖ KOŞUL SAĞLANMADI: Anahtar kelime bulunamadı.")

def main():
    print("Evrensel Bot başlatılıyor...")
    application = Application.builder().token(BOT_TOKEN).build()

    # Tek bir evrensel dinleyici ekliyoruz.
    # Bu dinleyici, kaynak gruptaki metin içeren HER ŞEYİ yakalar.
    application.add_handler(MessageHandler(filters.TEXT & filters.Chat(KAYNAK_GRUP_ID) & ~filters.COMMAND, universal_handler))

    print("Bot çalışıyor. Kaynak gruptaki tüm metin aktiviteleri dinleniyor...")
    application.run_polling()

if __name__ == '__main__':
    main()



