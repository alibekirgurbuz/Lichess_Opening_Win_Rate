# main.py

import tkinter as tk
from view import LichessAnalyzerView
from model import get_games_from_lichess
from analyzer import analyze_openings


def main():
    root = tk.Tk()

    def on_analyze():
        inputs = view.get_inputs()
        username = inputs["username"]

        if not username:
            view.show_error("Lütfen bir kullanıcı adı girin.")
            return

        try:
            max_games = int(inputs["max_games"])
            if max_games <= 0:
                view.show_error("Oyun sayısı pozitif bir sayı olmalıdır.")
                return
        except ValueError:
            view.show_error("Lütfen geçerli bir sayı girin.")
            return

        color_filter = inputs["color"]

        # UI'ı güncelle
        view.set_status("Analiz yapılıyor...")
        view.clear_results()

        # Model'den veriyi al
        games, error = get_games_from_lichess(username, max_games)

        if error:
            view.set_status(f"Hata: {error}")
            return

        if not games:
            view.set_status(f"{username} için oyun bulunamadı.")
            return

        # Analyzer ile veriyi işle
        results, error = analyze_openings(games, username, color_filter, 5)

        if error:
            view.set_status(f"Analiz hatası: {error}")
            return

        # View'a sonuçları göster
        if not results:
            renk_metin = "beyaz taşlarla" if color_filter == "white" else "siyah taşlarla" if color_filter == "black" else ""
            view.set_status(f"{username} için {renk_metin} oynanan açılış bulunamadı.")
        else:
            view.display_results(results)
            renk_metin = "beyaz ve siyah taşlarla" if color_filter == "both" else "beyaz taşlarla" if color_filter == "white" else "siyah taşlarla"
            view.set_status(f"{username} kullanıcısının {renk_metin} en çok oynadığı {len(results)} açılış listelendi.")

    view = LichessAnalyzerView(root, on_analyze)
    root.mainloop()


if __name__ == "__main__":
    main()