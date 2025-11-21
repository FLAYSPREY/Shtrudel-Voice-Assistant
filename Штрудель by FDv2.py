import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import os
import webbrowser
import time
import threading
from datetime import datetime
import random
import speech_recognition as sr
import math
import re

# Проверяем установленные пакеты
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

class UltraModernVoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.tts_engine = None
        self.is_speaking = False
        self.is_listening = False
        self.animation_angle = 0
        
        # Современная цветовая схема
        self.colors = {
            'bg_dark': '#0a0a12',
            'bg_medium': '#1a1a2e',
            'bg_light': '#252542',
            'accent_purple': '#8b5cf6',
            'accent_blue': '#06b6d4',
            'accent_green': '#10b981',
            'accent_pink': '#ec4899',
            'accent_orange': '#f59e0b',
            'accent_red': '#ef4444',
            'text_primary': '#f8fafc',
            'text_secondary': '#94a3b8',
            'glass_effect': 'rgba(30, 30, 60, 0.7)'
        }
        
        # Инициализация голосового движка
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.setup_voice()
            except Exception as e:
                print(f"Ошибка TTS: {e}")
        
        # Инициализация распознавания речи
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.speech_available = True
        except:
            self.speech_available = False
        
        self.setup_ui()
        self.log_message("🚀 Нейро-ассистент активирован!", "success")
        
        # Калибровка микрофона
        if self.speech_available:
            threading.Thread(target=self.calibrate_microphone, daemon=True).start()

    def calibrate_microphone(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.log_message("✅ Микрофон откалиброван", "success")
        except Exception as e:
            self.log_message(f"⚠️ Ошибка калибровки: {e}", "warning")

    def setup_voice(self):
        if self.tts_engine:
            try:
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
                self.tts_engine.setProperty('rate', 160)
                self.tts_engine.setProperty('volume', 0.8)
            except Exception as e:
                print(f"Ошибка настройки голоса: {e}")

    def setup_ui(self):
        self.root.title("🔮 НЕЙРО-АССИСТЕНТ | Голосовое управление")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.colors['bg_dark'])
        self.root.minsize(1300, 800)
        
        # Современные эффекты
        self.root.attributes('-alpha', 0.97)
        
        self.set_modern_style()
        self.create_layout()

    def set_modern_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.TFrame', background=self.colors['bg_medium'])
        style.configure('Modern.TNotebook', background=self.colors['bg_dark'], borderwidth=0)
        style.configure('Modern.TNotebook.Tab', 
                       background=self.colors['bg_medium'],
                       foreground=self.colors['text_primary'],
                       padding=[25, 12],
                       font=('Segoe UI', 11, 'bold'),
                       focuscolor='none')
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['accent_purple'])],
                 foreground=[('selected', self.colors['bg_dark'])])

    def create_layout(self):
        # Главный контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # Баннер
        self.create_banner(main_container)
        
        # Панель управления
        self.create_control_panel(main_container)
        
        # Основной контент
        self.create_content_area(main_container)

    def create_banner(self, parent):
        banner_frame = tk.Frame(parent, bg=self.colors['bg_medium'], height=100)
        banner_frame.pack(fill=tk.X, pady=(0, 20))
        banner_frame.pack_propagate(False)
        
        # Стильный баннер с градиентом
        banner_canvas = tk.Canvas(banner_frame, bg=self.colors['bg_medium'], height=100, highlightthickness=0)
        banner_canvas.pack(fill=tk.BOTH, expand=True)
        
        banner_canvas.create_text(700, 35, text="🍎 ШТРУДЕЛЬ", 
                                font=('Segoe UI', 32, 'bold'),
                                fill=self.colors['accent_purple'])
        banner_canvas.create_text(700, 65, text="by FLAYSPREY and Dusia", 
                                font=('Segoe UI', 14, 'italic'),
                                fill=self.colors['text_secondary'])

    def create_control_panel(self, parent):
        control_frame = tk.Frame(parent, bg=self.colors['bg_medium'], relief=tk.FLAT, bd=0)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        inner_frame = tk.Frame(control_frame, bg=self.colors['bg_medium'])
        inner_frame.pack(fill=tk.X, padx=20, pady=20)

        # Левая часть - статусы
        status_frame = tk.Frame(inner_frame, bg=self.colors['bg_medium'])
        status_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        voice_status = "● ГОЛОСОВОЙ ВВОД: АКТИВЕН" if self.speech_available else "● ГОЛОСОВОЙ ВВОД: НЕДОСТУПЕН"
        voice_color = self.colors['accent_green'] if self.speech_available else self.colors['accent_red']
        
        tk.Label(status_frame, text=voice_status, font=('Segoe UI', 11, 'bold'),
                bg=self.colors['bg_medium'], fg=voice_color).pack(anchor=tk.W, pady=(0, 8))
        
        tts_status = "● TTS СИНТЕЗ РЕЧИ: АКТИВЕН" if TTS_AVAILABLE else "● TTS СИНТЕЗ РЕЧИ: НЕДОСТУПЕН"
        tts_color = self.colors['accent_green'] if TTS_AVAILABLE else self.colors['accent_red']
        
        tk.Label(status_frame, text=tts_status, font=('Segoe UI', 11),
                bg=self.colors['bg_medium'], fg=tts_color).pack(anchor=tk.W)

        # Центральная часть - кнопки управления
        btn_frame = tk.Frame(inner_frame, bg=self.colors['bg_medium'])
        btn_frame.pack(side=tk.LEFT, padx=50)
        
        self.listen_btn = self.create_glass_button(
            btn_frame, "🎤 НАЧАТЬ СЛУШАТЬ", self.colors['accent_purple'],
            self.start_voice_listening, width=180
        )
        
        if not self.speech_available:
            self.listen_btn.config(state=tk.DISABLED, bg=self.colors['text_secondary'])
        
        self.stop_btn = self.create_glass_button(
            btn_frame, "⏹️ ОСТАНОВИТЬ", self.colors['accent_red'],
            self.stop_voice_listening, width=150, state=tk.DISABLED
        )

        # Правая часть - визуализатор
        viz_frame = tk.Frame(inner_frame, bg=self.colors['bg_medium'])
        viz_frame.pack(side=tk.RIGHT)
        
        tk.Label(viz_frame, text="🎵 ВИЗУАЛИЗАТОР АКТИВНОСТИ", font=('Segoe UI', 10), 
                bg=self.colors['bg_medium'], fg=self.colors['text_secondary']).pack()
        
        self.visualizer_canvas = tk.Canvas(viz_frame, bg=self.colors['bg_light'],
                                          height=50, width=200, highlightthickness=0)
        self.visualizer_canvas.pack(pady=(8, 0))
        self.animate_visualizer()

    def create_glass_button(self, parent, text, color, command, width=120, state=tk.NORMAL):
        btn = tk.Button(parent,
                      text=text,
                      font=('Segoe UI', 10, 'bold'),
                      bg=color,
                      fg=self.colors['text_primary'],
                      width=width//8,
                      height=2,
                      relief=tk.FLAT,
                      bd=0,
                      cursor='hand2',
                      state=state,
                      command=command)
        btn.pack(side=tk.LEFT, padx=8)
        return btn

    def create_content_area(self, parent):
        notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка команд
        commands_frame = ttk.Frame(notebook, style='Modern.TFrame')
        notebook.add(commands_frame, text="⚡ БЫСТРЫЕ КОМАНДЫ")
        self.setup_commands_tab(commands_frame)
        
        # Вкладка журнала
        log_frame = ttk.Frame(notebook, style='Modern.TFrame')
        notebook.add(log_frame, text="📊 СИСТЕМНЫЙ ЖУРНАЛ")
        self.setup_log_tab(log_frame)
        
        # Вкладка голосовых команд
        voice_frame = ttk.Frame(notebook, style='Modern.TFrame')
        notebook.add(voice_frame, text="🎤 ГОЛОСОВЫЕ КОМАНДЫ")
        self.setup_voice_commands_tab(voice_frame)

    def setup_commands_tab(self, parent):
        container = tk.Frame(parent, bg=self.colors['bg_medium'])
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Сетка команд в современном стиле
        command_categories = [
            {
                "name": "🖥️ СИСТЕМНЫЕ",
                "color": self.colors['accent_blue'],
                "commands": [
                    ("📁 Проводник", self.open_explorer),
                    ("⚙️ Настройки", self.open_settings),
                    ("🔒 Блокировка", self.lock_pc),
                ]
            },
            {
                "name": "🌐 БРАУЗЕР",
                "color": self.colors['accent_green'],
                "commands": [
                    ("🌐 Браузер", self.open_browser),
                    ("➕ Новая вкладка", self.browser_new_tab),
                    ("❌ Закрыть вкладку", self.browser_close_tab),
                    ("➡️ Следующая вкладка", self.browser_next_tab),
                    ("⬅️ Предыдущая вкладка", self.browser_previous_tab),
                ]
            },
            {
                "name": "📺 YOUTUBE",
                "color": self.colors['accent_red'],
                "commands": [
                    ("📺 YouTube", self.open_youtube),
                    ("⏸️ Пауза", self.youtube_pause),
                    ("▶️ Играть", self.youtube_play),
                    ("⏩ Перемотай 10", lambda: self.youtube_skip(10)),
                    ("⏪ Назад 10", lambda: self.youtube_rewind(10)),
                    ("🎛️ Полный экран", self.youtube_fullscreen),
                ]
            },
            {
                "name": "🎵 SPOTIFY",
                "color": self.colors['accent_pink'],
                "commands": [
                    ("🎵 Spotify", self.open_spotify),
                    ("▶️ Воспроизвести", self.spotify_play),
                    ("⏸️ Пауза", self.spotify_pause),
                    ("⏭️ Следующий", self.spotify_next),
                    ("⏮️ Предыдущий", self.spotify_previous),
                ]
            }
        ]
        
        for i, category in enumerate(command_categories):
            row = i // 2
            col = i % 2
            self.create_category_card(container, category, row, col)

    def create_category_card(self, parent, category, row, col):
        card_frame = tk.Frame(parent, bg=self.colors['bg_light'], relief=tk.FLAT, bd=0)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)

        # Заголовок карточки
        header_frame = tk.Frame(card_frame, bg=category['color'], height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=category['name'], font=('Segoe UI', 12, 'bold'),
                bg=category['color'], fg=self.colors['bg_dark']).pack(expand=True)

        # Команды
        commands_frame = tk.Frame(card_frame, bg=self.colors['bg_light'])
        commands_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        for text, command in category["commands"]:
            btn = tk.Button(commands_frame,
                          text=text,
                          font=('Segoe UI', 9),
                          bg=self.colors['accent_purple'],
                          fg=self.colors['text_primary'],
                          width=18,
                          height=1,
                          relief=tk.FLAT,
                          bd=0,
                          cursor='hand2',
                          command=command)
            btn.pack(pady=3, fill=tk.X)

    def setup_log_tab(self, parent):
        log_container = tk.Frame(parent, bg=self.colors['bg_medium'])
        log_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        tk.Label(log_container, text="📊 СИСТЕМНЫЙ ЖУРНАЛ В РЕАЛЬНОМ ВРЕМЕНИ",
                font=('Segoe UI', 12, 'bold'), bg=self.colors['bg_medium'],
                fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(log_container,
                                                 bg=self.colors['bg_dark'],
                                                 fg=self.colors['accent_blue'],
                                                 font=('Cascadia Code', 10),
                                                 wrap=tk.WORD,
                                                 insertbackground=self.colors['accent_blue'],
                                                 relief=tk.FLAT,
                                                 bd=0)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def setup_voice_commands_tab(self, parent):
        commands_info = """
🎤 ГОЛОСОВЫЕ КОМАНДЫ (произнесите четко):

🖥️ СИСТЕМНЫЕ КОМАНДЫ:
• "Проводник" - открыть проводник
• "Настройки" - открыть настройки Windows
• "Блокировка" - заблокировать компьютер

🌐 БРАУЗЕР КОМАНДЫ:
• "Браузер" - открыть браузер
• "Новая вкладка" - открыть новую вкладку
• "Закрыть вкладку" - закрыть текущую вкладку
• "Следующая вкладка" - переключить на следующую вкладку
• "Предыдущая вкладка" - переключить на предыдущую вкладку
• "Обновить страницу" - обновить текущую страницу
• "Назад" - вернуться на предыдущую страницу
• "Вперед" - перейти вперед по истории
• "Закрыть браузер" - закрыть браузер

📺 YOUTUBE КОМАНДЫ:
• "Ютуб" - открыть YouTube
• "Ютуб пауза" - пауза видео
• "Ютуб играть" - продолжить видео
• "Ютуб перемотай 10" - перемотка на 10 сек вперед
• "Ютуб назад 10" - перемотка на 10 сек назад
• "Ютуб скорость 2" - скорость 2x
• "Ютуб скорость 1.5" - скорость 1.5x
• "Ютуб скорость 1" - нормальная скорость
• "Ютуб следующий" - следующее видео
• "Ютуб предыдущий" - предыдущее видео
• "Ютуб полноэкранный" - полный экран
• "Ютуб громче" - увеличить громкость
• "Ютуб тише" - уменьшить громкость

🎵 SPOTIFY КОМАНДЫ:
• "Спотіфай" - открыть Spotify
• "Спотіфай играть" - воспроизвести
• "Спотіфай пауза" - пауза
• "Спотіфай следующий" - следующий трек
• "Спотіфай предыдущий" - предыдущий трек
• "Спотіфай громче" - увеличить громкость
• "Спотіфай тише" - уменьшить громкость
"""
        text_container = tk.Frame(parent, bg=self.colors['bg_medium'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        commands_text = scrolledtext.ScrolledText(text_container,
                                                 bg=self.colors['bg_dark'],
                                                 fg=self.colors['text_secondary'],
                                                 font=('Cascadia Code', 11),
                                                 wrap=tk.WORD,
                                                 relief=tk.FLAT,
                                                 bd=0)
        commands_text.pack(fill=tk.BOTH, expand=True)
        commands_text.insert(tk.END, commands_info)
        commands_text.config(state=tk.DISABLED)

    def animate_visualizer(self):
        if hasattr(self, 'visualizer_canvas'):
            self.visualizer_canvas.delete("all")
            width = 200
            height = 50
            
            # Фон
            self.visualizer_canvas.create_rectangle(0, 0, width, height, 
                                                   fill=self.colors['bg_light'], outline="")
            
            if self.is_listening:
                # Анимация при прослушивании
                for i in range(8):
                    amplitude = math.sin(time.time() * 8 + i * 0.8) * 4 + 6
                    x = i * 25 + 12
                    color = [self.colors['accent_pink'], self.colors['accent_purple']][i % 2]
                    
                    self.visualizer_canvas.create_rectangle(
                        x - 8, height/2 - amplitude,
                        x + 8, height/2 + amplitude,
                        fill=color, outline=""
                    )
            else:
                # Статичная анимация
                for i in range(8):
                    x = i * 25 + 12
                    self.visualizer_canvas.create_rectangle(
                        x - 4, height/2 - 2,
                        x + 4, height/2 + 2,
                        fill=self.colors['text_secondary'], outline=""
                    )
            
            self.root.after(100, self.animate_visualizer)

    def log_message(self, message, msg_type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        colors = {
            "success": self.colors['accent_green'],
            "warning": self.colors['accent_orange'],
            "error": self.colors['accent_red'],
            "info": self.colors['accent_blue']
        }
        
        color = colors.get(msg_type, self.colors['accent_blue'])
        
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{message}\n", msg_type)
        
        self.log_text.tag_configure("timestamp", foreground=self.colors['text_secondary'])
        self.log_text.tag_configure(msg_type, foreground=color)
        
        self.log_text.see(tk.END)
        self.root.update()

    def speak(self, text):
        self.log_message(f"🔊 ОЗВУЧКА: {text}")
        
        if self.tts_engine and not self.is_speaking:
            self.is_speaking = True
            
            def speak_thread():
                try:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                except Exception as e:
                    self.log_message(f"Ошибка озвучивания: {e}", "error")
                finally:
                    self.is_speaking = False
            
            threading.Thread(target=speak_thread, daemon=True).start()
        elif not TTS_AVAILABLE:
            messagebox.showinfo("Ассистент", text)

    def listen_voice(self):
        if not self.speech_available:
            return ""
            
        try:
            with self.microphone as source:
                self.log_message("👂 Слушаю...", "info")
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=6)
            
            text = self.recognizer.recognize_google(audio, language="ru-RU").lower()
            self.log_message(f"🎯 Распознано: {text}", "success")
            return text
            
        except sr.WaitTimeoutError:
            self.log_message("⏰ Время ожидания истекло", "warning")
            return ""
        except sr.UnknownValueError:
            self.log_message("❌ Речь не распознана", "warning")
            return ""
        except Exception as e:
            self.log_message(f"❌ Ошибка распознавания: {e}", "error")
            return ""

    def start_voice_listening(self):
        if self.is_listening or not self.speech_available:
            return
            
        self.is_listening = True
        self.listen_btn.config(state=tk.DISABLED, bg=self.colors['text_secondary'])
        self.stop_btn.config(state=tk.NORMAL, bg=self.colors['accent_red'])
        
        self.log_message("🎤 Голосовое управление активировано", "success")
        self.speak("Голосовое управление активировано. Говорите команду.")
        
        def listen_loop():
            while self.is_listening:
                command = self.listen_voice()
                if command and self.is_listening:
                    self.process_voice_command(command)
                time.sleep(1)
        
        threading.Thread(target=listen_loop, daemon=True).start()

    def stop_voice_listening(self):
        self.is_listening = False
        self.listen_btn.config(state=tk.NORMAL, bg=self.colors['accent_purple'])
        self.stop_btn.config(state=tk.DISABLED, bg=self.colors['text_secondary'])
        
        self.log_message("⏹️ Голосовое управление остановлено", "info")
        self.speak("Голосовое управление отключено")

    def extract_number(self, text):
        """Извлечь число из текста команды"""
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else None

    def extract_speed(self, text):
        """Извлечь скорость из текста команды"""
        speeds = re.findall(r'\d+\.?\d*', text)
        return float(speeds[0]) if speeds else 1.0

    def process_voice_command(self, command):
        command = command.lower()
        self.log_message(f"🔍 Обрабатываю команду: {command}", "info")
        
        # Системные команды
        if any(word in command for word in ['проводник', 'explorer']):
            self.open_explorer()
        elif any(word in command for word in ['настройки', 'settings']):
            self.open_settings()
        elif any(word in command for word in ['блокировка', 'lock']):
            self.lock_pc()
            
        # Браузер команды
        elif any(word in command for word in ['браузер', 'browser']):
            self.open_browser()
        elif 'новая вкладка' in command:
            self.browser_new_tab()
        elif 'закрыть вкладку' in command:
            self.browser_close_tab()
        elif 'следующая вкладка' in command:
            self.browser_next_tab()
        elif 'предыдущая вкладка' in command:
            self.browser_previous_tab()
        elif 'обновить страницу' in command:
            self.browser_refresh()
        elif 'назад' in command and 'вкладк' not in command:
            self.browser_back()
        elif 'вперед' in command:
            self.browser_forward()
        elif 'закрыть браузер' in command:
            self.browser_close()
            
        # YouTube команды
        elif any(word in command for word in ['ютуб', 'youtube']):
            if 'пауза' in command:
                self.youtube_pause()
            elif 'играть' in command or 'продолжить' in command:
                self.youtube_play()
            elif 'перемотай' in command or 'вперед' in command:
                seconds = self.extract_number(command)
                self.youtube_skip(seconds or 10)
            elif 'назад' in command or 'верни' in command:
                seconds = self.extract_number(command)
                self.youtube_rewind(seconds or 10)
            elif 'скорость' in command:
                speed = self.extract_speed(command)
                self.youtube_speed(speed)
            elif 'следующий' in command:
                self.youtube_next()
            elif 'предыдущий' in command:
                self.youtube_previous()
            elif 'полноэкранный' in command or 'полный экран' in command:
                self.youtube_fullscreen()
            elif 'громче' in command:
                self.volume_up()
            elif 'тише' in command:
                self.volume_down()
            else:
                self.open_youtube()
                
        # Spotify команды
        elif any(word in command for word in ['спотифай', 'spotify']):
            if 'играть' in command or 'включи' in command:
                self.spotify_play()
            elif 'пауза' in command or 'останови' in command:
                self.spotify_pause()
            elif 'следующий' in command:
                self.spotify_next()
            elif 'предыдущий' in command:
                self.spotify_previous()
            elif 'громче' in command:
                self.volume_up()
            elif 'тише' in command:
                self.volume_down()
            else:
                self.open_spotify()
                
        else:
            self.speak("Команда не распознана")

    # СИСТЕМНЫЕ КОМАНДЫ
    def open_explorer(self):
        os.system("explorer")
        self.speak("Открываю проводник")
        self.log_message("📁 Проводник запущен", "success")

    def open_settings(self):
        os.system("start ms-settings:")
        self.speak("Открываю настройки")
        self.log_message("⚙️ Настройки открыты", "success")

    def lock_pc(self):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        self.speak("Блокирую компьютер")
        self.log_message("🔒 Компьютер заблокирован", "success")

    # БРАУЗЕР КОМАНДЫ
    def open_browser(self):
        webbrowser.open("https://google.com")
        self.speak("Открываю браузер")
        self.log_message("🌐 Браузер открыт", "success")

    def browser_new_tab(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', 't')
            self.speak("Новая вкладка")
            self.log_message("🌐 Новая вкладка открыта", "success")

    def browser_close_tab(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', 'w')
            self.speak("Закрываю вкладку")
            self.log_message("🌐 Вкладка закрыта", "success")

    def browser_next_tab(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', 'tab')
            self.speak("Следующая вкладка")
            self.log_message("🌐 Переключено на следующую вкладку", "success")

    def browser_previous_tab(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('ctrl', 'shift', 'tab')
            self.speak("Предыдущая вкладка")
            self.log_message("🌐 Переключено на предыдущую вкладку", "success")

    def browser_refresh(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('f5')
            self.speak("Обновляю страницу")
            self.log_message("🌐 Страница обновлена", "success")

    def browser_back(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('alt', 'left')
            self.speak("Назад")
            self.log_message("🌐 Навигация назад", "success")

    def browser_forward(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('alt', 'right')
            self.speak("Вперед")
            self.log_message("🌐 Навигация вперед", "success")

    def browser_close(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('alt', 'f4')
            self.speak("Закрываю браузер")
            self.log_message("🌐 Браузер закрыт", "success")

    # YOUTUBE КОМАНДЫ
    def open_youtube(self):
        webbrowser.open("https://youtube.com")
        self.speak("Открываю YouTube")
        self.log_message("📺 YouTube открыт", "success")

    def youtube_pause(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('k')
            self.speak("Пауза на YouTube")
            self.log_message("⏸️ YouTube на паузе", "success")

    def youtube_play(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('k')
            self.speak("Продолжаю YouTube")
            self.log_message("▶️ YouTube воспроизведение", "success")

    def youtube_skip(self, seconds=10):
        if PYAUTOGUI_AVAILABLE:
            for _ in range(seconds):
                pyautogui.press('right')
            self.speak(f"Перематываю на {seconds} секунд")
            self.log_message(f"⏩ YouTube перемотка вперед на {seconds} сек", "success")

    def youtube_rewind(self, seconds=10):
        if PYAUTOGUI_AVAILABLE:
            for _ in range(seconds):
                pyautogui.press('left')
            self.speak(f"Перематываю на {seconds} секунд назад")
            self.log_message(f"⏪ YouTube перемотка назад на {seconds} сек", "success")

    def youtube_speed(self, speed=1.0):
        if PYAUTOGUI_AVAILABLE:
            # Установка скорости через горячие клавиши
            pyautogui.hotkey('shift', '>')  # Увеличить скорость
            self.speak(f"Скорость {speed}")
            self.log_message(f"🎚️ YouTube скорость {speed}x", "success")

    def youtube_next(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('shift', 'n')
            self.speak("Следующее видео")
            self.log_message("⏭️ Следующее видео YouTube", "success")

    def youtube_previous(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.hotkey('shift', 'p')
            self.speak("Предыдущее видео")
            self.log_message("⏮️ Предыдущее видео YouTube", "success")

    def youtube_fullscreen(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('f')
            self.speak("Полноэкранный режим")
            self.log_message("📺 YouTube полноэкранный режим", "success")

    # SPOTIFY КОМАНДЫ
    def open_spotify(self):
        try:
            # Пробуем разные способы запуска
            try:
                os.system("start spotify:")  # URI схема
            except:
                os.system("spotify")  # Прямой запуск
            
            self.speak("Запускаю Spotify")
            self.log_message("🎵 Spotify запущен", "success")
            time.sleep(2)  # Даем время на запуск
            
        except Exception as e:
            self.log_message(f"❌ Ошибка Spotify: {e}", "error")
            self.speak("Ошибка запуска Spotify")

    def spotify_play(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('playpause')
            self.speak("Включаю Spotify")
            self.log_message("🎵 Spotify воспроизведение", "success")

    def spotify_pause(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('playpause')
            self.speak("Пауза в Spotify")
            self.log_message("⏸️ Spotify на паузе", "success")

    def spotify_next(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('nexttrack')
            self.speak("Следующий трек")
            self.log_message("⏭️ Следующий трек Spotify", "success")

    def spotify_previous(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('prevtrack')
            self.speak("Предыдущий трек")
            self.log_message("⏮️ Предыдущий трек Spotify", "success")

    # ОБЩИЕ КОМАНДЫ
    def volume_up(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('volumeup')
            self.speak("Громче")
            self.log_message("🔊 Громкость увеличена", "success")

    def volume_down(self):
        if PYAUTOGUI_AVAILABLE:
            pyautogui.press('volumedown')
            self.speak("Тише")
            self.log_message("🔈 Громкость уменьшена", "success")

def main():
    try:
        root = tk.Tk()
        app = UltraModernVoiceAssistant(root)
        
        # Центрирование окна
        root.update_idletasks()
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) // 2
        root.geometry(f"+{x}+{y}")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Ошибка запуска: {e}")

if __name__ == "__main__":
    main()