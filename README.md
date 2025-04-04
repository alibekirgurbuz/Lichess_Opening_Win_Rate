
# ♟️ Lichess Açılış Analiz Aracı

Bu proje, bir **Lichess** kullanıcısının oynadığı satranç oyunlarını analiz ederek en çok kullandığı açılışları ve bu açılışlardaki kazanma oranlarını gösteren basit bir masaüstü uygulamasıdır. Python ve `Tkinter` kullanılarak geliştirilmiştir.

## 🚀 Özellikler

- Belirli bir kullanıcı adı için Lichess API üzerinden oyun geçmişi alınır
- Beyaz, siyah veya her iki taşla oynanan açılışlar analiz edilebilir
- En çok tercih edilen açılışlar ve bu açılışlardaki kazanma oranları listelenir
- Basit ve kullanıcı dostu bir grafik arayüz (GUI)

## 🖼️ Ekran Görüntüsü

> (Buraya bir ekran görüntüsü ekleyebilirsin)

## 🛠️ Kurulum

### Gereksinimler

- Python 3.8+
- İnternet bağlantısı (Lichess API erişimi için)

### Bağımlılıklar

Aşağıdaki modüllerin kurulu olması gerekir. Gerekirse şu komutla kurabilirsin:

```bash
pip install requests
```

### Çalıştırma

```bash
python LichessPlayerAnalysis.py
```

## 📊 Kullanım

1. Uygulamayı başlat.
2. Lichess kullanıcı adını gir.
3. Analiz etmek istediğin maksimum oyun sayısını belirt (varsayılan: 200).
4. Taş rengini seç (Beyaz, Siyah veya Her İki Renk).
5. "Analiz Et" butonuna tıkla.

Sonuçlar tablo olarak gösterilecektir:

| # | Açılış Adı | Oyun Sayısı | Kazanma Oranı |
|--|-------------|-------------|----------------|

## 📡 Lichess API Kullanımı

Uygulama, [Lichess API](https://lichess.org/api) üzerinden kullanıcı oyunlarını çeker. `application/x-ndjson` formatında stream edilen veriler işlenerek açılışlara göre analiz yapılır.

## ❗ Notlar

- Çok fazla oyun analiz etmeye çalışmak API sınırlarına takılabilir.
- Lichess hesabının açık olması gerekir (gizli hesaplar desteklenmez).

## 📄 Lisans

Bu proje açık kaynaklıdır. Dilediğin gibi kullanabilir, geliştirebilir veya katkıda bulunabilirsin.
