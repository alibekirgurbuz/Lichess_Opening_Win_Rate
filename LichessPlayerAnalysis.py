import requests
import json
from collections import Counter
import tkinter as tk
from tkinter import ttk, messagebox, StringVar

def en_cok_oynanan_acilislar(kullanici_adi, renk="both", limit=5, max_oyun=200):
    # Lichess API endpoint'i
    url = f"https://lichess.org/api/games/user/{kullanici_adi}"
    
    # API isteği için başlıklar ve parametreler
    headers = {
        "Accept": "application/x-ndjson"
    }
    params = {
        "max": max_oyun,  # Maksimum oyun sayısını sınırla
        "opening": "true"  # Sadece açılış bilgisi olan oyunları getir
    }
    
    # API'den oyunları al
    try:
        response = requests.get(url, headers=headers, params=params, stream=True)
        if response.status_code != 200:
            return None, f"Hata: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Bağlantı hatası: {str(e)}"
    
    # Açılışları saklamak için veri yapısı
    acilislar = {}  # {açılış_adı: {"toplam": 0, "kazanma": 0}}
    
    # Her bir oyunu işle
    oyun_sayisi = 0
    for line in response.iter_lines():
        if line:
            try:
                oyun = json.loads(line.decode('utf-8'))
                if "opening" in oyun and "players" in oyun and "status" in oyun:
                    acilis_adi = oyun["opening"]["name"]
                    
                    # Kullanıcının hangi renk olduğunu belirle
                    beyaz_oyuncu = oyun["players"]["white"]
                    siyah_oyuncu = oyun["players"]["black"]
                    
                    kullanici_beyaz = beyaz_oyuncu.get("user", {}).get("name", "").lower() == kullanici_adi.lower()
                    kullanici_siyah = siyah_oyuncu.get("user", {}).get("name", "").lower() == kullanici_adi.lower()
                    
                    # Renk filtreleme
                    if (renk == "white" and not kullanici_beyaz) or (renk == "black" and not kullanici_siyah):
                        continue
                    
                    # Renk bilgisini açılış adına ekle
                    renk_bilgisi = "Beyaz" if kullanici_beyaz else "Siyah"
                    tam_acilis_adi = f"{acilis_adi} ({renk_bilgisi})"
                    
                    # Açılışı takip et
                    if tam_acilis_adi not in acilislar:
                        acilislar[tam_acilis_adi] = {"toplam": 0, "kazanma": 0}
                    
                    acilislar[tam_acilis_adi]["toplam"] += 1
                    
                    # Kazanma durumu kontrol et
                    if "winner" in oyun:
                        kullanici_kazandi = (oyun["winner"] == "white" and kullanici_beyaz) or (oyun["winner"] == "black" and kullanici_siyah)
                        if kullanici_kazandi:
                            acilislar[tam_acilis_adi]["kazanma"] += 1
                
                oyun_sayisi += 1
                if oyun_sayisi >= max_oyun:
                    break
            except Exception as e:
                continue
    
    # Açılışları toplam oyuna göre sırala
    acilis_listesi = []
    for acilis, istatistik in acilislar.items():
        toplam = istatistik["toplam"]
        kazanma = istatistik["kazanma"]
        kazanma_orani = (kazanma / toplam * 100) if toplam > 0 else 0
        acilis_listesi.append((acilis, toplam, kazanma_orani))
    
    # En çok oynanan açılışları al
    en_cok_oynananlar = sorted(acilis_listesi, key=lambda x: x[1], reverse=True)[:limit]
    
    return en_cok_oynananlar, None

def analiz_yap():
    kullanici_adi = kullanici_adi_entry.get().strip()
    if not kullanici_adi:
        messagebox.showerror("Hata", "Lütfen bir kullanıcı adı girin.")
        return
    
    # Oyun sayısını al
    try:
        oyun_sayisi = int(oyun_sayisi_entry.get().strip())
        if oyun_sayisi <= 0:
            messagebox.showerror("Hata", "Oyun sayısı pozitif bir sayı olmalıdır.")
            return
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin.")
        return
    
    # Seçilen rengi al
    secilen_renk = renk_secimi.get()
    
    # Analiz düğmesini devre dışı bırak ve durumu güncelle
    analiz_btn.config(state="disabled")
    durum_label.config(text="Analiz yapılıyor...")
    root.update()
    
    # Sonuçları temizle
    for i in tree.get_children():
        tree.delete(i)
    
    # Analizi yap
    sonuclar, hata = en_cok_oynanan_acilislar(kullanici_adi, renk=secilen_renk, max_oyun=oyun_sayisi)
    
    # Analiz düğmesini tekrar etkinleştir
    analiz_btn.config(state="normal")
    
    if hata:
        durum_label.config(text=f"Hata: {hata}")
        return
    
    if not sonuclar:
        renk_metin = "beyaz taşlarla" if secilen_renk == "white" else "siyah taşlarla" if secilen_renk == "black" else ""
        durum_label.config(text=f"{kullanici_adi} için {renk_metin} oynanan açılış bulunamadı.")
        return
    
    # Sonuçları tabloya ekle
    for i, (acilis, sayi, oran) in enumerate(sonuclar, 1):
        tree.insert("", "end", values=(i, acilis, sayi, f"%{oran:.1f}"))
    
    renk_metin = "beyaz ve siyah taşlarla" if secilen_renk == "both" else "beyaz taşlarla" if secilen_renk == "white" else "siyah taşlarla"
    durum_label.config(text=f"{kullanici_adi} kullanıcısının {renk_metin} en çok oynadığı {len(sonuclar)} açılış listelendi.")

# Ana uygulama penceresi
root = tk.Tk()
root.title("Lichess Açılış Analizi")
root.geometry("700x500")
root.resizable(True, True)

# Ana çerçeve
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

# Kullanıcı adı giriş alanı
input_frame = ttk.Frame(main_frame)
input_frame.pack(fill="x", pady=(0, 10))

ttk.Label(input_frame, text="Lichess Kullanıcı Adı:").pack(side="left", padx=(0, 10))
kullanici_adi_entry = ttk.Entry(input_frame, width=30)
kullanici_adi_entry.pack(side="left", padx=(0, 10))
kullanici_adi_entry.focus()

# Oyun sayısı giriş alanı
ttk.Label(input_frame, text="Analiz Edilecek Oyun Sayısı:").pack(side="left", padx=(0, 10))
oyun_sayisi_entry = ttk.Entry(input_frame, width=10)
oyun_sayisi_entry.pack(side="left", padx=(0, 10))
oyun_sayisi_entry.insert(0, "200")  # Varsayılan değer

# İkinci frame - renk seçimi için
input_frame2 = ttk.Frame(main_frame)
input_frame2.pack(fill="x", pady=(0, 20))

# Renk seçimi
ttk.Label(input_frame2, text="Taş Rengi:").pack(side="left", padx=(0, 10))
renk_secimi = StringVar(value="both")
ttk.Radiobutton(input_frame2, text="Her İki Renk", variable=renk_secimi, value="both").pack(side="left", padx=(0, 10))
ttk.Radiobutton(input_frame2, text="Beyaz", variable=renk_secimi, value="white").pack(side="left", padx=(0, 10))
ttk.Radiobutton(input_frame2, text="Siyah", variable=renk_secimi, value="black").pack(side="left", padx=(0, 10))

# Analiz butonu
analiz_btn = ttk.Button(input_frame2, text="Analiz Et", command=analiz_yap)
analiz_btn.pack(side="left", padx=(10, 0))

# Durum çubuğu
durum_label = ttk.Label(main_frame, text="Kullanıcı adı girin, taş rengini seçin ve 'Analiz Et' düğmesine tıklayın.")
durum_label.pack(fill="x", pady=(0, 10))

# Sonuç tablosu
columns = ("sira", "acilis", "sayi", "kazanma_orani")
tree = ttk.Treeview(main_frame, columns=columns, show="headings")

# Sütun başlıkları
tree.heading("sira", text="#")
tree.heading("acilis", text="Açılış Adı")
tree.heading("sayi", text="Oyun Sayısı")
tree.heading("kazanma_orani", text="Kazanma Oranı")

# Sütun genişlikleri
tree.column("sira", width=30, anchor="center")
tree.column("acilis", width=350, anchor="w")
tree.column("sayi", width=100, anchor="center")
tree.column("kazanma_orani", width=100, anchor="center")

# Ağacı paketleme
tree.pack(fill="both", expand=True)

# Kaydırma çubuğu
scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Varsayılan olarak enter tuşunu analiz işlemine bağla
root.bind('<Return>', lambda event: analiz_yap())

# Uygulamayı başlat
root.mainloop()