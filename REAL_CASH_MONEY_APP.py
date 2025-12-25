#!/usr/bin/env python3
"""
REAL CASH MONEY COLORS AI BUSINESS APP
Professionelle Desktop-Anwendung für KI-Geschäftsautomatisierung
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, PhotoImage
import threading
import time
import sqlite3
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import webbrowser
import sys

class RealCashMoneyApp:
    """Professionelle Business-Desktop-App"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CASH MONEY AI BUSINESS SUITE v2.3 - Professional Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')

        # App-Variablen
        self.current_user = "Administrator"
        self.session_start = datetime.now()
        self.data_path = Path("business_data.db")
        self.config_path = Path("business_config.json")

        # Business-Daten
        self.revenue_data = {
            'total': 15467.89,
            'monthly': {'2025-12': 2347.89},
            'projects': {},
            'clients': []
        }

        self.project_types = [
            "AI Consultierung",
            "Marketing Automation",
            "Content Erstellung",
            "Software Entwicklung",
            "Business Intelligence"
        ]

        # UI Initialisierung
        self.setup_database()
        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.create_main_interface()
        self.load_config()

        # Start-Systemservices
        threading.Thread(target=self.auto_backup, daemon=True).start()
        threading.Thread(target=self.update_metrics, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.confirm_quit)
        # Nichts mehr ausgeben - App soll leise starten

    def setup_database(self):
        """Professionelle Datenbankstruktur setup"""
        try:
            self.conn = sqlite3.connect(self.data_path)
            cursor = self.conn.cursor()

            # Projekte-Tabelle
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT,
                    status TEXT DEFAULT 'Aktiv',
                    client_name TEXT,
                    start_date DATE,
                    budget REAL,
                    revenue REAL DEFAULT 0,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Aufgaben-Tabelle
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT DEFAULT 'Normal',
                    status TEXT DEFAULT 'Ausstehend',
                    assigned_to TEXT,
                    due_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )
            ''')

            # Umsatz-Tabelle
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS revenue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER,
                    amount REAL NOT NULL,
                    currency TEXT DEFAULT 'EUR',
                    description TEXT,
                    category TEXT,
                    payment_date DATE DEFAULT CURRENT_DATE,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Kunden-Tabelle
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    company TEXT,
                    address TEXT,
                    status TEXT DEFAULT 'Aktiv',
                    total_revenue REAL DEFAULT 0,
                    projects_count INTEGER DEFAULT 0,
                    added_date DATE DEFAULT CURRENT_DATE
                )
            ''')

            # Sample-Daten falls leer
            cursor.execute("SELECT COUNT(*) FROM projects")
            if cursor.fetchone()[0] == 0:
                self.insert_sample_data()

            self.conn.commit()

        except Exception as e:
            messagebox.showerror("Database Error", f"Database initialization failed: {e}")

    def insert_sample_data(self):
        """Echte Beispiel-Daten einspeisen"""
        projects = [
            ("KI Strategie-Beratung", "AI Consultierung", "TechCorp GmbH", "2025-12-01", 5000.00, "KI-Implementierung für mittelständisches Unternehmen"),
            ("Marketing Automation", "Marketing Automation", "StartupXYZ", "2025-11-15", 3500.00, "Automatisierte Social Media Vermarktung"),
            ("Content Creator Platform", "Content Erstellung", "MediaHub", "2025-10-20", 7500.00, "AI-basierte Content-Generierung Plattform"),
            ("Business Intelligence Dashboard", "Business Intelligence", "DataFlow Inc.", "2025-09-10", 12000.00, "Erweiterte BI-Lösung für Finanzanalyse"),
            ("Mobile App Entwicklung", "Software Entwicklung", "InnoTech", "2025-08-05", 15000.00, "Native Mobile-Anwendung mit AI-Integration")
        ]

        for project in projects:
            self.conn.execute('''
                INSERT INTO projects (name, type, client_name, start_date, budget, notes, revenue)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (*project, project[0] * 25))  # Revenue calculation

        # Kunden hinzufügen
        clients = [
            ("TechCorp GmbH", "info@techcorp.de", "+49-123-456789", "TechCorp GmbH", "München, Deutschland"),
            ("StartupXYZ", "contact@startupxyz.com", "+49-987-654321", "StartupXYZ GmbH", "Berlin, Deutschland"),
            ("MediaHub", "hello@mediahub.net", "+49-555-121212", "MediaHub Networks", "Frankfurt, Deutschland"),
            ("DataFlow Inc.", "support@dataflow.com", "+1-555-DATA", "DataFlow Inc.", "New York, USA"),
            ("InnoTech", "projects@innotech.eu", "+49-777-888999", "InnoTech Solutions", "Hamburg, Deutschland")
        ]

        for client in clients:
            self.conn.execute('''
                INSERT INTO clients (name, email, phone, company, address)
                VALUES (?, ?, ?, ?, ?)
            ''', client)

        # Beispiel-Aufgaben
        tasks = [
            (1, "KI-Architektur Analyse", "Projekt-Architektur durchführen", "Hoch", "2025-12-15"),
            (2, "Social Media Setup", "Automatisierte Posting-Infrastruktur aufbauen", "Mittel", "2025-11-30"),
            (3, "Content Strategie", "KI-Content-Generierung implementieren", "Hoch", "2025-12-20"),
            (4, "Data Integration", "Business-Daten mit BI-System verknüpfen", "Mittel", "2025-12-10"),
            (5, "App Design", "Mobile User Interface gestalten", "Mittel", "2025-12-25")
        ]

        for task in tasks:
            self.conn.execute('''
                INSERT INTO tasks (project_id, title, description, priority, due_date)
                VALUES (?, ?, ?, ?, ?)
            ''', task)

    def create_menu(self):
        """Professionelle Menüleiste"""
        menubar = tk.Menu(self.root)

        # Datei-Menü
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Neues Projekt", command=self.new_project, accelerator="Ctrl+N")
        file_menu.add_command(label="Projekt öffnen", command=self.open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Backup erstellen", command=self.create_backup)
        file_menu.add_SEPARATOR()
        file_menu.add_command(label="Beenden", command=self.confirm_quit)
        menubar.add_cascade(label="Datei", menu=file_menu)

        # Bearbeiten-Menü
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Rückgängig", accelerator="Ctrl+Z")
        edit_menu.add_SEPARATOR()
        edit_menu.add_command(label="Einstellungen", command=self.show_settings)
        menubar.add_cascade(label="Bearbeiten", menu=edit_menu)

        # Projekt-Menü
        project_menu = tk.Menu(menubar, tearoff=0)
        project_menu.add_command(label="Projekt-Manager", command=self.show_project_manager)
        project_menu.add_command(label="Aufgaben verwalten", command=self.show_task_manager)
        project_menu.add_command(label="Kunden-Datenbank", command=self.show_client_manager)
        project_menu.add_separator()
        project_menu.add_command(label="Berichte generieren", command=self.generate_reports)
        menubar.add_cascade(label="Projekte", menu=project_menu)

        # Finanzen-Menü
        finance_menu = tk.Menu(menubar, tearoff=0)
        finance_menu.add_command(label="Umsatz-Tracker", command=self.show_revenue_tracker)
        finance_menu.add_command(label="Budget-Planung", command=self.show_budget_planner)
        finance_menu.add_command(label="Steuerberichterstattung", command=self.show_tax_reports)
        finance_menu.add_separator()
        finance_menu.add_command(label="Finanz-Dashboard", command=self.show_finance_dashboard)
        menubar.add_cascade(label="Finanzen", menu=finance_menu)

        # Hilfe-Menü
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Online-Hilfe", command=lambda: webbrowser.open("https://cashmoney-ai.com/help"))
        help_menu.add_command(label="Support", command=lambda: webbrowser.open("mailto:support@cashmoney-ai.com"))
        help_menu.add_separator()
        help_menu.add_command(label="Über", command=self.show_about)
        menubar.add_cascade(label="Hilfe", menu=help_menu)

        self.root.config(menu=menubar)

        # Keyboard Shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_project())
        self.root.focus_force()

    def create_toolbar(self):
        """Professionele Toolbar"""
        toolbar = ttk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        # Buttons mit Bildern (würden normalerweise Bilder laden)
        buttons = [
            ("🆕", self.new_project, "Neues Projekt"),
            ("📁", self.open_project, "Projekt öffnen"),
            ("💾", self.create_backup, "Backup"),
            ("🧮", self.calculate_revenue, "Berechnen"),
            ("📊", self.generate_reports, "Berichte"),
            ("⚙️", self.show_settings, "Einstellungen")
        ]

        for text, command, tooltip in buttons:
            btn = tk.Button(toolbar, text=text, command=command, width=3,
                          font=('Arial', 12), relief=tk.RAISED)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

            # Tooltip
            self.create_tooltip(btn, tooltip)

        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Quick-Search
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side=tk.RIGHT, padx=5)

        ttk.Label(search_frame, text="Schnell-Suche:").pack(side=tk.LEFT)
        self.quick_search = ttk.Entry(search_frame, width=20)
        self.quick_search.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="🔍", width=3, command=self.perform_search).pack(side=tk.LEFT)

        self.root.bind('<Control-f>', lambda e: self.quick_search.focus())
        self.quick_search.bind('<Return>', lambda e: self.perform_search())

    def create_tooltip(self, widget, text):
        """Tooltip-Funktionalität"""
        def on_enter(event):
            self.tooltip = tk.Toplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(self.tooltip, text=text, justify=tk.LEFT,
                           background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                           font=("Tahoma", "8", "normal"))
            label.pack()

        def on_leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()

        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)

    def create_statusbar(self):
        """Professionelle Statusleiste"""
        self.status_frame = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Links: Status
        self.status_var = tk.StringVar()
        self.status_var.set("Bereit")
        ttk.Label(self.status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=5)

        # Rechts: System-Info
        info_frame = ttk.Frame(self.status_frame)
        info_frame.pack(side=tk.RIGHT, padx=5)

        self.time_var = tk.StringVar()
        self.time_var.set(datetime.now().strftime("%H:%M:%S"))
        ttk.Label(info_frame, textvariable=self.time_var).pack(side=tk.RIGHT, padx=10)

        self.user_var = tk.StringVar()
        self.user_var.set(f"Benutzer: {self.current_user}")
        ttk.Label(info_frame, textvariable=self.user_var).pack(side=tk.RIGHT, padx=10)

        # Update-Zeit
        self.update_clock()

    def update_clock(self):
        """Live-Uhr in Statusleiste"""
        self.time_var.set(datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.update_clock)

    def create_main_interface(self):
        """Haupt-Interface mit Tabs"""
        # Haupt-Container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Linke Seitenleiste
        self.left_sidebar = ttk.Frame(main_container, width=250)
        main_container.add(self.left_sidebar, weight=0)

        # Rechter Hauptbereich
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=1)

        # Seitenleiste füllen
        self.create_sidebar()

        # Haupt-Tab-Interface
        self.create_main_tabs(right_panel)

    def create_sidebar(self):
        """Professionelle Seitenleiste"""
        # Titel
        sidebar_title = ttk.Label(self.left_sidebar, text="NAVIGATION",
                                font=('Arial', 11, 'bold'))
        sidebar_title.pack(pady=10)

        # Projekte-Sektion
        projects_label = ttk.Label(self.left_sidebar, text="AKTIVE PROJEKTE",
                                 font=('Arial', 9, 'bold'), foreground='blue')
        projects_label.pack(anchor=tk.W, padx=10, pady=(10,5))

        # Projekt-Liste (Treeview)
        self.project_tree = ttk.Treeview(self.left_sidebar, height=8, selectmode='browse')
        self.project_tree.heading('#0', text='Projekte')

        # Beispiel-Einträge hinzufügen
        root_node = self.project_tree.insert('', 'end', text='Alle Projekte')

        projects = ["KI Strategie-Beratung", "Marketing Automation", "Content Creator Platform"]
        for project in projects:
            self.project_tree.insert(root_node, 'end', text=project)

        self.project_tree.pack(fill=tk.X, padx=10, pady=(0,10))

        # Quick-Stats
        stats_frame = ttk.LabelFrame(self.left_sidebar, text="SCHNELLSTATS", padding=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=10)

        self.sidebar_stats = {}
        stat_items = [
            ("Aktive Projekte:", "5"),
            ("Ausstehende Aufgaben:", "12"),
            ("Heute Umsatz:", "€634.75"),
            ("Monat Ziel:", "€15,000")
        ]

        for label, value in stat_items:
            row = ttk.Frame(stats_frame)
            row.pack(fill=tk.X, pady=1)
            ttk.Label(row, text=label, font=('Arial', 8)).pack(side=tk.LEFT)
            self.sidebar_stats[label] = ttk.Label(row, text=value, font=('Arial', 8, 'bold'),
                                                 foreground='green')
            self.sidebar_stats[label].pack(side=tk.RIGHT)

        # Quick-Actions
        actions_frame = ttk.Frame(self.left_sidebar)
        actions_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(actions_frame, text="+ NEUE AUFGABE",
                  command=self.quick_add_task).pack(fill=tk.X, pady=2)

        ttk.Button(actions_frame, text="📞 KUNDE HINZUFÜGEN",
                  command=self.quick_add_client).pack(fill=tk.X, pady=2)

    def create_main_tabs(self, parent):
        """Haupt-Tabs Interface"""
        self.main_notebook = ttk.Notebook(parent)
        self.main_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Dashboard Tab
        dashboard_frame = self.create_dashboard_tab()
        self.main_notebook.add(dashboard_frame, text="📊 Dashboard")

        # Projekte Tab
        projects_frame = self.create_projects_tab()
        self.main_notebook.add(projects_frame, text="💼 Projekte")

        # Finanzen Tab
        finance_frame = self.create_finance_tab()
        self.main_notebook.add(finance_frame, text="💰 Finanzen")

        # Berichte Tab
        reports_frame = self.create_reports_tab()
        self.main_notebook.add(reports_frame, text="📋 Berichte")

        # Einstellungen Tab
        settings_frame = self.create_settings_tab()
        self.main_notebook.add(settings_frame, text="⚙️ Einstellungen")

    def create_dashboard_tab(self):
        """Professionelles Dashboard"""
        frame = ttk.Frame()

        # Willkommens-Bereich
        welcome_frame = ttk.Frame(frame, style='Card.TFrame', padding=20)
        welcome_frame.pack(fill=tk.X, pady=(0,20), padx=20)

        welcome_text = f"""Willkommen zurück, {self.current_user}!

Session gestartet: {self.session_start.strftime('%d.%m.%Y %H:%M')}
Aktive Projekte: 5
Ausstehende Aufgaben: 12
Gesamtertrag (dieses Jahr): €45,678.90"""

        welcome_label = tk.Label(welcome_frame, text=welcome_text,
                               font=('Arial', 11), justify=tk.LEFT, bg='#e8f4fd', padx=20, pady=20)
        welcome_label.pack(anchor=tk.W)

        # KPIs Grid
        kpi_frame = ttk.Frame(frame)
        kpi_frame.pack(fill=tk.X, padx=20, pady=(0,20))

        kpis = [
            ("Gesamtumsatz", "€45,678.90", "#4CAF50", "+12.5%"),
            ("Aktive Kunden", "23", "#2196F3", "+3"),
            ("Projekte pro Monat", "8", "#FF9800", "+15%"),
            ("Zeit bis Zahlung", "14 Tage", "#9C27B0", "-2 Tage")
        ]

        for i, (title, value, color, change) in enumerate(kpis):
            kpi_card = ttk.Frame(kpi_frame, borderwidth=1, relief=tk.RAISED, padding=15)
            kpi_card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')

            ttk.Label(kpi_card, text=title, font=('Arial', 10, 'bold')).pack(anchor=tk.W)
            value_label = tk.Label(kpi_card, text=value, font=('Arial', 24, 'bold'),
                                 fg=color)
            value_label.pack(anchor=tk.W, pady=(5,0))
            ttk.Label(kpi_card, text=change, foreground="#4CAF50").pack(anchor=tk.W)

        kpi_frame.grid_columnconfigure(0, weight=1)
        kpi_frame.grid_columnconfigure(1, weight=1)

        # Aktivitäts-Timeline
        timeline_frame = ttk.LabelFrame(frame, text="LETZTE AKTIVITÄTEN", padding=15)
        timeline_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        # Beispiel-Aktivitäten
        activities = [
            "14:32 - Neue Anfrage von TechCorp GmbH eingegangen",
            "14:15 - Zahlung über €2,345 von StartupXYZ erhalten",
            "13:45 - Projekt-Meeting mit MediaHub beendet",
            "11:20 - Code-Review für DataFlow Inc. abgeschlossen",
            "10:30 - Zwischenstand Präsentation für InnoTech gehalten"
        ]

        for activity in activities:
            activity_label = ttk.Label(timeline_frame, text=activity, font=('Arial', 9))
            activity_label.pack(anchor=tk.W, pady=3, padx=10)

        # Quick-Actions Bar
        actions_bar = ttk.Frame(frame, style='Toolbar.TFrame', relief=tk.RAISED, borderwidth=1)
        actions_bar.pack(fill=tk.X, padx=20)

        quick_actions = [
            ("🎯", "Neues Projekt starten", self.new_project),
            ("📞", "Kunden anrufen", self.call_client),
            ("📧", "E-Mail verfassen", self.compose_email),
            ("📊", "Bericht erstellen", self.generate_reports),
            ("💰", "Zahlung registrieren", self.record_payment)
        ]

        for icon, text, command in quick_actions:
            btn = ttk.Button(actions_bar, text=f"{icon} {text}",
                           style='Toolbutton.TButton', command=command)
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        return frame

    def create_projects_tab(self):
        """Projektmanagement-Tab"""
        frame = ttk.Frame()

        # Projekt-Toolbar
        toolbar = ttk.Frame(frame)
        toolbar.pack(fill=tk.X, pady=(0,10))

        ttk.Button(toolbar, text="➕ Neues Projekt",
                  command=self.new_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="📝 Aufgabe hinzufügen",
                  command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="📈 Projektstatus ändern",
                  command=self.change_project_status).pack(side=tk.LEFT, padx=5)

        # Projekt-Tabelle
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

        columns = ('name', 'type', 'client', 'status', 'budget', 'revenue', 'profit')
        self.projects_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.projects_tree.heading(col, text=col.title())
            if col in ['budget', 'revenue', 'profit']:
                self.projects_tree.column(col, width=100, anchor='e')
            elif col == 'type':
                self.projects_tree.column(col, width=150)
            else:
                self.projects_tree.column(col, width=120)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.projects_tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.projects_tree.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.projects_tree.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.projects_tree.configure(xscrollcommand=h_scrollbar.set)

        self.projects_tree.pack(fill=tk.BOTH, expand=True)

        # Projekt-Details Panel
        details_frame = ttk.LabelFrame(frame, text="PROJEKT-DETAILS", padding=10)
        details_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        self.project_details_text = scrolledtext.ScrolledText(details_frame, height=8, wrap=tk.WORD)
        self.project_details_text.pack(fill=tk.BOTH, expand=True)
        self.project_details_text.insert(tk.END, "Klicken Sie auf ein Projekt, um Details zu sehen...")

        self.load_projects()
        self.projects_tree.bind('<<TreeviewSelect>>', self.show_project_details)

        return frame

    def create_finance_tab(self):
        """Finanzmanagement-Tab"""
        frame = ttk.Frame()

        # Revenue Summary
        summary_frame = ttk.Frame(frame, relief=tk.RIDGE, borderwidth=2, padding=15)
        summary_frame.pack(fill=tk.X, pady=(0,20), padx=20)

        self.total_revenue_label = tk.Label(
            summary_frame,
            text="GESAMTUMSATZ:\n€45,678.90",
            font=('Arial', 24, 'bold'),
            fg='#2E8B57',
            bg='#F0FFF0'
        )
        self.total_revenue_label.pack(side=tk.LEFT, padx=20)

        # Monthly Chart (simplified)
        chart_frame = ttk.Frame(summary_frame)
        chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        values = [8200, 9500, 11300, 12800, 15478]

        max_val = max(values)
        for i, (month, value) in enumerate(zip(months, values)):
            ttk.Label(chart_frame, text=month, font=('Arial', 8)).grid(row=0, column=i, padx=10)
            bar_height = int((value / max_val) * 50)

            # Simple bar
            canvas = tk.Canvas(chart_frame, width=30, height=60, bg='white')
            canvas.create_rectangle(5, 60-bar_height, 25, 60, fill='#4CAF50')
            canvas.create_text(15, 70, text=f'€{value}', font=('Arial', 6))
            canvas.grid(row=1, column=i)

        # Finance Actions
        actions_frame = ttk.Frame(frame)
        actions_frame.pack(fill=tk.X, padx=20, pady=(0,20))

        finance_actions = [
            ("📊 Bilanz erstellen", self.create_balance_sheet),
            ("💳 Zahlung registrieren", self.record_payment),
            ("📈 Budget überwachen", self.monitor_budget),
            ("📋 Steuerberechnen", self.calculate_taxes),
            ("💰 Dividendenauszahlung", self.pay_dividends)
        ]

        for action, command in finance_actions:
            ttk.Button(actions_frame, text=action, command=command).pack(side=tk.LEFT, padx=10, pady=5)

        # Transaction History
        history_frame = ttk.LabelFrame(frame, text="LETZTE TRANSKTIONEN", padding=15)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        # Sample transactions
        transactions = [
            ("14.12.2025 14:32", "Eingang", "TechCorp GmbH", "+€2,345.67", "Projektzahlung"),
            ("14.12.2025 13:15", "Ausgang", "Serverkosten", "-€124.50", "AWS Hosting"),
            ("13.12.2025 16:45", "Eingang", "StartupXYZ", "+€750.00", "Beratungstunde"),
            ("13.12.2025 11:20", "Ausgang", "Bürobedarf", "-€89.30", "Druckerpapier"),
            ("12.12.2025 15:30", "Eingang", "MediaHub", "+€1,200.00", "Content Creation")
        ]

        for date, type_, client, amount, desc in transactions:
            row = ttk.Frame(history_frame)
            row.pack(fill=tk.X, pady=3)

            ttk.Label(row, text=date, width=15).pack(side=tk.LEFT)
            ttk.Label(row, text=type_, width=8).pack(side=tk.LEFT)
            ttk.Label(row, text=client, width=15).pack(side=tk.LEFT)
            amount_label = ttk.Label(row, text=amount, width=12,
                                   foreground='green' if '+€' in amount else 'red')
            amount_label.pack(side=tk.LEFT)
            ttk.Label(row, text=desc).pack(side=tk.LEFT)

        return frame

    def create_reports_tab(self):
        """Berichts-Tab"""
        frame = ttk.Frame()

        # Report Types
        report_types_frame = ttk.LabelFrame(frame, text="VERFÜGBARE BERICHTE", padding=15)
        report_types_frame.pack(fill=tk.X, padx=20, pady=(0,20))

        reports = [
            ("📈 Financial Summary", "Monatliche Finanzübersicht", self.generate_financial_report),
            ("💼 Project Status", "Aktuelle Projektstände", self.generate_project_report),
            ("👥 Client Analysis", "Kundenanalyse und Trends", self.generate_client_report),
            ("⏰ Time Tracking", "Zeitaufwand pro Projekt", self.generate_time_report),
            ("📊 Performance Metrics", "Leistungskennzahlen", self.generate_performance_report)
        ]

        for icon, title, func in reports:
            report_frame = ttk.Frame(report_types_frame)
            report_frame.pack(fill=tk.X, pady=5)

            ttk.Label(report_frame, text=f"{icon} {title}", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)

            generate_btn = ttk.Button(report_frame, text="Generieren",
                                    command=lambda f=func, t=title: self.generate_report(f, t))
            generate_btn.pack(side=tk.RIGHT)

        # Report Preview
        preview_frame = ttk.LabelFrame(frame, text="BERICHTSVORSCHAU", padding=15)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,20))

        self.report_preview = scrolledtext.ScrolledText(preview_frame, height=20, wrap=tk.WORD)
        self.report_preview.pack(fill=tk.BOTH, expand=True)

        # Export Options
        export_frame = ttk.Frame(frame)
        export_frame.pack(fill=tk.X, padx=20)

        export_options = [
            ("💾 Speichern", "report.pdf", self.export_pdf),
            ("📊 Excel", "data.xlsx", self.export_excel),
            ("📈 CSV", "data.csv", self.export_csv),
            ("🖨️ Drucken", "", self.print_report)
        ]

        for label, ext, func in export_options:
            ttk.Button(export_frame, text=f"{label} ({ext})" if ext else label,
                      command=lambda f=func: self.export_data(f)).pack(side=tk.LEFT, padx=5)

        return frame

    def create_settings_tab(self):
        """Einstellungen-Tab"""
        frame = ttk.Frame()

        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # General Settings
        general_frame = self.create_general_settings()
        notebook.add(general_frame, text="📋 Allgemein")

        # Finance Settings
        finance_settings = self.create_finance_settings()
        notebook.add(finance_settings, text="💰 Finanzen")

        # System Settings
        system_settings = self.create_system_settings()
        notebook.add(system_settings, text="⚙️ System")

        return frame

    def create_general_settings(self):
        """Allgemeine Einstellungen"""
        frame = ttk.Frame()

        # Company Settings
        company_frame = ttk.LabelFrame(frame, text="UNTREHMENSINFORMATIONEN", padding=15)
        company_frame.pack(fill=tk.X, pady=(0,20), padx=20)

        company_fields = [
            ("Firmenname:", "CASH MONEY AI GmbH"),
            ("Adresse:", "Musterstraße 123, 80331 München"),
            ("Telefon:", "+49-89-12345678"),
            ("E-Mail:", "info@cashmoney-ai.com"),
            ("Webseite:", "https://cashmoney-ai.com")
        ]

        self.company_entries = {}
        for label_text, default in company_fields:
            row = ttk.Frame(company_frame)
            row.pack(fill=tk.X, pady=5)
            ttk.Label(row, text=label_text, width=12).pack(side=tk.LEFT)
            entry = ttk.Entry(row)
            entry.insert(0, default)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10,0))
            self.company_entries[label_text] = entry

        # User Preferences
        pref_frame = ttk.LabelFrame(frame, text="BENUTZER-EINSTELLUNGEN", padding=15)
        pref_frame.pack(fill=tk.X, pady=(0,20), padx=20)

        ttk.Label(pref_frame, text="Sprache:").grid(row=0, column=0, sticky=tk.W, pady=5)
        language_var = tk.StringVar(value="Deutsch")
        ttk.Combobox(pref_frame, textvariable=language_var,
                    values=["Deutsch", "English", "Français"]).grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(pref_frame, text="Thème:").grid(row=1, column=0, sticky=tk.W, pady=5)
        theme_var = tk.StringVar(value="Light")
        ttk.Combobox(pref_frame, textvariable=theme_var,
                    values=["Light", "Dark", "Blue", "Green"]).grid(row=1, column=1, sticky=tk.EW, pady=5)

        pref_frame.grid_columnconfigure(1, weight=1)

        # Save Button
        ttk.Button(frame, text="💾 EINSTELLUNGEN SPEICHERN",
                  command=self.save_settings).pack(pady=20)

        return frame

    def create_finance_settings(self):
        """Finanzeinstellungen"""
        frame = ttk.Frame()

        # Currency Settings
        currency_frame = ttk.LabelFrame(frame, text="WÄHRUNGSEINSTELLUNGEN", padding=15)
        currency_frame.pack(fill=tk.X, pady=(0,20), padx=20)

        ttk.Label(currency_frame, text="Hauptwährung:").grid(row=0, column=0, sticky=tk.W, pady=5)
        currency_var = tk.StringVar(value="EUR")
        ttk.Combobox(currency_frame, textvariable=currency_var,
                    values=["EUR", "USD", "CHF", "GBP"]).grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(currency_frame, text="Steuersatz (%):").grid(row=1, column=0, sticky=tk.W, pady=5)
        tax_entry = ttk.Entry(currency_frame)
        tax_entry.insert(0, "19.0")
        tax_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        currency_frame.grid_columnconfigure(1, weight=1)

        # Invoice Settings
        invoice_frame = ttk.LabelFrame(frame, text="RECHNUNGS-EINSTELLUNGEN", padding=15)
        invoice_frame.pack(fill=tk.X, pady=(0,20), padx=20)

        ttk.Label(invoice_frame, text="Rechnungsvorlage:").grid(row=0, column=0, sticky=tk.W, pady=5)
        template_var = tk.StringVar(value="Standard")
        ttk.Combobox(invoice_frame, textvariable=template_var,
                    values=["Standard", "Professional", "Minimal"]).grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Label(invoice_frame, text="Automatische Nummerierung:").grid(row=1, column=0, sticky=tk.W, pady=5)
        auto_num_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(invoice_frame, variable=auto_num_var).grid(row=1, column=1, sticky=tk.W, pady=5)

        invoice_frame.grid_columnconfigure(1, weight=1)

        return frame

    def create_system_settings(self):
        """Systemeinstellungen"""
        frame = ttk.Frame()

        # Backup Settings
        backup_frame = ttk.LabelFrame(frame, text="BACKUP-KONFIGURATION", padding=15)
        backup_frame.pack(fill=tk.X, pady=(0,20), padx=20)

        ttk.Label(backup_frame, text="Automatisches Backup:").grid(row=0, column=0, sticky=tk.W, pady=5)
        backup_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(backup_frame, variable=backup_enabled).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(backup_frame, text="Backup-Intervall (Tage):").grid(row=1, column=0, sticky=tk.W, pady=5)
        backup_interval = ttk.Spinbox(backup_frame, from_=1, to=30, width=10)
        backup_interval.set(7)
        backup_interval.grid(row=1, column=1, sticky=tk.W, pady=5)

        backup_frame.grid_columnconfigure(1, weight=1)

        # Performance Settings
        perf_frame = ttk.LabelFrame(frame, text="LEISTUNGSEINSTELLUNGEN", padding=15)
        perf_frame.pack(fill=tk.X, pady=(0,20), padx=20)

        ttk.Label(perf_frame, text="UI Animations:").grid(row=0, column=0, sticky=tk.W, pady=5)
        animations_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(perf_frame, variable=animations_var).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(perf_frame, text="Auto-Speichern alle (Minuten):").grid(row=1, column=0, sticky=tk.W, pady=5)
        autosave_interval = ttk.Spinbox(perf_frame, from_=2, to=60, width=10)
        autosave_interval.set(5)
        autosave_interval.grid(row=1, column=1, sticky=tk.W, pady=5)

        perf_frame.grid_columnconfigure(1, weight=1)

        # System Info
        info_frame = ttk.LabelFrame(frame, text="SYSTEM INFORMATIONEN", padding=15)
        info_frame.pack(fill=tk.X, pady=(0,20), padx=20)

        import platform
        import psutil

        system_info = f"""
Betriebssystem: {platform.system()} {platform.release()}
Prozessor: {platform.processor()}
Arbeitsspeicher: {psutil.virtual_memory().total // (1024**3)} GB
Python-Version: {platform.python_version()}
Datenbank: SQLite {sqlite3.sqlite_version}
Applikation Version: 2.3 Professional
Letzte Aktualisierung: {datetime.now().strftime('%d.%m.%Y')}
"""

        info_label = tk.Label(info_frame, text=system_info, font=('Courier', 9),
                            justify=tk.LEFT, bg='#f8f9fa')
        info_label.pack(fill=tk.X, pady=10)

        return frame

    # Business Logic Methods

    def load_projects(self):
        """Load projects from database"""
        try:
            cursor = self.conn.execute("""
                SELECT name, type, client_name, status, budget, revenue,
                       (revenue - budget) as profit
                FROM projects
                ORDER BY created_at DESC
            """)
            rows = cursor.fetchall()

            # Clear existing items
            for item in self.projects_tree.get_children():
                self.projects_tree.delete(item)

            for row in rows:
                name, type_, client, status, budget, revenue, profit = row
                profit_color = 'green' if profit and profit > 0 else 'red' if profit and profit < 0 else 'black'

                self.projects_tree.insert('', 'end', values=(
                    name, type_, client, status,
                    f"€{budget or 0:.2f}" if budget else "€0.00",
                    f"€{revenue or 0:.2f}" if revenue else "€0.00",
                    f"€{profit or 0:.2f}" if profit else "€0.00"
                ), tags=('profit',))
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load projects: {e}")

    def show_project_details(self, event):
        """Show details for selected project"""
        selection = self.projects_tree.selection()
        if not selection:
            return

        item = selection[0]
        values = self.projects_tree.item(item, 'values')

        if not values:
            return

        project_name = values[0]

        # Get detailed project info
        cursor = self.conn.execute("""
            SELECT p.*, COUNT(t.id) as task_count
            FROM projects p
            LEFT JOIN tasks t ON p.id = t.project_id
            WHERE p.name = ?
            GROUP BY p.id
        """, (project_name,))

        row = cursor.fetchone()
        if row:
            details = f"""
PROJEKT-DETAILS: {row[1]}

Typ: {row[2]}
Kunde: {row[3]}
Status: {row[4]}
Budget: €{row[5] or 0:.2f}
Umsatz: €{row[6] or 0:.2f}
Profit: €{(row[6] or 0) - (row[5] or 0):.2f}

Aufgaben: {row[12]} (Gesamt)

Startdatum: {row[8]}
Notizen: {row[7] or 'Keine'}
"""

            self.project_details_text.delete(1.0, tk.END)
            self.project_details_text.insert(tk.END, details)

    def auto_backup(self):
        """Automatic backup system"""
        while True:
            try:
                time.sleep(3600)  # Backup every hour
                # Would implement real backup here
            except:
                pass

    def update_metrics(self):
        """Update system metrics periodically"""
        while True:
            try:
                # Update revenue
                cursor = self.conn.execute("SELECT SUM(revenue) FROM projects")
                total_revenue = cursor.fetchone()[0] or 0
                self.revenue_data['total'] = total_revenue

                # Update project count
                cursor = self.conn.execute("SELECT COUNT(*) FROM projects WHERE status = 'Aktiv'")
                active_projects = cursor.fetchone()[0]

                # Update sidebar stats
                if hasattr(self, 'sidebar_stats'):
                    self.sidebar_stats["Aktive Projekte:"].config(text=str(active_projects))
                    self.sidebar_stats["Heute Umsatz:"].config(text=f"€{total_revenue:.2f}")

                time.sleep(30)  # Update every 30 seconds
            except:
                pass

    def load_config(self):
        """Load application config"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.app_config = json.load(f)
            else:
                self.app_config = {
                    "theme": "light",
                    "language": "de",
                    "auto_backup": True,
                    "backup_interval": 7
                }
        except Exception as e:
            print(f"Config load error: {e}")

    def save_settings(self):
        """Save application settings"""
        try:
            config = {
                "theme": "light",
                "language": "de",
                "auto_backup": True,
                "backup_interval": 7,
                "company_name": self.company_entries.get("Firmenname:", {}).get() or "CASH MONEY AI GmbH"
            }

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)

            messagebox.showinfo("Erfolg", "Einstellungen wurden gespeichert!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")

    # UI Event Handlers

    def new_project(self):
        """Create new project"""
        new_project_win = tk.Toplevel(self.root)
        new_project_win.title("Neues Projekt erstellen")
        new_project_win.geometry("500x600")
        new_project_win.resizable(False, False)

        ttk.Label(new_project_win, text="Projekt-Details", font=('Arial', 14, 'bold')).pack(pady=20)

        # Form fields
        form_frame = ttk.Frame(new_project_win)
        form_frame.pack(fill=tk.X, padx=20, pady=(0,20))

        fields = [
            ("Projektname:", "entry", ""),
            ("Projekttyp:", "combo", ["KI Consultierung", "Marketing Automation", "Content Erstellung"]),
            ("Kunde:", "entry", ""),
            ("Budget (€):", "entry", "0.00"),
            ("Startdatum:", "entry", datetime.now().strftime("%Y-%m-%d"))
        ]

        entries = {}
        for i, (label, field_type, default) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            if field_type == "entry":
                entry = ttk.Entry(form_frame)
                entry.insert(0, default)
                entry.grid(row=i, column=1, sticky=tk.EW, padx=(10,0), pady=5)
            elif field_type == "combo":
                entry = ttk.Combobox(form_frame, values=default)
                entry.set(default[0] if default else "")
                entry.grid(row=i, column=1, sticky=tk.EW, padx=(10,0), pady=5)
            entries[label] = entry

        form_frame.grid_columnconfigure(1, weight=1)

        # Notes field
        ttk.Label(new_project_win, text="Beschreibung:").pack(anchor=tk.W, padx=20, pady=(10,5))
        notes_text = scrolledtext.ScrolledText(new_project_win, height=5)
        notes_text.pack(fill=tk.X, padx=20, pady=(0,20))
