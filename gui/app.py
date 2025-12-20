"""
🖥️ AI Toolkit GUI — Tkinter приложение

Графический интерфейс для AI Toolkit.
Позволяет создавать, очищать и управлять проектами через UI.
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Callable
import threading

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.constants import VERSION, TEMPLATES, IDE_CONFIGS
from src.core.config import set_default_ide, get_default_ai_targets
from src.commands.create import create_project
from src.commands.cleanup import analyze_project, cleanup_project
from src.commands.health import health_check
from src.commands.migrate import migrate_project


# ══════════════════════════════════════════════════════════════
# Цвета и стили
# ══════════════════════════════════════════════════════════════

COLORS = {
    "bg": "#1e1e2e",           # Catppuccin Mocha Base
    "bg_secondary": "#313244",  # Surface0
    "fg": "#cdd6f4",           # Text
    "accent": "#89b4fa",       # Blue
    "success": "#a6e3a1",      # Green
    "warning": "#f9e2af",      # Yellow
    "error": "#f38ba8",        # Red
    "border": "#45475a",       # Surface1
}

FONTS = {
    "heading": ("Segoe UI", 16, "bold"),
    "subheading": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "mono": ("Consolas", 10),
}


# ══════════════════════════════════════════════════════════════
# Главное окно
# ══════════════════════════════════════════════════════════════

class AIToolkitApp:
    """Главное приложение AI Toolkit"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"🛠️ AI Toolkit v{VERSION}")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS["bg"])
        
        # Стили
        self.setup_styles()
        
        # Переменные
        self.selected_ide = tk.StringVar(value="all")
        self.selected_template = tk.StringVar(value="bot")
        self.project_name = tk.StringVar(value="my_project")
        self.project_path = tk.StringVar(value=str(Path.home()))
        self.include_docker = tk.BooleanVar(value=True)
        self.include_ci = tk.BooleanVar(value=True)
        self.include_git = tk.BooleanVar(value=True)
        
        # UI
        self.create_ui()
    
    def setup_styles(self):
        """Настройка стилей ttk"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Frame
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Secondary.TFrame", background=COLORS["bg_secondary"])
        
        # Label
        style.configure(
            "TLabel",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        style.configure(
            "Heading.TLabel",
            font=FONTS["heading"],
        )
        style.configure(
            "Subheading.TLabel",
            font=FONTS["subheading"],
        )
        
        # Button
        style.configure(
            "TButton",
            background=COLORS["accent"],
            foreground=COLORS["bg"],
            font=FONTS["body"],
            padding=(20, 10),
        )
        style.configure(
            "Success.TButton",
            background=COLORS["success"],
        )
        style.configure(
            "Danger.TButton",
            background=COLORS["error"],
        )
        
        # Entry
        style.configure(
            "TEntry",
            fieldbackground=COLORS["bg_secondary"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Radiobutton
        style.configure(
            "TRadiobutton",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Checkbutton
        style.configure(
            "TCheckbutton",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Notebook
        style.configure(
            "TNotebook",
            background=COLORS["bg"],
        )
        style.configure(
            "TNotebook.Tab",
            background=COLORS["bg_secondary"],
            foreground=COLORS["fg"],
            padding=(20, 10),
        )
    
    def create_ui(self):
        """Создание UI"""
        # Заголовок
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(
            header,
            text="🛠️ AI Toolkit",
            style="Heading.TLabel",
        ).pack(side="left")
        
        ttk.Label(
            header,
            text=f"v{VERSION}",
            foreground=COLORS["accent"],
        ).pack(side="left", padx=10)
        
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tab 1: Create
        create_frame = ttk.Frame(notebook)
        notebook.add(create_frame, text="🆕 Создать проект")
        self.create_create_tab(create_frame)
        
        # Tab 2: Cleanup
        cleanup_frame = ttk.Frame(notebook)
        notebook.add(cleanup_frame, text="🧹 Очистка")
        self.create_cleanup_tab(cleanup_frame)
        
        # Tab 3: Health
        health_frame = ttk.Frame(notebook)
        notebook.add(health_frame, text="🏥 Health Check")
        self.create_health_tab(health_frame)
        
        # Tab 4: Settings
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Настройки")
        self.create_settings_tab(settings_frame)
    
    def create_create_tab(self, parent: ttk.Frame):
        """Вкладка создания проекта"""
        # Название проекта
        name_frame = ttk.Frame(parent)
        name_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(name_frame, text="📁 Название проекта:").pack(anchor="w")
        ttk.Entry(
            name_frame,
            textvariable=self.project_name,
            width=40,
        ).pack(fill="x", pady=5)
        
        # Путь
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(path_frame, text="📍 Путь:").pack(anchor="w")
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill="x", pady=5)
        
        ttk.Entry(
            path_input_frame,
            textvariable=self.project_path,
            width=40,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_input_frame,
            text="📂",
            command=self.browse_path,
            width=3,
        ).pack(side="left", padx=5)
        
        # Шаблон
        template_frame = ttk.Frame(parent)
        template_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(template_frame, text="📦 Шаблон:", style="Subheading.TLabel").pack(anchor="w")
        
        for key, tmpl in TEMPLATES.items():
            ttk.Radiobutton(
                template_frame,
                text=f"{tmpl['icon']} {tmpl['name']} — {tmpl['description']}",
                variable=self.selected_template,
                value=key,
            ).pack(anchor="w", pady=2)
        
        # Опции
        options_frame = ttk.Frame(parent)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(options_frame, text="⚙️ Опции:", style="Subheading.TLabel").pack(anchor="w")
        
        ttk.Checkbutton(
            options_frame,
            text="🐳 Docker (Dockerfile + docker-compose)",
            variable=self.include_docker,
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame,
            text="🚀 CI/CD (GitHub Actions)",
            variable=self.include_ci,
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame,
            text="🔗 Git (init + первый коммит)",
            variable=self.include_git,
        ).pack(anchor="w", pady=2)
        
        # Кнопка создания
        ttk.Button(
            parent,
            text="✨ Создать проект",
            command=self.do_create_project,
            style="Success.TButton",
        ).pack(pady=20)
    
    def create_cleanup_tab(self, parent: ttk.Frame):
        """Вкладка очистки"""
        ttk.Label(
            parent,
            text="🧹 Очистка грязных проектов",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        ttk.Label(
            parent,
            text="Анализирует проект и находит:\n"
                 "• venv внутри проекта\n"
                 "• Большие логи и данные\n"
                 "• Отсутствующие конфиги",
        ).pack(pady=10)
        
        self.cleanup_path = tk.StringVar()
        
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Entry(
            path_frame,
            textvariable=self.cleanup_path,
            width=50,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_frame,
            text="📂",
            command=lambda: self.browse_folder(self.cleanup_path),
            width=3,
        ).pack(side="left", padx=5)
        
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        ttk.Button(
            buttons_frame,
            text="🔍 Анализировать",
            command=self.do_analyze,
        ).pack(side="left", padx=10)
        
        ttk.Button(
            buttons_frame,
            text="🧹 Очистить (medium)",
            command=lambda: self.do_cleanup("medium"),
        ).pack(side="left", padx=10)
        
        # Результаты
        self.cleanup_results = tk.Text(
            parent,
            height=15,
            bg=COLORS["bg_secondary"],
            fg=COLORS["fg"],
            font=FONTS["mono"],
        )
        self.cleanup_results.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_health_tab(self, parent: ttk.Frame):
        """Вкладка health check"""
        ttk.Label(
            parent,
            text="🏥 Health Check",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        self.health_path = tk.StringVar()
        
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Entry(
            path_frame,
            textvariable=self.health_path,
            width=50,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_frame,
            text="📂",
            command=lambda: self.browse_folder(self.health_path),
            width=3,
        ).pack(side="left", padx=5)
        
        ttk.Button(
            parent,
            text="🏥 Проверить",
            command=self.do_health_check,
        ).pack(pady=20)
        
        # Результаты
        self.health_results = tk.Text(
            parent,
            height=15,
            bg=COLORS["bg_secondary"],
            fg=COLORS["fg"],
            font=FONTS["mono"],
        )
        self.health_results.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_settings_tab(self, parent: ttk.Frame):
        """Вкладка настроек"""
        ttk.Label(
            parent,
            text="⚙️ Настройки",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        # IDE
        ide_frame = ttk.Frame(parent)
        ide_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(ide_frame, text="🖥️ IDE по умолчанию:").pack(anchor="w")
        
        for key, cfg in IDE_CONFIGS.items():
            ttk.Radiobutton(
                ide_frame,
                text=f"{cfg['icon']} {cfg['name']}",
                variable=self.selected_ide,
                value=key,
            ).pack(anchor="w", pady=2)
        
        ttk.Button(
            parent,
            text="💾 Сохранить",
            command=self.save_settings,
        ).pack(pady=20)
    
    # ══════════════════════════════════════════════════════════════
    # Обработчики
    # ══════════════════════════════════════════════════════════════
    
    def browse_path(self):
        """Выбор папки для проекта"""
        path = filedialog.askdirectory(initialdir=self.project_path.get())
        if path:
            self.project_path.set(path)
    
    def browse_folder(self, var: tk.StringVar):
        """Выбор папки"""
        path = filedialog.askdirectory()
        if path:
            var.set(path)
    
    def do_create_project(self):
        """Создать проект"""
        name = self.project_name.get().strip()
        path = Path(self.project_path.get())
        
        if not name:
            messagebox.showerror("Ошибка", "Введите название проекта")
            return
        
        if not name.replace('_', '').replace('-', '').isalnum():
            messagebox.showerror("Ошибка", "Название: только буквы, цифры, _ и -")
            return
        
        if (path / name).exists():
            messagebox.showerror("Ошибка", f"Папка {path / name} уже существует")
            return
        
        # Установка IDE
        ide = self.selected_ide.get()
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        
        # Создание в отдельном потоке
        def create():
            try:
                result = create_project(
                    name=name,
                    path=path,
                    template=self.selected_template.get(),
                    ai_targets=cfg["ai_targets"],
                    include_docker=self.include_docker.get(),
                    include_ci=self.include_ci.get(),
                    include_git=self.include_git.get(),
                )
                
                if result:
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Успех",
                        f"✅ Проект {name} создан!\n\n"
                        f"Путь: {path / name}\n\n"
                        f"Следующие шаги:\n"
                        f"1. cd {path / name}\n"
                        f"2. ./scripts/bootstrap.sh\n"
                        f"3. source ../_venvs/{name}-venv/bin/activate"
                    ))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Ошибка", "Не удалось создать проект"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
        
        threading.Thread(target=create, daemon=True).start()
    
    def do_analyze(self):
        """Анализ проекта"""
        path = Path(self.cleanup_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        self.cleanup_results.delete("1.0", "end")
        
        issues = analyze_project(path)
        
        if not issues:
            self.cleanup_results.insert("end", "✅ Проект чистый! Проблем не найдено.\n")
        else:
            self.cleanup_results.insert("end", f"Найдено {len(issues)} проблем:\n\n")
            for issue in issues:
                self.cleanup_results.insert("end", f"  {issue}\n")
    
    def do_cleanup(self, level: str):
        """Очистка проекта"""
        path = Path(self.cleanup_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        if not messagebox.askyesno("Подтверждение", f"Очистить {path.name}?\nУровень: {level}"):
            return
        
        result = cleanup_project(path, level)
        
        if result:
            messagebox.showinfo("Успех", "Очистка завершена!")
            self.do_analyze()  # Обновить результаты
        else:
            messagebox.showerror("Ошибка", "Ошибка очистки")
    
    def do_health_check(self):
        """Health check"""
        path = Path(self.health_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        self.health_results.delete("1.0", "end")
        
        # Перехватываем вывод
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        try:
            result = health_check(path)
        finally:
            output = buffer.getvalue()
            sys.stdout = old_stdout
        
        # Убираем ANSI коды
        import re
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', output)
        
        self.health_results.insert("end", clean_output)
    
    def save_settings(self):
        """Сохранить настройки"""
        ide = self.selected_ide.get()
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        messagebox.showinfo("Настройки", f"IDE: {cfg['icon']} {cfg['name']}")
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


# ══════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════

def run_gui():
    """Запустить GUI приложение"""
    app = AIToolkitApp()
    app.run()


if __name__ == "__main__":
    run_gui()


🖥️ AI Toolkit GUI — Tkinter приложение

Графический интерфейс для AI Toolkit.
Позволяет создавать, очищать и управлять проектами через UI.
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Callable
import threading

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.constants import VERSION, TEMPLATES, IDE_CONFIGS
from src.core.config import set_default_ide, get_default_ai_targets
from src.commands.create import create_project
from src.commands.cleanup import analyze_project, cleanup_project
from src.commands.health import health_check
from src.commands.migrate import migrate_project


# ══════════════════════════════════════════════════════════════
# Цвета и стили
# ══════════════════════════════════════════════════════════════

COLORS = {
    "bg": "#1e1e2e",           # Catppuccin Mocha Base
    "bg_secondary": "#313244",  # Surface0
    "fg": "#cdd6f4",           # Text
    "accent": "#89b4fa",       # Blue
    "success": "#a6e3a1",      # Green
    "warning": "#f9e2af",      # Yellow
    "error": "#f38ba8",        # Red
    "border": "#45475a",       # Surface1
}

FONTS = {
    "heading": ("Segoe UI", 16, "bold"),
    "subheading": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "mono": ("Consolas", 10),
}


# ══════════════════════════════════════════════════════════════
# Главное окно
# ══════════════════════════════════════════════════════════════

class AIToolkitApp:
    """Главное приложение AI Toolkit"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"🛠️ AI Toolkit v{VERSION}")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS["bg"])
        
        # Стили
        self.setup_styles()
        
        # Переменные
        self.selected_ide = tk.StringVar(value="all")
        self.selected_template = tk.StringVar(value="bot")
        self.project_name = tk.StringVar(value="my_project")
        self.project_path = tk.StringVar(value=str(Path.home()))
        self.include_docker = tk.BooleanVar(value=True)
        self.include_ci = tk.BooleanVar(value=True)
        self.include_git = tk.BooleanVar(value=True)
        
        # UI
        self.create_ui()
    
    def setup_styles(self):
        """Настройка стилей ttk"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Frame
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Secondary.TFrame", background=COLORS["bg_secondary"])
        
        # Label
        style.configure(
            "TLabel",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        style.configure(
            "Heading.TLabel",
            font=FONTS["heading"],
        )
        style.configure(
            "Subheading.TLabel",
            font=FONTS["subheading"],
        )
        
        # Button
        style.configure(
            "TButton",
            background=COLORS["accent"],
            foreground=COLORS["bg"],
            font=FONTS["body"],
            padding=(20, 10),
        )
        style.configure(
            "Success.TButton",
            background=COLORS["success"],
        )
        style.configure(
            "Danger.TButton",
            background=COLORS["error"],
        )
        
        # Entry
        style.configure(
            "TEntry",
            fieldbackground=COLORS["bg_secondary"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Radiobutton
        style.configure(
            "TRadiobutton",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Checkbutton
        style.configure(
            "TCheckbutton",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Notebook
        style.configure(
            "TNotebook",
            background=COLORS["bg"],
        )
        style.configure(
            "TNotebook.Tab",
            background=COLORS["bg_secondary"],
            foreground=COLORS["fg"],
            padding=(20, 10),
        )
    
    def create_ui(self):
        """Создание UI"""
        # Заголовок
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(
            header,
            text="🛠️ AI Toolkit",
            style="Heading.TLabel",
        ).pack(side="left")
        
        ttk.Label(
            header,
            text=f"v{VERSION}",
            foreground=COLORS["accent"],
        ).pack(side="left", padx=10)
        
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tab 1: Create
        create_frame = ttk.Frame(notebook)
        notebook.add(create_frame, text="🆕 Создать проект")
        self.create_create_tab(create_frame)
        
        # Tab 2: Cleanup
        cleanup_frame = ttk.Frame(notebook)
        notebook.add(cleanup_frame, text="🧹 Очистка")
        self.create_cleanup_tab(cleanup_frame)
        
        # Tab 3: Health
        health_frame = ttk.Frame(notebook)
        notebook.add(health_frame, text="🏥 Health Check")
        self.create_health_tab(health_frame)
        
        # Tab 4: Settings
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Настройки")
        self.create_settings_tab(settings_frame)
    
    def create_create_tab(self, parent: ttk.Frame):
        """Вкладка создания проекта"""
        # Название проекта
        name_frame = ttk.Frame(parent)
        name_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(name_frame, text="📁 Название проекта:").pack(anchor="w")
        ttk.Entry(
            name_frame,
            textvariable=self.project_name,
            width=40,
        ).pack(fill="x", pady=5)
        
        # Путь
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(path_frame, text="📍 Путь:").pack(anchor="w")
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill="x", pady=5)
        
        ttk.Entry(
            path_input_frame,
            textvariable=self.project_path,
            width=40,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_input_frame,
            text="📂",
            command=self.browse_path,
            width=3,
        ).pack(side="left", padx=5)
        
        # Шаблон
        template_frame = ttk.Frame(parent)
        template_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(template_frame, text="📦 Шаблон:", style="Subheading.TLabel").pack(anchor="w")
        
        for key, tmpl in TEMPLATES.items():
            ttk.Radiobutton(
                template_frame,
                text=f"{tmpl['icon']} {tmpl['name']} — {tmpl['description']}",
                variable=self.selected_template,
                value=key,
            ).pack(anchor="w", pady=2)
        
        # Опции
        options_frame = ttk.Frame(parent)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(options_frame, text="⚙️ Опции:", style="Subheading.TLabel").pack(anchor="w")
        
        ttk.Checkbutton(
            options_frame,
            text="🐳 Docker (Dockerfile + docker-compose)",
            variable=self.include_docker,
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame,
            text="🚀 CI/CD (GitHub Actions)",
            variable=self.include_ci,
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame,
            text="🔗 Git (init + первый коммит)",
            variable=self.include_git,
        ).pack(anchor="w", pady=2)
        
        # Кнопка создания
        ttk.Button(
            parent,
            text="✨ Создать проект",
            command=self.do_create_project,
            style="Success.TButton",
        ).pack(pady=20)
    
    def create_cleanup_tab(self, parent: ttk.Frame):
        """Вкладка очистки"""
        ttk.Label(
            parent,
            text="🧹 Очистка грязных проектов",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        ttk.Label(
            parent,
            text="Анализирует проект и находит:\n"
                 "• venv внутри проекта\n"
                 "• Большие логи и данные\n"
                 "• Отсутствующие конфиги",
        ).pack(pady=10)
        
        self.cleanup_path = tk.StringVar()
        
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Entry(
            path_frame,
            textvariable=self.cleanup_path,
            width=50,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_frame,
            text="📂",
            command=lambda: self.browse_folder(self.cleanup_path),
            width=3,
        ).pack(side="left", padx=5)
        
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        ttk.Button(
            buttons_frame,
            text="🔍 Анализировать",
            command=self.do_analyze,
        ).pack(side="left", padx=10)
        
        ttk.Button(
            buttons_frame,
            text="🧹 Очистить (medium)",
            command=lambda: self.do_cleanup("medium"),
        ).pack(side="left", padx=10)
        
        # Результаты
        self.cleanup_results = tk.Text(
            parent,
            height=15,
            bg=COLORS["bg_secondary"],
            fg=COLORS["fg"],
            font=FONTS["mono"],
        )
        self.cleanup_results.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_health_tab(self, parent: ttk.Frame):
        """Вкладка health check"""
        ttk.Label(
            parent,
            text="🏥 Health Check",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        self.health_path = tk.StringVar()
        
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Entry(
            path_frame,
            textvariable=self.health_path,
            width=50,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_frame,
            text="📂",
            command=lambda: self.browse_folder(self.health_path),
            width=3,
        ).pack(side="left", padx=5)
        
        ttk.Button(
            parent,
            text="🏥 Проверить",
            command=self.do_health_check,
        ).pack(pady=20)
        
        # Результаты
        self.health_results = tk.Text(
            parent,
            height=15,
            bg=COLORS["bg_secondary"],
            fg=COLORS["fg"],
            font=FONTS["mono"],
        )
        self.health_results.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_settings_tab(self, parent: ttk.Frame):
        """Вкладка настроек"""
        ttk.Label(
            parent,
            text="⚙️ Настройки",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        # IDE
        ide_frame = ttk.Frame(parent)
        ide_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(ide_frame, text="🖥️ IDE по умолчанию:").pack(anchor="w")
        
        for key, cfg in IDE_CONFIGS.items():
            ttk.Radiobutton(
                ide_frame,
                text=f"{cfg['icon']} {cfg['name']}",
                variable=self.selected_ide,
                value=key,
            ).pack(anchor="w", pady=2)
        
        ttk.Button(
            parent,
            text="💾 Сохранить",
            command=self.save_settings,
        ).pack(pady=20)
    
    # ══════════════════════════════════════════════════════════════
    # Обработчики
    # ══════════════════════════════════════════════════════════════
    
    def browse_path(self):
        """Выбор папки для проекта"""
        path = filedialog.askdirectory(initialdir=self.project_path.get())
        if path:
            self.project_path.set(path)
    
    def browse_folder(self, var: tk.StringVar):
        """Выбор папки"""
        path = filedialog.askdirectory()
        if path:
            var.set(path)
    
    def do_create_project(self):
        """Создать проект"""
        name = self.project_name.get().strip()
        path = Path(self.project_path.get())
        
        if not name:
            messagebox.showerror("Ошибка", "Введите название проекта")
            return
        
        if not name.replace('_', '').replace('-', '').isalnum():
            messagebox.showerror("Ошибка", "Название: только буквы, цифры, _ и -")
            return
        
        if (path / name).exists():
            messagebox.showerror("Ошибка", f"Папка {path / name} уже существует")
            return
        
        # Установка IDE
        ide = self.selected_ide.get()
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        
        # Создание в отдельном потоке
        def create():
            try:
                result = create_project(
                    name=name,
                    path=path,
                    template=self.selected_template.get(),
                    ai_targets=cfg["ai_targets"],
                    include_docker=self.include_docker.get(),
                    include_ci=self.include_ci.get(),
                    include_git=self.include_git.get(),
                )
                
                if result:
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Успех",
                        f"✅ Проект {name} создан!\n\n"
                        f"Путь: {path / name}\n\n"
                        f"Следующие шаги:\n"
                        f"1. cd {path / name}\n"
                        f"2. ./scripts/bootstrap.sh\n"
                        f"3. source ../_venvs/{name}-venv/bin/activate"
                    ))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Ошибка", "Не удалось создать проект"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
        
        threading.Thread(target=create, daemon=True).start()
    
    def do_analyze(self):
        """Анализ проекта"""
        path = Path(self.cleanup_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        self.cleanup_results.delete("1.0", "end")
        
        issues = analyze_project(path)
        
        if not issues:
            self.cleanup_results.insert("end", "✅ Проект чистый! Проблем не найдено.\n")
        else:
            self.cleanup_results.insert("end", f"Найдено {len(issues)} проблем:\n\n")
            for issue in issues:
                self.cleanup_results.insert("end", f"  {issue}\n")
    
    def do_cleanup(self, level: str):
        """Очистка проекта"""
        path = Path(self.cleanup_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        if not messagebox.askyesno("Подтверждение", f"Очистить {path.name}?\nУровень: {level}"):
            return
        
        result = cleanup_project(path, level)
        
        if result:
            messagebox.showinfo("Успех", "Очистка завершена!")
            self.do_analyze()  # Обновить результаты
        else:
            messagebox.showerror("Ошибка", "Ошибка очистки")
    
    def do_health_check(self):
        """Health check"""
        path = Path(self.health_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        self.health_results.delete("1.0", "end")
        
        # Перехватываем вывод
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        try:
            result = health_check(path)
        finally:
            output = buffer.getvalue()
            sys.stdout = old_stdout
        
        # Убираем ANSI коды
        import re
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', output)
        
        self.health_results.insert("end", clean_output)
    
    def save_settings(self):
        """Сохранить настройки"""
        ide = self.selected_ide.get()
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        messagebox.showinfo("Настройки", f"IDE: {cfg['icon']} {cfg['name']}")
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


# ══════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════

def run_gui():
    """Запустить GUI приложение"""
    app = AIToolkitApp()
    app.run()


if __name__ == "__main__":
    run_gui()


🖥️ AI Toolkit GUI — Tkinter приложение

Графический интерфейс для AI Toolkit.
Позволяет создавать, очищать и управлять проектами через UI.
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Callable
import threading

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.constants import VERSION, TEMPLATES, IDE_CONFIGS
from src.core.config import set_default_ide, get_default_ai_targets
from src.commands.create import create_project
from src.commands.cleanup import analyze_project, cleanup_project
from src.commands.health import health_check
from src.commands.migrate import migrate_project


# ══════════════════════════════════════════════════════════════
# Цвета и стили
# ══════════════════════════════════════════════════════════════

COLORS = {
    "bg": "#1e1e2e",           # Catppuccin Mocha Base
    "bg_secondary": "#313244",  # Surface0
    "fg": "#cdd6f4",           # Text
    "accent": "#89b4fa",       # Blue
    "success": "#a6e3a1",      # Green
    "warning": "#f9e2af",      # Yellow
    "error": "#f38ba8",        # Red
    "border": "#45475a",       # Surface1
}

FONTS = {
    "heading": ("Segoe UI", 16, "bold"),
    "subheading": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "mono": ("Consolas", 10),
}


# ══════════════════════════════════════════════════════════════
# Главное окно
# ══════════════════════════════════════════════════════════════

class AIToolkitApp:
    """Главное приложение AI Toolkit"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"🛠️ AI Toolkit v{VERSION}")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS["bg"])
        
        # Стили
        self.setup_styles()
        
        # Переменные
        self.selected_ide = tk.StringVar(value="all")
        self.selected_template = tk.StringVar(value="bot")
        self.project_name = tk.StringVar(value="my_project")
        self.project_path = tk.StringVar(value=str(Path.home()))
        self.include_docker = tk.BooleanVar(value=True)
        self.include_ci = tk.BooleanVar(value=True)
        self.include_git = tk.BooleanVar(value=True)
        
        # UI
        self.create_ui()
    
    def setup_styles(self):
        """Настройка стилей ttk"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Frame
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Secondary.TFrame", background=COLORS["bg_secondary"])
        
        # Label
        style.configure(
            "TLabel",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        style.configure(
            "Heading.TLabel",
            font=FONTS["heading"],
        )
        style.configure(
            "Subheading.TLabel",
            font=FONTS["subheading"],
        )
        
        # Button
        style.configure(
            "TButton",
            background=COLORS["accent"],
            foreground=COLORS["bg"],
            font=FONTS["body"],
            padding=(20, 10),
        )
        style.configure(
            "Success.TButton",
            background=COLORS["success"],
        )
        style.configure(
            "Danger.TButton",
            background=COLORS["error"],
        )
        
        # Entry
        style.configure(
            "TEntry",
            fieldbackground=COLORS["bg_secondary"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Radiobutton
        style.configure(
            "TRadiobutton",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Checkbutton
        style.configure(
            "TCheckbutton",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Notebook
        style.configure(
            "TNotebook",
            background=COLORS["bg"],
        )
        style.configure(
            "TNotebook.Tab",
            background=COLORS["bg_secondary"],
            foreground=COLORS["fg"],
            padding=(20, 10),
        )
    
    def create_ui(self):
        """Создание UI"""
        # Заголовок
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(
            header,
            text="🛠️ AI Toolkit",
            style="Heading.TLabel",
        ).pack(side="left")
        
        ttk.Label(
            header,
            text=f"v{VERSION}",
            foreground=COLORS["accent"],
        ).pack(side="left", padx=10)
        
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tab 1: Create
        create_frame = ttk.Frame(notebook)
        notebook.add(create_frame, text="🆕 Создать проект")
        self.create_create_tab(create_frame)
        
        # Tab 2: Cleanup
        cleanup_frame = ttk.Frame(notebook)
        notebook.add(cleanup_frame, text="🧹 Очистка")
        self.create_cleanup_tab(cleanup_frame)
        
        # Tab 3: Health
        health_frame = ttk.Frame(notebook)
        notebook.add(health_frame, text="🏥 Health Check")
        self.create_health_tab(health_frame)
        
        # Tab 4: Settings
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Настройки")
        self.create_settings_tab(settings_frame)
    
    def create_create_tab(self, parent: ttk.Frame):
        """Вкладка создания проекта"""
        # Название проекта
        name_frame = ttk.Frame(parent)
        name_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(name_frame, text="📁 Название проекта:").pack(anchor="w")
        ttk.Entry(
            name_frame,
            textvariable=self.project_name,
            width=40,
        ).pack(fill="x", pady=5)
        
        # Путь
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(path_frame, text="📍 Путь:").pack(anchor="w")
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill="x", pady=5)
        
        ttk.Entry(
            path_input_frame,
            textvariable=self.project_path,
            width=40,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_input_frame,
            text="📂",
            command=self.browse_path,
            width=3,
        ).pack(side="left", padx=5)
        
        # Шаблон
        template_frame = ttk.Frame(parent)
        template_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(template_frame, text="📦 Шаблон:", style="Subheading.TLabel").pack(anchor="w")
        
        for key, tmpl in TEMPLATES.items():
            ttk.Radiobutton(
                template_frame,
                text=f"{tmpl['icon']} {tmpl['name']} — {tmpl['description']}",
                variable=self.selected_template,
                value=key,
            ).pack(anchor="w", pady=2)
        
        # Опции
        options_frame = ttk.Frame(parent)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(options_frame, text="⚙️ Опции:", style="Subheading.TLabel").pack(anchor="w")
        
        ttk.Checkbutton(
            options_frame,
            text="🐳 Docker (Dockerfile + docker-compose)",
            variable=self.include_docker,
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame,
            text="🚀 CI/CD (GitHub Actions)",
            variable=self.include_ci,
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame,
            text="🔗 Git (init + первый коммит)",
            variable=self.include_git,
        ).pack(anchor="w", pady=2)
        
        # Кнопка создания
        ttk.Button(
            parent,
            text="✨ Создать проект",
            command=self.do_create_project,
            style="Success.TButton",
        ).pack(pady=20)
    
    def create_cleanup_tab(self, parent: ttk.Frame):
        """Вкладка очистки"""
        ttk.Label(
            parent,
            text="🧹 Очистка грязных проектов",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        ttk.Label(
            parent,
            text="Анализирует проект и находит:\n"
                 "• venv внутри проекта\n"
                 "• Большие логи и данные\n"
                 "• Отсутствующие конфиги",
        ).pack(pady=10)
        
        self.cleanup_path = tk.StringVar()
        
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Entry(
            path_frame,
            textvariable=self.cleanup_path,
            width=50,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_frame,
            text="📂",
            command=lambda: self.browse_folder(self.cleanup_path),
            width=3,
        ).pack(side="left", padx=5)
        
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        ttk.Button(
            buttons_frame,
            text="🔍 Анализировать",
            command=self.do_analyze,
        ).pack(side="left", padx=10)
        
        ttk.Button(
            buttons_frame,
            text="🧹 Очистить (medium)",
            command=lambda: self.do_cleanup("medium"),
        ).pack(side="left", padx=10)
        
        # Результаты
        self.cleanup_results = tk.Text(
            parent,
            height=15,
            bg=COLORS["bg_secondary"],
            fg=COLORS["fg"],
            font=FONTS["mono"],
        )
        self.cleanup_results.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_health_tab(self, parent: ttk.Frame):
        """Вкладка health check"""
        ttk.Label(
            parent,
            text="🏥 Health Check",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        self.health_path = tk.StringVar()
        
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Entry(
            path_frame,
            textvariable=self.health_path,
            width=50,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_frame,
            text="📂",
            command=lambda: self.browse_folder(self.health_path),
            width=3,
        ).pack(side="left", padx=5)
        
        ttk.Button(
            parent,
            text="🏥 Проверить",
            command=self.do_health_check,
        ).pack(pady=20)
        
        # Результаты
        self.health_results = tk.Text(
            parent,
            height=15,
            bg=COLORS["bg_secondary"],
            fg=COLORS["fg"],
            font=FONTS["mono"],
        )
        self.health_results.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_settings_tab(self, parent: ttk.Frame):
        """Вкладка настроек"""
        ttk.Label(
            parent,
            text="⚙️ Настройки",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        # IDE
        ide_frame = ttk.Frame(parent)
        ide_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(ide_frame, text="🖥️ IDE по умолчанию:").pack(anchor="w")
        
        for key, cfg in IDE_CONFIGS.items():
            ttk.Radiobutton(
                ide_frame,
                text=f"{cfg['icon']} {cfg['name']}",
                variable=self.selected_ide,
                value=key,
            ).pack(anchor="w", pady=2)
        
        ttk.Button(
            parent,
            text="💾 Сохранить",
            command=self.save_settings,
        ).pack(pady=20)
    
    # ══════════════════════════════════════════════════════════════
    # Обработчики
    # ══════════════════════════════════════════════════════════════
    
    def browse_path(self):
        """Выбор папки для проекта"""
        path = filedialog.askdirectory(initialdir=self.project_path.get())
        if path:
            self.project_path.set(path)
    
    def browse_folder(self, var: tk.StringVar):
        """Выбор папки"""
        path = filedialog.askdirectory()
        if path:
            var.set(path)
    
    def do_create_project(self):
        """Создать проект"""
        name = self.project_name.get().strip()
        path = Path(self.project_path.get())
        
        if not name:
            messagebox.showerror("Ошибка", "Введите название проекта")
            return
        
        if not name.replace('_', '').replace('-', '').isalnum():
            messagebox.showerror("Ошибка", "Название: только буквы, цифры, _ и -")
            return
        
        if (path / name).exists():
            messagebox.showerror("Ошибка", f"Папка {path / name} уже существует")
            return
        
        # Установка IDE
        ide = self.selected_ide.get()
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        
        # Создание в отдельном потоке
        def create():
            try:
                result = create_project(
                    name=name,
                    path=path,
                    template=self.selected_template.get(),
                    ai_targets=cfg["ai_targets"],
                    include_docker=self.include_docker.get(),
                    include_ci=self.include_ci.get(),
                    include_git=self.include_git.get(),
                )
                
                if result:
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Успех",
                        f"✅ Проект {name} создан!\n\n"
                        f"Путь: {path / name}\n\n"
                        f"Следующие шаги:\n"
                        f"1. cd {path / name}\n"
                        f"2. ./scripts/bootstrap.sh\n"
                        f"3. source ../_venvs/{name}-venv/bin/activate"
                    ))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Ошибка", "Не удалось создать проект"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
        
        threading.Thread(target=create, daemon=True).start()
    
    def do_analyze(self):
        """Анализ проекта"""
        path = Path(self.cleanup_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        self.cleanup_results.delete("1.0", "end")
        
        issues = analyze_project(path)
        
        if not issues:
            self.cleanup_results.insert("end", "✅ Проект чистый! Проблем не найдено.\n")
        else:
            self.cleanup_results.insert("end", f"Найдено {len(issues)} проблем:\n\n")
            for issue in issues:
                self.cleanup_results.insert("end", f"  {issue}\n")
    
    def do_cleanup(self, level: str):
        """Очистка проекта"""
        path = Path(self.cleanup_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        if not messagebox.askyesno("Подтверждение", f"Очистить {path.name}?\nУровень: {level}"):
            return
        
        result = cleanup_project(path, level)
        
        if result:
            messagebox.showinfo("Успех", "Очистка завершена!")
            self.do_analyze()  # Обновить результаты
        else:
            messagebox.showerror("Ошибка", "Ошибка очистки")
    
    def do_health_check(self):
        """Health check"""
        path = Path(self.health_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        self.health_results.delete("1.0", "end")
        
        # Перехватываем вывод
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        try:
            result = health_check(path)
        finally:
            output = buffer.getvalue()
            sys.stdout = old_stdout
        
        # Убираем ANSI коды
        import re
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', output)
        
        self.health_results.insert("end", clean_output)
    
    def save_settings(self):
        """Сохранить настройки"""
        ide = self.selected_ide.get()
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        messagebox.showinfo("Настройки", f"IDE: {cfg['icon']} {cfg['name']}")
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


# ══════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════

def run_gui():
    """Запустить GUI приложение"""
    app = AIToolkitApp()
    app.run()


if __name__ == "__main__":
    run_gui()


🖥️ AI Toolkit GUI — Tkinter приложение

Графический интерфейс для AI Toolkit.
Позволяет создавать, очищать и управлять проектами через UI.
"""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Callable
import threading

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.constants import VERSION, TEMPLATES, IDE_CONFIGS
from src.core.config import set_default_ide, get_default_ai_targets
from src.commands.create import create_project
from src.commands.cleanup import analyze_project, cleanup_project
from src.commands.health import health_check
from src.commands.migrate import migrate_project


# ══════════════════════════════════════════════════════════════
# Цвета и стили
# ══════════════════════════════════════════════════════════════

COLORS = {
    "bg": "#1e1e2e",           # Catppuccin Mocha Base
    "bg_secondary": "#313244",  # Surface0
    "fg": "#cdd6f4",           # Text
    "accent": "#89b4fa",       # Blue
    "success": "#a6e3a1",      # Green
    "warning": "#f9e2af",      # Yellow
    "error": "#f38ba8",        # Red
    "border": "#45475a",       # Surface1
}

FONTS = {
    "heading": ("Segoe UI", 16, "bold"),
    "subheading": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "mono": ("Consolas", 10),
}


# ══════════════════════════════════════════════════════════════
# Главное окно
# ══════════════════════════════════════════════════════════════

class AIToolkitApp:
    """Главное приложение AI Toolkit"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"🛠️ AI Toolkit v{VERSION}")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS["bg"])
        
        # Стили
        self.setup_styles()
        
        # Переменные
        self.selected_ide = tk.StringVar(value="all")
        self.selected_template = tk.StringVar(value="bot")
        self.project_name = tk.StringVar(value="my_project")
        self.project_path = tk.StringVar(value=str(Path.home()))
        self.include_docker = tk.BooleanVar(value=True)
        self.include_ci = tk.BooleanVar(value=True)
        self.include_git = tk.BooleanVar(value=True)
        
        # UI
        self.create_ui()
    
    def setup_styles(self):
        """Настройка стилей ttk"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Frame
        style.configure("TFrame", background=COLORS["bg"])
        style.configure("Secondary.TFrame", background=COLORS["bg_secondary"])
        
        # Label
        style.configure(
            "TLabel",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        style.configure(
            "Heading.TLabel",
            font=FONTS["heading"],
        )
        style.configure(
            "Subheading.TLabel",
            font=FONTS["subheading"],
        )
        
        # Button
        style.configure(
            "TButton",
            background=COLORS["accent"],
            foreground=COLORS["bg"],
            font=FONTS["body"],
            padding=(20, 10),
        )
        style.configure(
            "Success.TButton",
            background=COLORS["success"],
        )
        style.configure(
            "Danger.TButton",
            background=COLORS["error"],
        )
        
        # Entry
        style.configure(
            "TEntry",
            fieldbackground=COLORS["bg_secondary"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Radiobutton
        style.configure(
            "TRadiobutton",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Checkbutton
        style.configure(
            "TCheckbutton",
            background=COLORS["bg"],
            foreground=COLORS["fg"],
            font=FONTS["body"],
        )
        
        # Notebook
        style.configure(
            "TNotebook",
            background=COLORS["bg"],
        )
        style.configure(
            "TNotebook.Tab",
            background=COLORS["bg_secondary"],
            foreground=COLORS["fg"],
            padding=(20, 10),
        )
    
    def create_ui(self):
        """Создание UI"""
        # Заголовок
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(
            header,
            text="🛠️ AI Toolkit",
            style="Heading.TLabel",
        ).pack(side="left")
        
        ttk.Label(
            header,
            text=f"v{VERSION}",
            foreground=COLORS["accent"],
        ).pack(side="left", padx=10)
        
        # Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tab 1: Create
        create_frame = ttk.Frame(notebook)
        notebook.add(create_frame, text="🆕 Создать проект")
        self.create_create_tab(create_frame)
        
        # Tab 2: Cleanup
        cleanup_frame = ttk.Frame(notebook)
        notebook.add(cleanup_frame, text="🧹 Очистка")
        self.create_cleanup_tab(cleanup_frame)
        
        # Tab 3: Health
        health_frame = ttk.Frame(notebook)
        notebook.add(health_frame, text="🏥 Health Check")
        self.create_health_tab(health_frame)
        
        # Tab 4: Settings
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Настройки")
        self.create_settings_tab(settings_frame)
    
    def create_create_tab(self, parent: ttk.Frame):
        """Вкладка создания проекта"""
        # Название проекта
        name_frame = ttk.Frame(parent)
        name_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(name_frame, text="📁 Название проекта:").pack(anchor="w")
        ttk.Entry(
            name_frame,
            textvariable=self.project_name,
            width=40,
        ).pack(fill="x", pady=5)
        
        # Путь
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(path_frame, text="📍 Путь:").pack(anchor="w")
        
        path_input_frame = ttk.Frame(path_frame)
        path_input_frame.pack(fill="x", pady=5)
        
        ttk.Entry(
            path_input_frame,
            textvariable=self.project_path,
            width=40,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_input_frame,
            text="📂",
            command=self.browse_path,
            width=3,
        ).pack(side="left", padx=5)
        
        # Шаблон
        template_frame = ttk.Frame(parent)
        template_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(template_frame, text="📦 Шаблон:", style="Subheading.TLabel").pack(anchor="w")
        
        for key, tmpl in TEMPLATES.items():
            ttk.Radiobutton(
                template_frame,
                text=f"{tmpl['icon']} {tmpl['name']} — {tmpl['description']}",
                variable=self.selected_template,
                value=key,
            ).pack(anchor="w", pady=2)
        
        # Опции
        options_frame = ttk.Frame(parent)
        options_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(options_frame, text="⚙️ Опции:", style="Subheading.TLabel").pack(anchor="w")
        
        ttk.Checkbutton(
            options_frame,
            text="🐳 Docker (Dockerfile + docker-compose)",
            variable=self.include_docker,
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame,
            text="🚀 CI/CD (GitHub Actions)",
            variable=self.include_ci,
        ).pack(anchor="w", pady=2)
        
        ttk.Checkbutton(
            options_frame,
            text="🔗 Git (init + первый коммит)",
            variable=self.include_git,
        ).pack(anchor="w", pady=2)
        
        # Кнопка создания
        ttk.Button(
            parent,
            text="✨ Создать проект",
            command=self.do_create_project,
            style="Success.TButton",
        ).pack(pady=20)
    
    def create_cleanup_tab(self, parent: ttk.Frame):
        """Вкладка очистки"""
        ttk.Label(
            parent,
            text="🧹 Очистка грязных проектов",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        ttk.Label(
            parent,
            text="Анализирует проект и находит:\n"
                 "• venv внутри проекта\n"
                 "• Большие логи и данные\n"
                 "• Отсутствующие конфиги",
        ).pack(pady=10)
        
        self.cleanup_path = tk.StringVar()
        
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Entry(
            path_frame,
            textvariable=self.cleanup_path,
            width=50,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_frame,
            text="📂",
            command=lambda: self.browse_folder(self.cleanup_path),
            width=3,
        ).pack(side="left", padx=5)
        
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(pady=20)
        
        ttk.Button(
            buttons_frame,
            text="🔍 Анализировать",
            command=self.do_analyze,
        ).pack(side="left", padx=10)
        
        ttk.Button(
            buttons_frame,
            text="🧹 Очистить (medium)",
            command=lambda: self.do_cleanup("medium"),
        ).pack(side="left", padx=10)
        
        # Результаты
        self.cleanup_results = tk.Text(
            parent,
            height=15,
            bg=COLORS["bg_secondary"],
            fg=COLORS["fg"],
            font=FONTS["mono"],
        )
        self.cleanup_results.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_health_tab(self, parent: ttk.Frame):
        """Вкладка health check"""
        ttk.Label(
            parent,
            text="🏥 Health Check",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        self.health_path = tk.StringVar()
        
        path_frame = ttk.Frame(parent)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Entry(
            path_frame,
            textvariable=self.health_path,
            width=50,
        ).pack(side="left", fill="x", expand=True)
        
        ttk.Button(
            path_frame,
            text="📂",
            command=lambda: self.browse_folder(self.health_path),
            width=3,
        ).pack(side="left", padx=5)
        
        ttk.Button(
            parent,
            text="🏥 Проверить",
            command=self.do_health_check,
        ).pack(pady=20)
        
        # Результаты
        self.health_results = tk.Text(
            parent,
            height=15,
            bg=COLORS["bg_secondary"],
            fg=COLORS["fg"],
            font=FONTS["mono"],
        )
        self.health_results.pack(fill="both", expand=True, padx=20, pady=10)
    
    def create_settings_tab(self, parent: ttk.Frame):
        """Вкладка настроек"""
        ttk.Label(
            parent,
            text="⚙️ Настройки",
            style="Subheading.TLabel",
        ).pack(pady=20)
        
        # IDE
        ide_frame = ttk.Frame(parent)
        ide_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(ide_frame, text="🖥️ IDE по умолчанию:").pack(anchor="w")
        
        for key, cfg in IDE_CONFIGS.items():
            ttk.Radiobutton(
                ide_frame,
                text=f"{cfg['icon']} {cfg['name']}",
                variable=self.selected_ide,
                value=key,
            ).pack(anchor="w", pady=2)
        
        ttk.Button(
            parent,
            text="💾 Сохранить",
            command=self.save_settings,
        ).pack(pady=20)
    
    # ══════════════════════════════════════════════════════════════
    # Обработчики
    # ══════════════════════════════════════════════════════════════
    
    def browse_path(self):
        """Выбор папки для проекта"""
        path = filedialog.askdirectory(initialdir=self.project_path.get())
        if path:
            self.project_path.set(path)
    
    def browse_folder(self, var: tk.StringVar):
        """Выбор папки"""
        path = filedialog.askdirectory()
        if path:
            var.set(path)
    
    def do_create_project(self):
        """Создать проект"""
        name = self.project_name.get().strip()
        path = Path(self.project_path.get())
        
        if not name:
            messagebox.showerror("Ошибка", "Введите название проекта")
            return
        
        if not name.replace('_', '').replace('-', '').isalnum():
            messagebox.showerror("Ошибка", "Название: только буквы, цифры, _ и -")
            return
        
        if (path / name).exists():
            messagebox.showerror("Ошибка", f"Папка {path / name} уже существует")
            return
        
        # Установка IDE
        ide = self.selected_ide.get()
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        
        # Создание в отдельном потоке
        def create():
            try:
                result = create_project(
                    name=name,
                    path=path,
                    template=self.selected_template.get(),
                    ai_targets=cfg["ai_targets"],
                    include_docker=self.include_docker.get(),
                    include_ci=self.include_ci.get(),
                    include_git=self.include_git.get(),
                )
                
                if result:
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Успех",
                        f"✅ Проект {name} создан!\n\n"
                        f"Путь: {path / name}\n\n"
                        f"Следующие шаги:\n"
                        f"1. cd {path / name}\n"
                        f"2. ./scripts/bootstrap.sh\n"
                        f"3. source ../_venvs/{name}-venv/bin/activate"
                    ))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Ошибка", "Не удалось создать проект"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
        
        threading.Thread(target=create, daemon=True).start()
    
    def do_analyze(self):
        """Анализ проекта"""
        path = Path(self.cleanup_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        self.cleanup_results.delete("1.0", "end")
        
        issues = analyze_project(path)
        
        if not issues:
            self.cleanup_results.insert("end", "✅ Проект чистый! Проблем не найдено.\n")
        else:
            self.cleanup_results.insert("end", f"Найдено {len(issues)} проблем:\n\n")
            for issue in issues:
                self.cleanup_results.insert("end", f"  {issue}\n")
    
    def do_cleanup(self, level: str):
        """Очистка проекта"""
        path = Path(self.cleanup_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        if not messagebox.askyesno("Подтверждение", f"Очистить {path.name}?\nУровень: {level}"):
            return
        
        result = cleanup_project(path, level)
        
        if result:
            messagebox.showinfo("Успех", "Очистка завершена!")
            self.do_analyze()  # Обновить результаты
        else:
            messagebox.showerror("Ошибка", "Ошибка очистки")
    
    def do_health_check(self):
        """Health check"""
        path = Path(self.health_path.get())
        
        if not path.exists():
            messagebox.showerror("Ошибка", "Путь не существует")
            return
        
        self.health_results.delete("1.0", "end")
        
        # Перехватываем вывод
        import io
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        try:
            result = health_check(path)
        finally:
            output = buffer.getvalue()
            sys.stdout = old_stdout
        
        # Убираем ANSI коды
        import re
        clean_output = re.sub(r'\x1b\[[0-9;]*m', '', output)
        
        self.health_results.insert("end", clean_output)
    
    def save_settings(self):
        """Сохранить настройки"""
        ide = self.selected_ide.get()
        cfg = IDE_CONFIGS[ide]
        set_default_ide(ide, cfg["ai_targets"])
        messagebox.showinfo("Настройки", f"IDE: {cfg['icon']} {cfg['name']}")
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


# ══════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════

def run_gui():
    """Запустить GUI приложение"""
    app = AIToolkitApp()
    app.run()


if __name__ == "__main__":
    run_gui()

