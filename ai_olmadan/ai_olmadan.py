import json
import random

# JSON veri tabanını al
with open('ai_olmadan/ai_olmadan_yk.json', 'r', encoding='utf-8') as veritabani:
    yazarkitap = json.load(veritabani)

# JSON verisini yazdır
print(yazarkitap)

# Yazarlara ve kitaplarına erişim
for yazar, kitaplar in yazarkitap.items():
    print(f"Yazar: {yazar}")
    for kitap in kitaplar:
        print(f"  Kitap: {kitap}")

#Soru Hazırlama
def rastgele_soru_uretme(kendi, liste):
    yeni_soru = random.choice(kendi, liste)
    while yeni_soru == kendi.onceki_soru:
            yeni_soru = random.choice(liste)
    kendi.onceki_soru = yeni_soru # Yeni bulunan ve aynı olmayan soruyu yeni soru olarak geri döndürme
    return yeni_soru

#Yeni Soru
def yeni_soru(kendi, yenisoru):
    if soru_tipi == 'kitap_sorma':
        kendi.gosterilen = kendi.rastgele_soru([kitap for kitaplar in yazarkitap.values() for kitap in kitaplar])
        kendi.label_soru.setText(f"{kendi.gosterilen} \n Kitabının yazarı kimdir?")
        print( yeni_soru )
    else:
        print()
        
##############
secim = 'a'

while secim != 'c':
    print (" \n Kitaptan yazar tahmin etmek için k yaziniz. \n Yazardan kitap tahmin etmek için y yaziniz. \n Güncel yazar, eser listesi için l. \n Çikiş için ise c. \n İstediğiniz işlem için uygun harfi yazin ve 'enter'e tiklayin:") # \n (k) \t / \t (y) \t /  (c) \n 
    secim = input()
    if secim == 'k':
        print("Kitap tahmin etme")
        soru_tipi = 'kitap_sorma'
    elif secim == 'y':
        print("Yazar Tahmin etme")
        soru_tipi = 'yazar_sorma'
    elif secim == 'l':
        print("Liste")
    elif secim == 'c':
        print ("İyi günler")
    else:
        print("Gerçersiz İşlem")