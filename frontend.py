import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from backend import StudyTrackerDB

class StudyTrackerApp:
    def __init__(self, root):
        self.root = root
        self.db = StudyTrackerDB()
        self.settings = {
            'language': self.db.get_setting('language', 'en'),
            'theme': self.db.get_setting('theme', 'light')
        }
        
        self.translations = {
            'en': {
                'title': "Study Hours Tracker",
                'date': "Date (YYYY-MM-DD):",
                'hours': "Hours studied:",
                'add': "Add",
                'total': "Current week total:",
                'history': "View History",
                'history_title': "Study History",
                'settings': "Settings",
                'language': "Language",
                'theme': "Theme",
                'light': "Light",
                'dark': "Dark",
                'english': "English",
                'spanish': "Spanish",
                'error_date': "Invalid date format",
                'error_hours': "Invalid hours value",
                'dup_entry': "Duplicate entry for date:",
                'success': "Entry added successfully",
                'week': "Week",
                'year': "Year",
                'no_data': "No data available",
                'reset_button': "🧹 Reset All Data",
                'reset_confirm1': "Are you sure you want to delete ALL study records?",
                'reset_confirm2': "This action cannot be undone. Confirm deletion:",
                'reset_success': "All data has been successfully deleted",
                'warning': "Warning"
            },
            'es': {
                'title': "Registro de Horas de Estudio",
                'date': "Fecha (AAAA-MM-DD):",
                'hours': "Horas estudiadas:",
                'add': "Agregar",
                'total': "Total semana actual:",
                'history': "Ver Historial",
                'history_title': "Historial de Estudio",
                'settings': "Configuración",
                'language': "Idioma",
                'theme': "Tema",
                'light': "Claro",
                'dark': "Oscuro",
                'english': "Inglés",
                'spanish': "Español",
                'error_date': "Formato de fecha inválido",
                'error_hours': "Valor de horas inválido",
                'dup_entry': "Entrada duplicada para la fecha:",
                'success': "Registro agregado exitosamente",
                'week': "Semana",
                'year': "Año",
                'no_data': "Sin datos disponibles",
                'reset_button': "🧹 Borrar Todos los Datos",
                'reset_confirm1': "¿Estás seguro de borrar TODOS los registros de estudio?",
                'reset_confirm2': "Esta acción no se puede deshacer. Confirma el borrado:",
                'reset_success': "Todos los datos han sido eliminados exitosamente",
                'warning': "Advertencia"
            }
        }
        
        self.themes = {
            'light': {
                'bg': '#FFFFFF', 'fg': '#000000',
                'entry_bg': '#FFFFFF', 'frame_bg': '#F0F0F0',
                'button_bg': '#E0E0E0', 'hover_bg': '#D0D0D0',
                'tree_bg': '#FFFFFF', 'tree_fg': '#000000',
                'heading_bg': '#E0E0E0', 'heading_fg': '#000000',
                'danger_bg': '#dc3545', 'danger_hover': '#c82333'
            },
            'dark': {
                'bg': '#2D2D2D', 'fg': '#FFFFFF',
                'entry_bg': '#404040', 'frame_bg': '#3D3D3D',
                'button_bg': '#505050', 'hover_bg': '#606060',
                'tree_bg': '#404040', 'tree_fg': '#FFFFFF',
                'heading_bg': '#505050', 'heading_fg': '#FFFFFF',
                'danger_bg': '#bb2d3b', 'danger_hover': '#a52834'
            }
        }
        
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        self.root.title(self.translate('title'))
        self.root.geometry("500x400")
        
        # Menu
        self.menu_bar = tk.Menu(self.root)
        self.setup_menu()
        self.root.config(menu=self.menu_bar)
        
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Date entry
        self.date_label = ttk.Label(self.main_frame, text=self.translate('date'))
        self.date_label.grid(row=0, column=0, sticky='w', pady=5)
        
        self.date_entry = ttk.Entry(self.main_frame)
        self.date_entry.grid(row=0, column=1, sticky='ew', padx=5)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Hours entry
        self.hours_label = ttk.Label(self.main_frame, text=self.translate('hours'))
        self.hours_label.grid(row=1, column=0, sticky='w', pady=5)
        
        self.hours_entry = ttk.Entry(self.main_frame)
        self.hours_entry.grid(row=1, column=1, sticky='ew', padx=5)
        
        # Add button
        self.add_btn = ttk.Button(
            self.main_frame, 
            text=self.translate('add'), 
            command=self.add_hours
        )
        self.add_btn.grid(row=1, column=2, padx=5)
        
        # Stats
        self.stats_frame = ttk.LabelFrame(self.main_frame, text=self.translate('total'))
        self.stats_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=10)
        
        self.total_label = ttk.Label(self.stats_frame, text="0.00")
        self.total_label.pack(pady=5)
        
        # Button container
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=10)
        
        # History button
        self.history_btn = ttk.Button(
            button_frame,
            text=self.translate('history'),
            command=self.show_history
        )
        self.history_btn.pack(side='left', expand=True, fill='x', padx=2)
        
        # Reset button
        self.reset_btn = ttk.Button(
            button_frame,
            text=self.translate('reset_button'),
            command=self.confirm_reset,
            style='Danger.TButton'
        )
        self.reset_btn.pack(side='left', expand=True, fill='x', padx=2)
        
        self.update_total()
    
    def setup_menu(self):
        settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        
        # Language submenu
        lang_menu = tk.Menu(settings_menu, tearoff=0)
        lang_menu.add_radiobutton(
            label=self.translate('english'),
            command=lambda: self.change_language('en')
        )
        lang_menu.add_radiobutton(
            label=self.translate('spanish'),
            command=lambda: self.change_language('es')
        )
        
        # Theme submenu
        theme_menu = tk.Menu(settings_menu, tearoff=0)
        theme_menu.add_radiobutton(
            label=self.translate('light'),
            command=lambda: self.change_theme('light')
        )
        theme_menu.add_radiobutton(
            label=self.translate('dark'),
            command=lambda: self.change_theme('dark')
        )
        
        settings_menu.add_cascade(label=self.translate('language'), menu=lang_menu)
        settings_menu.add_cascade(label=self.translate('theme'), menu=theme_menu)
        self.menu_bar.add_cascade(label=self.translate('settings'), menu=settings_menu)
    
    def apply_theme(self):
        theme = self.themes[self.settings['theme']]
        style = ttk.Style()
        
        # Configure colors
        self.root.config(bg=theme['bg'])
        style.configure('.', 
            background=theme['bg'], 
            foreground=theme['fg'],
            fieldbackground=theme['entry_bg']
        )
        style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        style.configure('TFrame', background=theme['frame_bg'])
        style.configure('TLabelframe', background=theme['frame_bg'])
        style.configure('TLabelframe.Label', background=theme['frame_bg'], foreground=theme['fg'])
        style.configure('TButton', 
            background=theme['button_bg'],
            bordercolor=theme['button_bg'],
            lightcolor=theme['button_bg'],
            darkcolor=theme['button_bg'],
            foreground='black'
        )
        style.configure('Danger.TButton', 
            background=theme['button_bg'],
            foreground='black',
            bordercolor=theme['button_bg'],
            lightcolor=theme['button_bg'],
            darkcolor=theme['button_bg']
        )
        style.map('TButton',
            background=[('active', theme['hover_bg'])],
            bordercolor=[('active', theme['hover_bg'])],
            lightcolor=[('active', theme['hover_bg'])],
            darkcolor=[('active', theme['hover_bg'])],
           
        )
        style.map('Danger.TButton',
            background=[('active', theme['hover_bg'])],
            bordercolor=[('active', theme['hover_bg'])],
            lightcolor=[('active', theme['hover_bg'])],
            darkcolor=[('active', theme['hover_bg'])]
            
        )
    
    def apply_theme_to_window(self, window):
        theme = self.themes[self.settings['theme']]
        style = ttk.Style()
        
        window.config(bg=theme['bg'])
        style.configure('Treeview', 
            background=theme['tree_bg'],
            fieldbackground=theme['tree_bg'],
            foreground=theme['tree_fg']
        )
        style.configure('Treeview.Heading', 
            background=theme['heading_bg'],
            foreground=theme['heading_fg']
        )
        style.map('Treeview', 
            background=[('selected', theme['hover_bg'])]
        )
    
    def translate(self, key):
        return self.translations[self.settings['language']][key]
    
    def change_language(self, lang):
        self.settings['language'] = lang
        self.db.save_setting('language', lang)
        self.update_texts()
    
    def change_theme(self, theme):
        self.settings['theme'] = theme
        self.db.save_setting('theme', theme)
        self.apply_theme()
    
    def update_texts(self):
        self.root.title(self.translate('title'))
        self.date_label.config(text=self.translate('date'))
        self.hours_label.config(text=self.translate('hours'))
        self.add_btn.config(text=self.translate('add'))
        self.stats_frame.config(text=self.translate('total'))
        self.history_btn.config(text=self.translate('history'))
        self.reset_btn.config(text=self.translate('reset_button'))
    
    def add_hours(self):
        date = self.date_entry.get()
        hours = self.hours_entry.get()
        
        if not all([date, hours]):
            messagebox.showerror(
                self.translate('error'),
                self.translate('error_hours')
            )
            return
        
        try:
            success = self.db.add_hours(hours, date)
            if success:
                messagebox.showinfo(
                    self.translate('success'),
                    self.translate('success')
                )
                self.update_total()
                self.date_entry.delete(0, 'end')
                self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
                self.hours_entry.delete(0, 'end')
            else:
                messagebox.showerror(
                    self.translate('error'),
                    f"{self.translate('dup_entry')} {date}"
                )
        except Exception as e:
            messagebox.showerror(
                self.translate('error'),
                str(e)
            )
    
    def update_total(self):
        total = self.db.get_week_total()
        self.total_label.config(text=f"{total:.2f}")
    
    def show_history(self):
        history = self.db.get_history()
        
        history_win = tk.Toplevel(self.root)
        history_win.title(self.translate('history_title'))
        self.apply_theme_to_window(history_win)
        
        # Main container
        container = ttk.Frame(history_win)
        container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview
        tree = ttk.Treeview(
            container,
            columns=('week', 'year', 'hours'),
            show='headings',
            selectmode='browse'
        )
        
        # Configure columns
        tree.heading('week', text=self.translate('week'))
        tree.heading('year', text=self.translate('year'))
        tree.heading('hours', text=self.translate('hours'))
        
        tree.column('week', width=80, anchor='center')
        tree.column('year', width=80, anchor='center')
        tree.column('hours', width=100, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            container,
            orient='vertical',
            command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Configure grid weights
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Populate data
        if history:
            for entry in history:
                week, year, total = entry
                tree.insert('', 'end', values=(week, year, f"{total:.2f}"))
        else:
            tree.insert('', 'end', values=(self.translate('no_data'), '', ''))
        
        # Resize window
        history_win.minsize(300, 200)
    
    def confirm_reset(self):
        # Primera confirmación
        confirm1 = messagebox.askyesno(
            self.translate('warning'),
            self.translate('reset_confirm1')
        )
        if not confirm1:
            return
        
        # Segunda confirmación
        confirm2 = messagebox.askyesno(
            self.translate('warning'),
            self.translate('reset_confirm2')
        )
        if not confirm2:
            return
        
        # Ejecutar borrado
        self.db.reset_all_data()
        messagebox.showinfo(
            self.translate('success'),
            self.translate('reset_success')
        )
        self.update_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTrackerApp(root)
    root.mainloop()