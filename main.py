import tkinter as tk
from tkinter import font
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Hesap Makinesi")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C3E50')
        
        # Değişkenler
        self.current_input = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        # Renkler
        self.bg_color = "#2C3E50"
        self.display_bg = "#34495E"
        self.button_bg = "#ECF0F1"
        self.button_fg = "#2C3E50"
        self.operator_bg = "#E67E22"
        self.operator_fg = "white"
        self.equal_bg = "#27AE60"
        self.equal_fg = "white"
        self.clear_bg = "#E74C3C"
        self.clear_fg = "white"
        self.func_bg = "#3498DB"
        self.func_fg = "white"
        
        # Fontlar
        self.display_font = font.Font(family="Segoe UI", size=28, weight="bold")
        self.button_font = font.Font(family="Segoe UI", size=14, weight="bold")
        
        self.create_widgets()
        self.bind_keys()
    
    def create_widgets(self):
        # Ekran çerçevesi
        display_frame = tk.Frame(self.root, bg=self.bg_color, height=120)
        display_frame.pack(fill=tk.BOTH, padx=10, pady=(20, 10))
        display_frame.pack_propagate(False)
        
        # Ekran
        self.display_label = tk.Label(
            display_frame,
            textvariable=self.result_var,
            font=self.display_font,
            bg=self.display_bg,
            fg="white",
            anchor="e",
            padx=15,
            pady=20,
            relief=tk.FLAT
        )
        self.display_label.pack(fill=tk.BOTH, expand=True)
        
        # Buton çerçevesi
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 20))
        
        # Buton düzeni
        buttons = [
            ('C', 0, 0, 1, self.clear_bg, self.clear_fg),
            ('±', 0, 1, 1, self.func_bg, self.func_fg),
            ('%', 0, 2, 1, self.func_bg, self.func_fg),
            ('÷', 0, 3, 1, self.operator_bg, self.operator_fg),
            ('7', 1, 0, 1, self.button_bg, self.button_fg),
            ('8', 1, 1, 1, self.button_bg, self.button_fg),
            ('9', 1, 2, 1, self.button_bg, self.button_fg),
            ('×', 1, 3, 1, self.operator_bg, self.operator_fg),
            ('4', 2, 0, 1, self.button_bg, self.button_fg),
            ('5', 2, 1, 1, self.button_bg, self.button_fg),
            ('6', 2, 2, 1, self.button_bg, self.button_fg),
            ('-', 2, 3, 1, self.operator_bg, self.operator_fg),
            ('1', 3, 0, 1, self.button_bg, self.button_fg),
            ('2', 3, 1, 1, self.button_bg, self.button_fg),
            ('3', 3, 2, 1, self.button_bg, self.button_fg),
            ('+', 3, 3, 1, self.operator_bg, self.operator_fg),
            ('0', 4, 0, 2, self.button_bg, self.button_fg),
            ('.', 4, 2, 1, self.button_bg, self.button_fg),
            ('=', 4, 3, 1, self.equal_bg, self.equal_fg),
        ]
        
        # Butonları oluştur
        for btn in buttons:
            text, row, col, colspan, bg, fg = btn
            button = tk.Button(
                buttons_frame,
                text=text,
                font=self.button_font,
                bg=bg,
                fg=fg,
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=lambda t=text: self.button_click(t)
            )
            
            # Hover efekti
            button.bind("<Enter>", lambda e, b=button, bg=bg: b.configure(bg=self.darken_color(bg)))
            button.bind("<Leave>", lambda e, b=button, bg=bg: b.configure(bg=bg))
            
            button.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=5, pady=5)
        
        # Grid ağırlıkları
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)
    
    def darken_color(self, color):
        """Rengi koyulaştır"""
        if color == self.button_bg:
            return "#D5D8DC"
        elif color == self.operator_bg:
            return "#D35400"
        elif color == self.equal_bg:
            return "#229954"
        elif color == self.clear_bg:
            return "#C0392B"
        elif color == self.func_bg:
            return "#2980B9"
        return color
    
    def button_click(self, value):
        if value == 'C':
            self.current_input = ""
            self.result_var.set("0")
        elif value == '=':
            self.calculate_result()
        elif value == '±':
            if self.current_input and self.current_input != "0":
                if self.current_input[0] == '-':
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.result_var.set(self.current_input)
        elif value == '%':
            self.calculate_percentage()
        elif value in ['+', '-', '×', '÷']:
            if self.current_input:
                self.current_input += ' ' + value + ' '
                self.result_var.set(self.current_input)
        else:
            # Sayı ve nokta ekleme
            if self.current_input == "0" and value != '.':
                self.current_input = value
            else:
                self.current_input += value
            self.result_var.set(self.current_input)
    
    def calculate_result(self):
        try:
            # İşlem sembollerini Python operatörlerine çevir
            expression = self.current_input.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            
            # Sonucu formatla
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 8)
            
            self.current_input = str(result)
            self.result_var.set(self.current_input)
        except Exception as e:
            self.result_var.set("Hata!")
            self.current_input = ""
    
    def calculate_percentage(self):
        try:
            # Yüzde hesaplama
            expression = self.current_input.replace('×', '*').replace('÷', '/')
            result = eval(expression) / 100
            self.current_input = str(result)
            self.result_var.set(self.current_input)
        except:
            self.result_var.set("Hata!")
            self.current_input = ""
    
    def bind_keys(self):
        """Klavye desteği"""
        self.root.bind('<Return>', lambda e: self.button_click('='))
        self.root.bind('<Escape>', lambda e: self.button_click('C'))
        self.root.bind('<BackSpace>', self.backspace)
        
        for key in '0123456789':
            self.root.bind(key, lambda e, k=key: self.button_click(k))
        
        self.root.bind('+', lambda e: self.button_click('+'))
        self.root.bind('-', lambda e: self.button_click('-'))
        self.root.bind('*', lambda e: self.button_click('×'))
        self.root.bind('/', lambda e: self.button_click('÷'))
        self.root.bind('.', lambda e: self.button_click('.'))
        self.root.bind('%', lambda e: self.button_click('%'))
    
    def backspace(self, event):
        self.current_input = self.current_input[:-1]
        if not self.current_input:
            self.current_input = "0"
        self.result_var.set(self.current_input)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ModernCalculator(root)
    root.mainloop()