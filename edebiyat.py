import sys
import random
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit,
    QVBoxLayout, QWidget, QMessageBox, QRadioButton, QButtonGroup, QHBoxLayout, QListWidget, QFormLayout, QDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# JSON dosya ismi
DOSYA_ADI = "yazarlar_kitaplar.json"

def yazarlar_kitaplar_yukle():
    """JSON dosyasından yazar ve kitapları yükler."""
    if os.path.exists(DOSYA_ADI):
        with open(DOSYA_ADI, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "Ahmet Hamdi Tanpınar": ["Huzur"],
        "Orhan Pamuk": ["Benim Adım Kırmızı", "Kar"],
        "Yusuf Atılgan": ["Anayurt Oteli"],
        "Yaşar Kemal": ["İnce Memed"],
        "Peyami Safa": ["Dokuzuncu Hariciye Koğuşu"],
        "Halide Edib Adıvar": ["Ateşten Gömlek"]
    }

def yazarlar_kitaplar_kaydet():
    """Yazar ve kitapları JSON dosyasına kaydeder."""
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        json.dump(yazarlar_kitaplar, f, ensure_ascii=False, indent=4)

# Türk edebiyatından yazarlar ve kitapları, uygulama başlarken dosyadan yüklenir
yazarlar_kitaplar = yazarlar_kitaplar_yukle()

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dogru_sayisi = 0
        self.yanlis_sayisi = 0
        self.onceki_soru = None  # Önceki soruyu saklamak için değişken
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Kitap ve Yazar Quiz")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.initWidgets()
        self.setCentralWidget(self.container)

    def initWidgets(self):
        self.layout = QVBoxLayout()

        self.layout_mod = QFormLayout()
        self.radio_kitap = QRadioButton("Kitap")
        self.radio_yazar = QRadioButton("Yazar")
        self.radio_kitap.setChecked(True)  # Varsayılan seçim
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_kitap)
        self.button_group.addButton(self.radio_yazar)
        self.layout_mod.addRow(QLabel("Mod Seçimi:"), self.radio_kitap)
        self.layout_mod.addRow("", self.radio_yazar)
        self.layout.addLayout(self.layout_mod)

        self.label_soru = QLabel("Rastgele bir kitap veya yazar seçmek için 'Sonraki Soru'ya tıklayın.")
        self.label_soru.setAlignment(Qt.AlignCenter)
        self.label_soru.setFont(QFont('Arial', 18))
        self.label_soru.setStyleSheet("color: #333;")
        self.layout.addWidget(self.label_soru)

        self.input_cvp = QLineEdit()
        self.input_cvp.setPlaceholderText("Cevabınızı buraya girin")
        self.input_cvp.setFont(QFont('Arial', 14))
        self.input_cvp.setStyleSheet("padding: 10px; border: 2px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.input_cvp)

        self.layout_buttons = QHBoxLayout()
        self.buton_gonder = QPushButton("Gönder")
        self.buton_gonder.setFont(QFont('Arial', 14))
        self.buton_gonder.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;")
        self.buton_gonder.clicked.connect(self.kontrol_et)
        self.buton_gonder.setEnabled(False)
        self.layout_buttons.addWidget(self.buton_gonder)

        self.buton_sonraki = QPushButton("Sonraki Soru")
        self.buton_sonraki.setFont(QFont('Arial', 14))
        self.buton_sonraki.setStyleSheet("background-color: #2196F3; color: white; border-radius: 10px; padding: 10px 20px;")
        self.buton_sonraki.clicked.connect(self.yeni_soru)
        self.layout_buttons.addWidget(self.buton_sonraki)

        self.buton_ekle = QPushButton("Yeni Kitap Ekle")
        self.buton_ekle.setFont(QFont('Arial', 14))
        self.buton_ekle.setStyleSheet("background-color: #f44336; color: white; border-radius: 10px; padding: 10px 20px;")
        self.buton_ekle.clicked.connect(self.kitap_ekle)
        self.layout_buttons.addWidget(self.buton_ekle)

        self.buton_yazar_ekle = QPushButton("Yeni Yazar Ekle")
        self.buton_yazar_ekle.setFont(QFont('Arial', 14))
        self.buton_yazar_ekle.setStyleSheet("background-color: #f44336; color: white; border-radius: 10px; padding: 10px 20px;")
        self.buton_yazar_ekle.clicked.connect(self.yazar_ekle)
        self.layout_buttons.addWidget(self.buton_yazar_ekle)

        self.layout.addLayout(self.layout_buttons)

        self.label_cikti = QLabel("")
        self.label_cikti.setAlignment(Qt.AlignCenter)
        self.label_cikti.setFont(QFont('Arial', 16))
        self.label_cikti.setStyleSheet("color: #333;")
        self.layout.addWidget(self.label_cikti)

        self.label_istatistik = QLabel(f"Doğru: {self.dogru_sayisi}, Yanlış: {self.yanlis_sayisi}")
        self.label_istatistik.setAlignment(Qt.AlignCenter)
        self.label_istatistik.setFont(QFont('Arial', 14))
        self.label_istatistik.setStyleSheet("color: #555;")
        self.layout.addWidget(self.label_istatistik)

        self.container = QWidget()
        self.container.setLayout(self.layout)

    def yeni_soru(self):
        self.label_cikti.setText("")
        self.input_cvp.clear()

        if self.radio_kitap.isChecked():
            self.soru_tipi = 'kitap'
            self.gosterilen = self.rastgele_soru([kitap for kitaplar in yazarlar_kitaplar.values() for kitap in kitaplar])
            self.label_soru.setText(f"Kitap: {self.gosterilen}\nYazarını yazın.")
        else:
            self.soru_tipi = 'yazar'
            self.gosterilen = self.rastgele_soru(list(yazarlar_kitaplar.keys()))
            self.label_soru.setText(f"Yazar: {self.gosterilen}\nKitaplarından birini yazın.")

        self.buton_gonder.setEnabled(True)

    def rastgele_soru(self, liste):
        yeni_soru = random.choice(liste)
        while yeni_soru == self.onceki_soru:
            yeni_soru = random.choice(liste)
        self.onceki_soru = yeni_soru
        return yeni_soru

    def kontrol_et(self):
        cevap = self.input_cvp.text().strip()
        if not cevap:
            QMessageBox.warning(self, "Boş Cevap", "Lütfen bir cevap girin.")
            return

        dogru = False
        if self.soru_tipi == 'kitap':
            dogru_yazar = next((yazar for yazar, kitaplar in yazarlar_kitaplar.items() if self.gosterilen in kitaplar), None)
            if dogru_yazar and cevap.lower() == dogru_yazar.lower():
                dogru = True
        elif self.soru_tipi == 'yazar':
            dogru_kitaplar = yazarlar_kitaplar.get(self.gosterilen, [])
            if cevap.lower() in map(str.lower, dogru_kitaplar):
                dogru = True

        if dogru:
            self.label_cikti.setText("Doğru!")
            self.dogru_sayisi += 1
        else:
            if self.soru_tipi == 'kitap':
                dogru_yazar = next((yazar for yazar, kitaplar in yazarlar_kitaplar.items() if self.gosterilen in kitaplar), "Bilinmiyor")
                self.label_cikti.setText(f"Yanlış! Doğru Cevap: {dogru_yazar}")
            else:
                dogru_kitaplar = ", ".join(yazarlar_kitaplar.get(self.gosterilen, []))
                self.label_cikti.setText(f"Yanlış! Doğru Cevaplar: {dogru_kitaplar}")
            self.yanlis_sayisi += 1

        self.guncelle_istatistik()

        self.buton_gonder.setEnabled(False)

    def kitap_ekle(self):
        self.window = QWidget()
        self.window.setWindowTitle("Yeni Kitap Ekle")
        self.window.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.list_yazarlar = QListWidget()
        for yazar in yazarlar_kitaplar:
            kitaplar = ", ".join(yazarlar_kitaplar[yazar])
            self.list_yazarlar.addItem(f"{yazar} - Kitapları: {kitaplar}")
        layout.addWidget(self.list_yazarlar)

        self.label_yeni_kitap = QLabel("Seçilen yazara eklenecek kitabı yazın:")
        layout.addWidget(self.label_yeni_kitap)
        self.input_yeni_kitap = QLineEdit()
        self.input_yeni_kitap.setFont(QFont('Arial', 14))
        self.input_yeni_kitap.setStyleSheet("padding: 5px; border: 2px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.input_yeni_kitap)

        self.buton_kitap_ekle = QPushButton("Kitap Ekle")
        self.buton_kitap_ekle.setFont(QFont('Arial', 14))
        self.buton_kitap_ekle.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;")
        self.buton_kitap_ekle.clicked.connect(self.kitap_ekle_islemi)
        layout.addWidget(self.buton_kitap_ekle)

        self.window.setLayout(layout)
        self.window.show()

    def kitap_ekle_islemi(self):
        selected_yazar = self.list_yazarlar.currentItem().text().split(" -")[0]
        yeni_kitap = self.input_yeni_kitap.text().strip()

        if not yeni_kitap:
            QMessageBox.warning(self.window, "Boş Kitap Adı", "Lütfen bir kitap adı girin.")
            return

        if selected_yazar in yazarlar_kitaplar:
            yazarlar_kitaplar[selected_yazar].append(yeni_kitap)
            QMessageBox.information(self.window, "Başarılı", f"{yeni_kitap} adlı kitap {selected_yazar} yazara eklendi.")
            yazarlar_kitaplar_kaydet()
        else:
            QMessageBox.warning(self.window, "Hata", "Bir hata oluştu.")

        self.window.close()

    def yazar_ekle(self):
        self.yazar_ekleme_penceresi = QDialog()
        self.yazar_ekleme_penceresi.setWindowTitle("Yeni Yazar Ekle")
        self.yazar_ekleme_penceresi.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label_yeni_yazar = QLabel("Yeni yazar adını girin:")
        layout.addWidget(self.label_yeni_yazar)

        self.input_yeni_yazar = QLineEdit()
        self.input_yeni_yazar.setFont(QFont('Arial', 14))
        self.input_yeni_yazar.setStyleSheet("padding: 5px; border: 2px solid #ccc; border-radius: 5px;")
        layout.addWidget(self.input_yeni_yazar)

        self.buton_yazar_ekle = QPushButton("Yazar Ekle")
        self.buton_yazar_ekle.setFont(QFont('Arial', 14))
        self.buton_yazar_ekle.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px 20px;")
        self.buton_yazar_ekle.clicked.connect(self.yazar_ekle_islemi)
        layout.addWidget(self.buton_yazar_ekle)

        self.yazar_ekleme_penceresi.setLayout(layout)
        self.yazar_ekleme_penceresi.exec_()

    def yazar_ekle_islemi(self):
        yeni_yazar = self.input_yeni_yazar.text().strip()

        if not yeni_yazar:
            QMessageBox.warning(self.yazar_ekleme_penceresi, "Boş Yazar Adı", "Lütfen bir yazar adı girin.")
            return

        if yeni_yazar not in yazarlar_kitaplar:
            yazarlar_kitaplar[yeni_yazar] = []
            QMessageBox.information(self.yazar_ekleme_penceresi, "Başarılı", f"{yeni_yazar} adlı yazar eklendi.")
            yazarlar_kitaplar_kaydet()
        else:
            QMessageBox.warning(self.yazar_ekleme_penceresi, "Yazar Mevcut", "Bu yazar zaten mevcut.")

        self.yazar_ekleme_penceresi.close()

    def guncelle_istatistik(self):
        self.label_istatistik.setText(f"Doğru: {self.dogru_sayisi}, Yanlış: {self.yanlis_sayisi}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
