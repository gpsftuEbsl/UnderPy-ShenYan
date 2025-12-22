# underPy/ui/game_ui.py

import tkinter as tk
from functools import partial
from PIL import Image, ImageTk # 記得 pip install pillow

class GameUI:
    def __init__(self, master, game_manager):
        self.master = master
        self.game = game_manager
        self.master.title("UnderPy - Dungeon Adventure")
        self.master.geometry("600x650") 
        
        # --- [美化設定] ---
        # 定義色票 (Color Palette)
        self.colors = {
            "bg_main": "#2C3E50",       # 主視窗背景 (深藍灰)
            "bg_text": "#34495E",       # 文字區背景 (淺一點的灰)
            "fg_text": "#ECF0F1",       # 一般文字 (白)
            "fg_accent": "#E74C3C",     # 強調色 (紅 - HP)
            "btn_bg": "#2980B9",        # 按鈕背景 (藍)
            "btn_fg": "#FFFFFF",        # 按鈕文字 (白)
            "btn_hover": "#3498DB",     # 按鈕滑鼠懸停色
            "input_bg": "#ECF0F1",      # 輸入框背景
            "input_fg": "#2C3E50"       # 輸入框文字
        }
        
        # 定義字體
        self.fonts = {
            "main": ("Microsoft JhengHei", 12),           # 一般中文
            "mono": ("Consolas", 11),                     # 數據/系統訊息
            "bold": ("Microsoft JhengHei", 12, "bold"),   # 按鈕/標題
            "status": ("Impact", 16)                      # HP 狀態
        }

        # 設定主視窗背景
        self.master.configure(bg=self.colors["bg_main"])

        # --- 1. 狀態顯示區 (HP) ---
        self.status_frame = tk.Frame(master, bg=self.colors["bg_main"])
        self.status_frame.pack(fill="x", pady=(15, 5), padx=20)
        
        self.status_label = tk.Label(
            self.status_frame, 
            text="HP: 100/100", 
            font=self.fonts["status"],
            bg=self.colors["bg_main"], 
            fg=self.colors["fg_accent"],
            anchor="w"
        )
        self.status_label.pack(side="left")

        # --- 2. 圖片顯示區 ---
        # 加一個外框讓圖片看起來像在相框裡
        self.image_frame = tk.Frame(master, bg="black", bd=2, relief="sunken")
        self.image_frame.pack(pady=10)
        
        self.image_label = tk.Label(self.image_frame, bg="black")
        self.image_label.pack()
        self.current_image = None 

        # --- 3. 劇情文字區 (含捲軸) ---
        self.text_frame = tk.Frame(master, bg=self.colors["bg_main"])
        self.text_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # 捲軸
        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            self.text_frame, 
            height=10, 
            state='disabled',
            bg=self.colors["bg_text"],
            fg=self.colors["fg_text"],
            font=self.fonts["main"],
            bd=0,               # 去除邊框
            padx=10, pady=10,   # 內距
            yscrollcommand=self.scrollbar.set,
            relief="flat"       # 扁平化
        )
        self.text_area.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.text_area.yview)
        
        # 設定 Text 的 Tag 樣式 (讓系統訊息有顏色)
        self.text_area.tag_config("system", foreground="#F1C40F") # 黃色警告

        # --- 4. 密碼輸入區 (平時隱藏) ---
        self.input_frame = tk.Frame(master, bg=self.colors["bg_main"])
        
        self.entry_field = tk.Entry(
            self.input_frame, 
            font=self.fonts["mono"],
            bg=self.colors["input_bg"],
            fg=self.colors["input_fg"],
            bd=0,
            relief="flat"
        )
        self.entry_field.pack(side="left", padx=5, ipady=3)
        
        self.confirm_btn = tk.Button(
            self.input_frame, 
            text="確認輸入", 
            command=self.submit_password,
            font=self.fonts["bold"],
            bg=self.colors["fg_accent"], # 紅色按鈕
            fg="white",
            relief="flat",
            activebackground="#C0392B",
            activeforeground="white",
            cursor="hand2"
        )
        self.confirm_btn.pack(side="left", padx=5)

        # --- 5. 按鈕區 ---
        self.button_frame = tk.Frame(master, bg=self.colors["bg_main"])
        self.button_frame.pack(pady=20, padx=20, fill="x")

    # --- UI 方法 ---

    def update_status(self, text):
        self.status_label.config(text=text)

    def update_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.config(state='disabled')

    def append_text(self, text):
        self.text_area.config(state='normal')
        if "【系統】" in text:
            self.text_area.insert(tk.END, text + "\n", "system")
        else:
            self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def set_choices(self, choices, handler_function):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        if choices and handler_function:
            inner_frame = tk.Frame(self.button_frame, bg=self.colors["bg_main"])
            inner_frame.pack()

            for choice in choices:
                command = partial(handler_function, choice)
                btn = tk.Button(
                    inner_frame, 
                    text=choice, 
                    command=command, 
                    width=12,
                    font=self.fonts["bold"],
                    bg=self.colors["btn_bg"],
                    fg=self.colors["btn_fg"],
                    activebackground=self.colors["btn_hover"],
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    pady=5,
                    cursor="hand2"
                )
                btn.pack(side="left", padx=10)

    def update_image(self, image_path=None):
        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((400, 250), Image.Resampling.LANCZOS)
                self.current_image = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.current_image, width=400, height=250)
            except Exception as e:
                print(f"載入圖片失敗: {e}")
                self.image_label.config(image="", width=1, height=1)
        else:
            self.image_label.config(image="", width=1, height=1)

    # --- 輸入框控制 ---
    def show_input_field(self):
        self.input_frame.pack(pady=10, after=self.text_area) 
        self.entry_field.delete(0, tk.END)
        self.entry_field.focus()

    def hide_input_field(self):
        self.input_frame.pack_forget()

    def submit_password(self):
        password = self.entry_field.get()
        self.game.handle_password_input(password)
