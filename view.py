# view.py

import tkinter as tk
from tkinter import ttk, messagebox, StringVar


class LichessAnalyzerView:
    def __init__(self, root, on_analyze_callback):
        self.root = root
        self.root.title("Lichess Açılış Analizi")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        self.on_analyze_callback = on_analyze_callback

        self._setup_ui()

    def _setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(input_frame, text="Lichess Kullanıcı Adı:").pack(side="left", padx=(0, 10))
        self.kullanici_adi_entry = ttk.Entry(input_frame, width=30)
        self.kullanici_adi_entry.pack(side="left", padx=(0, 10))
        self.kullanici_adi_entry.focus()

        ttk.Label(input_frame, text="Analiz Edilecek Oyun Sayısı:").pack(side="left", padx=(0, 10))
        self.oyun_sayisi_entry = ttk.Entry(input_frame, width=10)
        self.oyun_sayisi_entry.pack(side="left", padx=(0, 10))
        self.oyun_sayisi_entry.insert(0, "200")

        input_frame2 = ttk.Frame(main_frame)
        input_frame2.pack(fill="x", pady=(0, 20))

        ttk.Label(input_frame2, text="Taş Rengi:").pack(side="left", padx=(0, 10))
        self.renk_secimi = StringVar(value="both")
        ttk.Radiobutton(input_frame2, text="Her İki Renk", variable=self.renk_secimi, value="both").pack(side="left",
                                                                                                         padx=(0, 10))
        ttk.Radiobutton(input_frame2, text="Beyaz", variable=self.renk_secimi, value="white").pack(side="left",
                                                                                                   padx=(0, 10))
        ttk.Radiobutton(input_frame2, text="Siyah", variable=self.renk_secimi, value="black").pack(side="left",
                                                                                                   padx=(0, 10))

        self.analiz_btn = ttk.Button(input_frame2, text="Analiz Et", command=self.on_analyze_callback)
        self.analiz_btn.pack(side="left", padx=(10, 0))

        self.durum_label = ttk.Label(main_frame,
                                     text="Kullanıcı adı girin, taş rengini seçin ve 'Analiz Et' düğmesine tıklayın.")
        self.durum_label.pack(fill="x", pady=(0, 10))

        self.tree = ttk.Treeview(main_frame, columns=("sira", "acilis", "sayi", "kazanma_orani"), show="headings")
        self.tree.heading("sira", text="#")
        self.tree.heading("acilis", text="Açılış Adı")
        self.tree.heading("sayi", text="Oyun Sayısı")
        self.tree.heading("kazanma_orani", text="Kazanma Oranı")
        self.tree.column("sira", width=30, anchor="center")
        self.tree.column("acilis", width=350, anchor="w")
        self.tree.column("sayi", width=100, anchor="center")
        self.tree.column("kazanma_orani", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.root.bind('<Return>', lambda event: self.on_analyze_callback())

    def get_inputs(self):
        return {
            "username": self.kullanici_adi_entry.get().strip(),
            "max_games": self.oyun_sayisi_entry.get().strip(),
            "color": self.renk_secimi.get()
        }

    def set_status(self, message):
        self.durum_label.config(text=message)
        self.root.update()

    def clear_results(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

    def display_results(self, results):
        for i, (acilis, sayi, oran) in enumerate(results, 1):
            self.tree.insert("", "end", values=(i, acilis, sayi, f"%{oran:.1f}"))

    def show_error(self, message):
        messagebox.showerror("Hata", message)