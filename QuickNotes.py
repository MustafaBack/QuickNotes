import tkinter as tk
from tkinter import filedialog, messagebox, font
import datetime

class QuickNotes(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QuickNotes")
        self.geometry("800x600")

        # Başlangıçta açık modda başlıyoruz
        self.is_dark_mode = False
        self.current_file = None  # Kaydedilen dosya yolu

        # Metin alanı
        self.text_area = tk.Text(self)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        # Durum çubuğu
        self.status_bar = tk.Label(self, text="Satır: 1, Sütun: 1", anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Menü çubuğu
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Dosya menüsü
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Dosya", menu=self.file_menu)

        self.file_menu.add_command(label="Aç", command=self.open_file)
        self.file_menu.add_command(label="Farklı Kaydet", command=self.save_as)
        self.file_menu.add_command(label="Kaydet", command=self.save_file, state=tk.DISABLED)  # Başta Kaydet menüde görünmesin
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Çıkış", command=self.on_close)

        # Düzen menüsü
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Düzen", menu=self.edit_menu)
        self.edit_menu.add_command(label="Geri Al", command=self.undo)
        self.edit_menu.add_command(label="Kes", command=self.cut)
        self.edit_menu.add_command(label="Kopyala", command=self.copy)
        self.edit_menu.add_command(label="Yapıştır", command=self.paste)
        self.edit_menu.add_command(label="Sil", command=self.delete)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Tümünü Seç", command=self.select_all)

        # Git menüsü
        self.go_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Git", menu=self.go_menu)
        self.go_menu.add_command(label="Saat/Tarih", command=self.insert_time_date)
        self.go_menu.add_separator()

        # Yazı Tipi menüsü
        self.font_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Yazı Tipi", menu=self.font_menu)
        self.font_menu.add_command(label="Arial", command=lambda: self.change_font("Arial", 12))
        self.font_menu.add_command(label="Times New Roman", command=lambda: self.change_font("Times New Roman", 12))
        self.font_menu.add_command(label="Courier", command=lambda: self.change_font("Courier", 12))

        # Karanlık Mod / Açık Mod menüsü
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Görünüm", menu=self.view_menu)
        self.view_menu.add_command(label="Karanlık Mod", command=self.toggle_mode)
        self.view_menu.add_command(label="Açık Mod", command=self.toggle_mode)

        # Başlangıçta karanlık modda değiliz
        self.apply_light_mode()

        # Uygulama kapanmadan önce uyarı
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_mode(self):
        """Karanlık mod ve açık mod arasında geçiş yapar"""
        if self.is_dark_mode:
            self.is_dark_mode = False
            self.apply_light_mode()
        else:
            self.is_dark_mode = True
            self.apply_dark_mode()

    def apply_light_mode(self):
        """Açık mod ayarları"""
        self.config(bg="white")
        self.text_area.config(bg="white", fg="black")
        self.status_bar.config(bg="lightgray", fg="black")
        self.change_menu_style(bg="white", fg="black")

    def apply_dark_mode(self):
        """Karanlık mod ayarları"""
        self.config(bg="black")
        self.text_area.config(bg="black", fg="white")
        self.status_bar.config(bg="gray", fg="white")
        self.change_menu_style(bg="black", fg="white")

    def change_menu_style(self, bg, fg):
        """Menü çubuğunun stilini değiştirir"""
        self.menu_bar.config(bg=bg, fg=fg)
        self.file_menu.config(bg=bg, fg=fg)
        self.edit_menu.config(bg=bg, fg=fg)
        self.go_menu.config(bg=bg, fg=fg)
        self.font_menu.config(bg=bg, fg=fg)
        self.view_menu.config(bg=bg, fg=fg)

    def open_file(self):
        """Dosya açar"""
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, file.read())
                self.current_file = file_path  # Dosya yolu kaydedildi
                self.file_menu.entryconfig("Kaydet", state=tk.NORMAL)  # Kaydet butonunu aktif et
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya açılamadı: {str(e)}")

    def save_file(self):
        """Dosyayı kaydeder"""
        if self.current_file:  # Eğer bir dosya yolu varsa
            try:
                with open(self.current_file, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Başarılı", "Dosya başarıyla kaydedildi.")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilemedi: {str(e)}")
        else:  # Eğer dosya kaydedilmemişse, farklı kaydet yapalım
            self.save_as()

    def save_as(self):
        """Farklı kaydet işlemi"""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.current_file = file_path  # Yeni dosya yolu kaydedildi
                self.file_menu.entryconfig("Kaydet", state=tk.NORMAL)  # Kaydet butonunu aktif et
                messagebox.showinfo("Başarılı", "Dosya başarıyla kaydedildi.")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilemedi: {str(e)}")
    
    def undo(self):
        """Geri alma işlemi"""
        self.text_area.event_generate("<<Undo>>")

    def cut(self):
        """Kesme işlemi"""
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        """Kopyalama işlemi"""
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        """Yapıştırma işlemi"""
        self.text_area.event_generate("<<Paste>>")

    def delete(self):
        """Silme işlemi"""
        self.text_area.delete("sel.first", "sel.last")

    def select_all(self):
        """Tümünü seçme işlemi"""
        self.text_area.tag_add("sel", "1.0", "end")
    
    def insert_time_date(self):
        """Saat ve tarih ekleme"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_area.insert(tk.END, current_time)

    def change_font(self, font_name, font_size):
        """Yazı tipini değiştirme"""
        self.text_area.config(font=(font_name, font_size))

    def on_close(self):
        """Uygulama kapanmadan önce uyarı"""
        if messagebox.askyesno("Çıkmak Üzeresiniz", "Değişiklikleri kaydetmeden çıkmak istediğinizden emin misiniz?", icon='warning'):
            self.destroy()


if __name__ == "__main__":
    app = QuickNotes()
    app.mainloop()
