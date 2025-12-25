# ui/game_ui.py
# 這裡專門拿來放遊戲介面相關的程式碼

import tkinter as tk
from functools import partial
from PIL import Image, ImageTk 
import random 

class GameUI:
    def __init__(self, master, game_manager):
        self.master = master
        self.game = game_manager
        self.master.title("UnderPy - Dungeon Adventure")
        
        # --- 全螢幕與視窗設定 ---
        self.master.attributes("-fullscreen", True)
        self.master.bind("<Escape>", self.exit_fullscreen)
        self.master.bind("<F11>", self.toggle_fullscreen)
        
        self.typing_job = None 
        
        # --- 美化與字體設定 ---
        self.colors = {
            "bg_main": "#000000", "bg_text": "#121D25", "fg_text": "#ECF0F1",
            "fg_accent": "#E74C3C", "btn_bg": "#121D25", "btn_fg": "#FFFFFF",
            "btn_hover": "#434343", "input_bg": "#ECF0F1", "input_fg": "#2C3E50"
        }
        
        self.fonts = {
            "main": ("Microsoft JhengHei", 18),
            "mono": ("Consolas", 16),
            "bold": ("Microsoft JhengHei", 16, "bold"),
            "status": ("Impact", 20)
        }

        self.master.configure(bg=self.colors["bg_main"])

        # --- 建立主容器 (用於震動) ---
        self.main_container = tk.Frame(self.master, bg=self.colors["bg_main"])
        self.main_container.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --- 1. 狀態顯示區 ---
        self.status_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.status_frame.pack(fill="x", pady=(40, 5), padx=50) 
        self.status_label = tk.Label(
            self.status_frame, text="HP: 100/100", font=self.fonts["status"],
            bg=self.colors["bg_main"], fg=self.colors["fg_accent"], anchor="w"
        )
        self.status_label.pack(side="left")

        # --- 2. 圖片顯示區 ---
        self.image_frame = tk.Frame(self.main_container, bg="black", bd=2, relief="sunken")
        self.image_frame.pack(pady=10)
        self.image_label = tk.Label(self.image_frame, bg="black")
        self.image_label.pack()
        self.current_image = None 

        # --- 3. 劇情文字區 ---
        # 這裡移除 expand=True，改用固定高度，確保下方空間
        self.text_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.text_frame.pack(pady=10, padx=50, fill="x") # 移除 expand，改用 fill="x"

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            self.text_frame, height=8, state='disabled', # 高度設為 8 行字，避免佔用過多空間
            bg=self.colors["bg_text"], fg=self.colors["fg_text"],
            font=self.fonts["main"], bd=0, padx=20, pady=20,
            yscrollcommand=self.scrollbar.set, relief="flat", wrap="word"
        )
        self.text_area.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.text_area.yview)
        self.text_area.tag_config("system", foreground="#F1C40F")

        # --- 4. 密碼輸入區 (平時隱藏) ---
        self.input_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        # 這裡不 pack，由 show_input_field 控制
        
        self.entry_field = tk.Entry(self.input_frame, font=self.fonts["mono"],
                                   bg=self.colors["input_bg"], fg=self.colors["input_fg"], 
                                   bd=0, width=20)
        self.entry_field.pack(side="left", padx=10, ipady=8)
        
        self.confirm_btn = tk.Button(self.input_frame, text="確認送出", command=self.submit_password,
                                    font=self.fonts["bold"], bg=self.colors["fg_accent"], fg="white",
                                    relief="flat", cursor="hand2", padx=20, pady=5)
        self.confirm_btn.pack(side="left", padx=5)

        # --- 5. 按鈕區 ---
        self.button_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.button_frame.pack(pady=20, padx=50, fill="x")

    # --- 全螢幕與基礎功能 ---
    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.master.attributes("-fullscreen")
        self.master.attributes("-fullscreen", not is_fullscreen)
        self.main_container.place(relx=0, rely=0, relwidth=1, relheight=1)

    def exit_fullscreen(self, event=None):
        self.master.attributes("-fullscreen", False)
        self.master.geometry("1000x800")
        self.main_container.place(relx=0, rely=0, relwidth=1, relheight=1)

    def update_status(self, text):
        self.status_label.config(text=text)

    def update_image(self, image_path=None):
        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((500, 350), Image.Resampling.LANCZOS)
                self.current_image = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.current_image, width=500, height=350)
            except Exception:
                self.image_label.config(image="", width=1, height=1)
        else:
            self.image_label.config(image="", width=1, height=1)

    def set_choices(self, choices, handler_function):
        for widget in self.button_frame.winfo_children(): widget.destroy()
        if choices:
            inner = tk.Frame(self.button_frame, bg=self.colors["bg_main"])
            inner.pack()
            for choice in choices:
                btn = tk.Button(inner, text=choice, command=partial(handler_function, choice),
                                width=15, font=self.fonts["bold"], bg=self.colors["btn_bg"],
                                fg=self.colors["btn_fg"], relief="flat", pady=10, cursor="hand2")
                btn.pack(side="left", padx=15)

    # --- 特效功能 ---
    def type_text(self, text, speed=60, clear=True):
        if self.typing_job is not None:
            self.master.after_cancel(self.typing_job)
        self.text_area.config(state='normal')
        if clear: self.text_area.delete('1.0', tk.END)
        self.text_area.config(state='disabled')
        self._type_next_char(text + "\n", 0, speed)

    def _type_next_char(self, text, index, speed):
        if index < len(text):
            char = text[index]
            self.text_area.config(state='normal')
            tag = "system" if "【系統】" in text or "提示" in text else None
            self.text_area.insert(tk.END, char, tag)
            self.text_area.see(tk.END)
            self.text_area.config(state='disabled')
            self.typing_job = self.master.after(speed, self._type_next_char, text, index + 1, speed)
        else:
            self.typing_job = None

    def shake_window(self):
        offsets = [(12, 7), (-12, -7), (10, -5), (-10, 5), (6, 3), (-6, -3), (0, 0)]
        for i, (dx, dy) in enumerate(offsets):
            self.master.after(i * 25, lambda x=dx, y=dy: self.main_container.place(
                x=x, y=y, relwidth=1, relheight=1
            ))

    def flash_red(self):
        old = self.colors["bg_main"]
        targets = [self.master, self.main_container, self.text_frame, self.status_frame, self.button_frame]
        for f in targets: f.configure(bg="#E74C3C")
        self.master.after(100, lambda: self._reset_color(old))

    def _reset_color(self, bg):
        targets = [self.master, self.main_container, self.text_frame, self.status_frame, self.button_frame]
        for f in targets: f.configure(bg=bg)

    # --- 輸入框控制 (關鍵修正) ---
    def show_input_field(self):
        # 修正：排在 text_frame 後面，而不是 text_area 後面
        self.input_frame.pack(pady=20, after=self.text_frame)
        self.entry_field.focus()

    def hide_input_field(self):
        self.input_frame.pack_forget()

    def submit_password(self):
        self.game.handle_password_input(self.entry_field.get())
