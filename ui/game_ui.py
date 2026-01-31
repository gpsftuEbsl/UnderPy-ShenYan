# ui/game_ui.py
# 這裡專門拿來放遊戲介面相關的程式碼

import tkinter as tk
from functools import partial
from PIL import Image, ImageTk
import os
from config import UI_COLORS, UI_FONTS, TYPEWRITER_SPEED, UI_IMAGE_WIDTH, UI_IMAGE_HEIGHT, UI_TEXT_HEIGHT, SHAKE_WINDOW_OFFSETS, SHAKE_WINDOW_INTERVAL, FLASH_RED_DURATION

class GameUI:
    """
    GameUI 的 Docstring

    負責遊戲介面的顯示與互動

    :param master: 主視窗物件 (tk.Tk)
    :param game_manager: 遊戲管理器物件 (GameManager)
    """
    def __init__(self, master, game_manager):
        self.master = master
        self.game = game_manager
        self.master.title("UnderPy - Dungeon Adventure")
        
        # --- 全螢幕與視窗設定 ---
        self.master.attributes("-fullscreen", True)
        
        # 修改：將 Esc 鍵綁定到退出程式
        self.master.bind("<Escape>", self.on_exit) 
        self.master.bind("<F11>", self.toggle_fullscreen)
        
        self.typing_job = None 
        
        # --- 美化與字體設定（使用 config）---
        self.colors = UI_COLORS
        self.fonts = UI_FONTS

        self.master.configure(bg=self.colors["bg_main"])

        # --- 建立主容器 (用於震動) ---
        self.main_container = tk.Frame(self.master, bg=self.colors["bg_main"])
        self.main_container.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --- 1. 狀態顯示區 ---
        self.status_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.status_frame.pack(fill="x", pady=(40, 5), padx=50) 
        
        # 左邊：HP 狀態 (保持變數名稱為 self.status_label)
        self.status_label = tk.Label(
            self.status_frame, text="HP: 100/100", font=self.fonts["status"],
            bg=self.colors["bg_main"], fg=self.colors["fg_accent"], anchor="w"
        )
        self.status_label.pack(side="left")
        
        # 右邊：提示文字
        self.hint_label = tk.Label(
            self.status_frame, text="press ESC to close", font=self.fonts["status"],
            bg=self.colors["bg_main"], fg=self.colors["fg_accent"], anchor="e"
        )
        self.hint_label.pack(side="right")

        # --- 2. 圖片顯示區 ---
        self.image_frame = tk.Frame(self.main_container, bg="black", bd=2, relief="sunken")
        self.image_frame.pack(pady=10)
        self.image_label = tk.Label(self.image_frame, bg="black")
        self.image_label.pack()
        self.current_image = None 

        # --- 3. 劇情文字區 ---
        # 固定高度，確保下方空間
        self.text_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.text_frame.pack(pady=10, padx=50, fill="x") # 移除 expand，改用 fill="x"

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            self.text_frame, height=UI_TEXT_HEIGHT, state='disabled', # 高度設為 8 行字，避免佔用過多空間
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
        
        self.confirm_btn = tk.Button(self.input_frame, text="請按這送出", command=self.submit_password,
                                     font=self.fonts["bold"], bg=self.colors["fg_accent"], fg="white",
                                     relief="flat", cursor="hand2", padx=20, pady=5)
        self.confirm_btn.pack(side="left", padx=5)

        # --- 5. 按鈕區 ---
        self.button_frame = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.button_frame.pack(pady=20, padx=50, fill="x")

    # --- 全螢幕與基礎功能 ---
    def toggle_fullscreen(self, event=None):
        """
        toggle_fullscreen 的 Docstring
        
        :param self: GameUI 物件
        :param event: 事件物件 (預設為 None)
        切換全螢幕模式
        """
        is_fullscreen = self.master.attributes("-fullscreen")
        self.master.attributes("-fullscreen", not is_fullscreen)
        self.main_container.place(relx=0, rely=0, relwidth=1, relheight=1)

    # 新增：退出遊戲的函式
    def on_exit(self, event=None):
        """
        關閉遊戲視窗
        :param event: Tkinter 觸發事件時會自動傳入
        """
        self.master.destroy()

    def update_status(self, text):
        """
        update_status 的 Docstring
        
        :param self: GameUI 物件
        :param text: 狀態文字
        """
        # 這裡的 self.status_label 指向左邊的 HP 血條
        self.status_label.config(text=text)

    

    def update_image(self, image_path=None):
        if not image_path:
            self.image_label.config(image="", width=1, height=1)
            return

        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            full_path = os.path.join(base_dir, image_path)

            # 驗證檔案存在
            if not os.path.exists(full_path):
                self.image_label.config(image="", width=1, height=1)
                return

            img = Image.open(full_path)
            img = img.resize((UI_IMAGE_WIDTH, UI_IMAGE_HEIGHT), Image.Resampling.LANCZOS)
            self.current_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.current_image, width=UI_IMAGE_WIDTH, height=UI_IMAGE_HEIGHT)

        except FileNotFoundError:
            # 圖片檔案不存在，靜默處理
            self.image_label.config(image="", width=1, height=1)
        except Exception as e:
            # PIL 無法打開或處理圖片，靜默處理
            self.image_label.config(image="", width=1, height=1)


    def set_choices(self, choices, handler_function):
        """
        set_choices 的 Docstring
        
        :param self: GameUI 物件
        :param choices: 選項清單
        :param handler_function: 選項處理函式
        """
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
    def type_text(self, text, speed=TYPEWRITER_SPEED, clear=True):
        """
        type_text 的 Docstring

        以打字機效果顯示文字
        
        :param self: GameUI 物件
        :param text: 要打字的文字
        :param speed: 打字速度 (毫秒)
        :param clear: 是否清除現有文字
        """
        if self.typing_job is not None:
            self.master.after_cancel(self.typing_job)
        self.text_area.config(state='normal')
        if clear: self.text_area.delete('1.0', tk.END)
        self.text_area.config(state='disabled')
        self._type_next_char(text + "\n", 0, speed)

    def _type_next_char(self, text, index, speed):
        """
        _type_next_char 的 Docstring

        內部遞迴函式，用於逐字顯示文字
        
        :param self: GameUI 物件
        :param text: 完整文字
        :param index: 當前索引
        :param speed: 打字速度 (毫秒)
        """
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
        offsets = SHAKE_WINDOW_OFFSETS
        for i, (dx, dy) in enumerate(offsets):
            self.master.after(i * SHAKE_WINDOW_INTERVAL, lambda x=dx, y=dy: self.main_container.place(
                x=x, y=y, relwidth=1, relheight=1
            ))

    def flash_red(self):
        """
        受到傷害時畫面閃紅特效
        
        :param self: GameUI 物件
        """
        old = self.colors["bg_main"]
        targets = [self.master, self.main_container, self.text_frame, self.status_frame, self.button_frame]
        for f in targets: f.configure(bg="#E74C3C")
        self.master.after(FLASH_RED_DURATION, lambda: self._reset_color(old))

    def _reset_color(self, bg):
        targets = [self.master, self.main_container, self.text_frame, self.status_frame, self.button_frame]
        for f in targets: f.configure(bg=bg)

    # --- 輸入框控制 (已修正顯示問題) ---
    def show_input_field(self):
        """顯示輸入框"""
        # 修正：排在 text_frame 後面，而不是 text_area 後面
        self.input_frame.pack(pady=20, after=self.text_frame)
        self.entry_field.focus()

    def hide_input_field(self):
        """
        影藏密碼輸入區 要用的時候再顯示
        """
        self.input_frame.pack_forget()

    def submit_password(self):
        self.game.handle_password_input(self.entry_field.get())