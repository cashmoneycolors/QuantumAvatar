#!/usr/bin/env python3
"""
JOULE PERFORMANCE PC MANAGER
Professionelle Desktop-Applikation für Gaming PC Produktverwaltung
RTX 5060 Blackwell Edition - DLSS 4 Quantum Optimiert

FEATURES:
- Vollständige Produkt-Spezifikationen RTX 5060
- DLSS 4 Transformer Technology Erklärung
- FPS Performance Calculator
- JSON Export Funktionalität
- Professional Dark Gaming Theme
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import json
from datetime import datetime
import os
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

class JoulePerformancePCManager:
    """Professionelle Gaming PC Produkt-Manager Applikation"""

    def __init__(self, root):
        self.root = root
        self.root.title("JOULE PERFORMANCE PC MANAGER - RTX 5060 Blackwell Edition v7.0")
        self.root.geometry("1500x1000")
        self.root.configure(bg='#0a0a1a')
        self.root.minsize(1200, 800)

        # RTX 5060 Blackwell Produktdaten (Live 2025 Daten)
        self.product_data = {
            "model": "Joule Performance RTX 5060 Gaming PC",
            "product_id": "JP-RTX5060-BLACKWELL-2025",
            "gpu": {
                "name": "NVIDIA GeForce RTX 5060",
                "architecture": "Blackwell",
                "cuda_cores": 3584,
                "rt_cores": 56,
                "tensor_cores": 112,
                "vram": "12 GB GDDR7",
                "memory_bus": "192-bit",
                "base_clock": "2040 MHz",
                "boost_clock": "2535 MHz",
                "power_tdp": "220W",
                "launch_date": "Mai 2025"
            },
            "cpu": "Intel Core i9-14900KF (24 Kerne, 32 Threads, 6.0 GHz Boost)",
            "ram": "64 GB DDR5-6000 MHz (2x 32 GB)",
            "storage": "2 TB PCIe 5.0 NVMe SSD",
            "motherboard": "Z790 Gaming Mainboard",
            "psu": "1000W 80PLUS Platinum",
            "cooling": "360mm AIO Wasserkühlung + RGB Lüfter",
            "case": "Premium Gaming Tower schwarz mit RGB",
            "os": "Windows 11 Pro vorinstalliert",
            "connectivity": "WiFi 6E + Bluetooth 5.4 + 5G LAN",
            "dlss": "DLSS 4 mit Multi Frame Generation (Bis 8x FPS Boost)",
            "price_eur": 2499.99,
            "original_price": 3199.00,
            "discount_percent": 22,
            "warranty": "36 Monate Premium Garantie",
            "availability": "Sofort lieferbar (RTX 50 Serie Stock)",
            "performance": {
                "1080p_ultra_dlss": "400+ FPS",
                "1440p_ultra_dlss": "250+ FPS",
                "4k_high_dlss4": "144+ FPS",
                "4k_path_tracing_mfg": "240+ FPS",
                "benchmark_score": "105/100 (Gaming Performance Index 2025)"
            },
            "dlss_4_features": [
                "Multi Frame Generation (bis zu 3 extra Frames)",
                "Transformer-basierte KI-Modelle (Vision Transformer)",
                "Globale Self-Attention für schärfere Details",
                "Retro-kompatibel alle RTX 20+ GPUs",
                "Bis zu 8x FPS-Steigerung bei 4K Path Tracing",
                "Frame Warp (NVIDIA Reflex 2) Integration",
                "AI-basiertes Ray Tracing Denoising",
                "Cloud-basierte KI-Model Updates"
            ],
            "compatibility": [
                "Windows 11/10 (64-bit erforderlich)",
                "DirectX 12 Ultimate mit Mesh Shading",
                "OpenGL 4.6 + Vulkan 1.3",
                "PCIe 5.0 Unterstützung",
                "USB 3.2 Gen2 (10 Gbps)",
                "HDR10 & Dolby Vision ready",
                "VR Ready (Quest 2/3 + PCVR)"
            ]
        }

        # Professional Gaming Theme Farben
        self.colors = {
            'bg_dark': '#0a0a1a',      # Dunkelblau-schwarz (Gaming Standard)
            'bg_card': '#1a1a2e',     # Leicht blauer Card-Hintergrund
            'bg_highlight': '#1f1f3f', # Hervorgehobene Bereiche
            'primary': '#00d4ff',     # Elektrisches Blau (RTX Branding)
            'secondary': '#ff6b9d',   # Neon Pink
            'accent': '#7bff8d',      # Elektrisches Grün (Success)
            'warning': '#ffa500',     # Orange (Warnung)
            'danger': '#ff4757',      # Rot (Fehler)
            'success': '#32cd32',     # Hellgrün
            'rtx_green': '#76b900',   # NVIDIA RTX Grün
            'text': '#ffffff',
            'text_light': '#b0b0cc',
            'text_dark': '#8080aa',
            'border': '#404060'
        }

        # GUI Initialisierung
        self.root.tk_setPalette(
            background=self.colors['bg_dark'],
            foreground=self.colors['text']
        )

        # Haupt-Tab-System erstellen
        self.create_main_interface()

        # App-Icon setzen (falls verfügbar)
        try:
            self.root.iconbitmap("icon.ico")  # Optional
        except:
            pass

        print("🎮 JOULE PERFORMANCE PC MANAGER RTX 5060 INITIALIZED")
        print("📊 DLSS 4 Quantum Technology Ready")
        print("🚀 Blackwell Architecture Optimized")

    def create_main_interface(self):
        """Erstellt das professionelle Haupt-Interface mit Tabs"""

        # Haupt-Tab-Control
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Style für Tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 12, 'bold'))
        style.configure('TFrame', background=self.colors['bg_dark'])

        # Tab 1: Produkt Overview
        tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab1, text="🖥️ PRODUKT OVERVIEW")
        self.build_product_overview_tab(tab1)

        # Tab 2: RTX 5060 Specs
        tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab2, text="🎮 RTX 5060 SPECS")
        self.build_gpu_specs_tab(tab2)

        # Tab 3: DLSS 4 Technology
        tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab3, text="⚡ DLSS 4 QUANTUM")
        self.build_dlss_technology_tab(tab3)

        # Tab 4: Performance Calculator
        tab4 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab4, text="📊 FPS CALCULATOR")
        self.build_performance_calculator_tab(tab4)

        # Tab 5: Compatibility & Support
        tab5 = ttk.Frame(self.tab_control)
        self.tab_control.add(tab5, text="🔧 SUPPORT & COMPATIBILITY")
        self.build_support_tab(tab5)

        # Action Bar am unteren Rand
        self.create_action_bar()

    def build_product_overview_tab(self, tab):
        """Baut den Produkt-Overview Tab"""

        # Scrollbar für langen Content
        main_frame = tk.Frame(tab, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_dark'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Haupt-Header
        header_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_dark'], pady=30)
        header_frame.pack(fill=tk.X)

        # RTX Branding
        rtx_label = tk.Label(header_frame, text="NVIDIA GEFORCE RTX", font=("Arial", 14),
                           fg=self.colors['rtx_green'], bg=self.colors['bg_dark'])
        rtx_label.pack()

        # Haupt-Titel
        title_label = tk.Label(header_frame, text="JOULE PERFORMANCE GAMING PC",
                             font=("Arial", 36, "bold"), fg=self.colors['primary'], bg=self.colors['bg_dark'])
        title_label.pack(pady=(10, 0))

        # Subtitle
        subtitle_label = tk.Label(header_frame, text="RTX 5060 Blackwell Edition - DLSS 4 Quantum Technology",
                                font=("Arial", 16), fg=self.colors['text_light'], bg=self.colors['bg_dark'])
        subtitle_label.pack(pady=(10, 20))

        # Produkt-Karte
        product_card = tk.Frame(scrollable_frame, bg=self.colors['bg_card'],
                              relief=tk.RIDGE, bd=2, padx=30, pady=25)
        product_card.pack(fill=tk.X, pady=20)

        # GPU Highlight Box
        gpu_highlight = tk.Frame(product_card, bg=self.colors['bg_highlight'],
                               relief=tk.RAISED, bd=2, padx=20, pady=15)
        gpu_highlight.pack(fill=tk.X, pady=(0, 20))

        gpu_title = tk.Label(gpu_highlight, text="🚀 FLAGHSHIP RTX 5060 BLACKWELL GPU",
                           font=("Arial", 16, "bold"), fg=self.colors['rtx_green'], bg=self.colors['bg_highlight'])
        gpu_title.pack()

        gpu_desc = tk.Label(gpu_highlight,
                           text="""3,584 CUDA Cores • 56 RT Cores • 112 Tensor Cores • 12 GB GDDR7
Blackwell Architecture • DLSS 4 Ready • 220W TDP • Future-Proof Gaming""",
                           font=("Arial", 11), fg=self.colors['text'], bg=self.colors['bg_highlight'],
                           justify=tk.LEFT)
        gpu_desc.pack(pady=(10, 0))

        # Preis-Sektion
        price_section = tk.Frame(product_card, bg=self.colors['bg_card'])
        price_section.pack(fill=tk.X, pady=20)

        # Rabatt Badge
        discount_badge = tk.Frame(price_section, bg=self.colors['danger'], padx=15, pady=8)
        discount_badge.pack(anchor='w', pady=(0, 15))

        discount_text = tk.Label(discount_badge, text=f"🔥 {self.product_data['discount_percent']}% EXKLUSIV-RABATT 🔥",
                               font=("Arial", 14, "bold"), fg="#ffffff", bg=self.colors['danger'])
        discount_text.pack()

        # Preis-Grid
        price_grid = tk.Frame(price_section, bg=self.colors['bg_card'])
        price_grid.pack(fill=tk.X)

        # Alter Preis
        old_price_label = tk.Label(price_grid, text="ORIGINALPREIS:",
                                 font=("Arial", 12), fg=self.colors['text_light'], bg=self.colors['bg_card'])
        old_price_label.pack(anchor='w')

        old_price_value = tk.Label(price_grid, text=f"{self.product_data['original_price']:,.2f} €".replace(",", "."),
                                 font=("Arial", 18, "overstrike"), fg=self.colors['text_light'], bg=self.colors['bg_card'])
        old_price_value.pack(anchor='w', pady=(5, 15))

        # Sparbetrag
        savings_label = tk.Label(price_grid, text=f"SIE SPAREN: {self.product_data['original_price'] - self.product_data['price_eur']:,.2f} €".replace(",", "."),
                               font=("Arial", 14, "bold"), fg=self.colors['accent'], bg=self.colors['bg_card'])
        savings_label.pack(anchor='w', pady=(0, 20))

        # Aktueller Preis (Prominent)
        current_price_label = tk.Label(price_grid, text="JETZT NUR:",
                                     font=("Arial", 20, "bold"), fg=self.colors['text'], bg=self.colors['bg_card'])
        current_price_label.pack(side=tk.LEFT)

        current_price_value = tk.Label(price_grid, text=".2f",
                                     font=("Arial", 48, "bold"), fg=self.colors['success'], bg=self.colors['bg_card'])
        current_price_value.pack(side=tk.LEFT, padx=(20, 0))

        # EUR Label
        price_eur_label = tk.Label(price_grid, text="EUR",
                                 font=("Arial", 20, "bold"), fg=self.colors['success'], bg=self.colors['bg_card'])
        price_eur_label.pack(side=tk.LEFT, padx=(10, 0))

        # Verfügbarkeit & Garantie
        availability_frame = tk.Frame(price_section, bg=self.colors['success'], padx=15, pady=12)
        availability_frame.pack(fill=tk.X, pady=(20, 0))

        availability_text = tk.Label(availability_frame,
                                   text=f"🟢 {self.product_data['availability']} | 🛡️ {self.product_data['warranty']}",
                                   font=("Arial", 12, "bold"), fg='white', bg=self.colors['success'])
        availability_text.pack()

        # Quick Specs Overview
        specs_overview = tk.LabelFrame(scrollable_frame, text="⚡ SCHNELLÜBERSICHT HAUPTKOMPONENTEN",
                                     font=("Arial", 16, "bold"), fg=self.colors['secondary'],
                                     bg=self.colors['bg_dark'], relief=tk.GROOVE, bd=2)
        specs_overview.pack(fill=tk.X, pady=20)

        specs_content = tk.Frame(specs_overview, bg=self.colors['bg_card'], padx=20, pady=20)
        specs_content.pack(fill=tk.X)

        # Schnell-Specs als Grid
        specs = [
            ("Grafikkarte", "RTX 5060 12GB GDDR7 Blackwell"),
            ("Prozessor", "Intel i9-14900KF (24 Kerne)"),
            ("Arbeitsspeicher", "64 GB DDR5-6000"),
            ("Speicher", "2 TB PCIe 5.0 NVMe SSD"),
            ("Netzteil", "1000W 80+ Platinum Modular"),
            ("Kühlung", "360mm AIO Wasserkühlung"),
            ("Gehäuse", "Premium Gaming Tower RGB"),
            ("Betriebssystem", "Windows 11 Pro vorinstalliert")
        ]

        for i, (component, spec) in enumerate(specs):
            spec_row = tk.Frame(specs_content, bg=self.colors['bg_card'], pady=5)
            spec_row.pack(fill=tk.X)

            component_label = tk.Label(spec_row, text=f"{component}:",
                                    font=("Arial", 11, "bold"), fg=self.colors['primary'],
                                    bg=self.colors['bg_card'], width=18, anchor="w")
            component_label.pack(side=tk.LEFT)

            spec_label = tk.Label(spec_row, text=spec,
                                font=("Arial", 11), fg=self.colors['text'],
                                bg=self.colors['bg_card'], anchor="w")
            spec_label.pack(side=tk.LEFT)

    def build_gpu_specs_tab(self, tab):
        """RTX 5060 detaillierte Spezifikationen"""

        tab.configure(bg=self.colors['bg_dark'])

        # Header
        header_label = tk.Label(tab, text="🎮 NVIDIA GEFORCE RTX 5060 BLACKWELL",
                              font=("Arial", 24, "bold"), fg=self.colors['rtx_green'],
                              bg=self.colors['bg_dark'])
        header_label.pack(pady=20)

        subtitle_label = tk.Label(tab, text="Flagship Gaming GPU - Quantum-Level Performance",
                                font=("Arial", 16), fg=self.colors['text_light'],
                                bg=self.colors['bg_dark'])
        subtitle_label.pack(pady=(0, 30))

        # GPU Spezifikationen
        specs_frame = tk.LabelFrame(tab, text="TECHNISCHE DATEN RTX 5060",
                                  font=("Arial", 16, "bold"), fg=self.colors['primary'],
                                  bg=self.colors['bg_dark'], relief=tk.GROOVE, bd=2)
        specs_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))

        # Scrollbares Specs-Fenster
        specs_canvas = tk.Canvas(specs_frame, bg=self.colors['bg_card'], highlightthickness=0)
        specs_scrollbar = ttk.Scrollbar(specs_frame, orient="vertical", command=specs_canvas.yview)
        specs_scrollable = tk.Frame(specs_canvas, bg=self.colors['bg_card'])

        specs_scrollable.bind("<Configure>", lambda e: specs_canvas.configure(scrollregion=specs_canvas.bbox("all")))
        specs_canvas.create_window((0, 0), window=specs_scrollable, anchor="nw")
        specs_canvas.configure(yscrollcommand=specs_scrollbar.set)

        specs_canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        specs_scrollbar.pack(side="right", fill="y")

        specs_canvas.bind_all("<MouseWheel>", lambda e: specs_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        inner_frame = tk.Frame(specs_scrollable, bg=self.colors['bg_card'], padx=20, pady=20)
        inner_frame.pack(fill=tk.BOTH, expand=True)

        # GPU Core Specs
        gpu_specs = [
            ("CUDA Cores", "3,584", "Parallel Processing Einheiten"),
            ("RT Cores (Ray Tracing)", "56 Gen 3", "Hardware Ray Tracing Beschleunigung"),
            ("Tensor Cores", "112 Gen 4", "AI & DLSS Processing"),
            ("VRAM Kapazität", "12 GB", "GDDR7 High-Speed Memory"),
            ("Memory Bus Width", "192-bit", "Memory Interface"),
            ("Memory Bandwidth", "720 GB/s", "VRAM Transfer Rate"),
            ("Base Clock Speed", "2,040 MHz", "Standard Taktrate"),
            ("Boost Clock Speed", "2,535 MHz", "Maximale Boost-Rate"),
            ("TDP (Thermal Design)", "220W", "Maximale Leistungsaufnahme"),
            ("Architecture", "Blackwell", "NVIDIA Next-Gen Architektur"),
            ("Transistor Count", "57.7 Milliarden", "Chip Komplexität"),
            ("Die Size", "314 mm²", "Chip-Fläche"),
            ("Manufacturing Node", "4N TSMC", "Herstellungsprozess")
        ]

        # Specs in Spalten anzeigen
        left_col = tk.Frame(inner_frame, bg=self.colors['bg_card'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        right_col = tk.Frame(inner_frame, bg=self.colors['bg_card'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Specs aufteilen
        mid_point = len(gpu_specs) // 2
        specs_left = gpu_specs[:mid_point]
        specs_right = gpu_specs[mid_point:]

        # Linke Spalte füllen
        self.create_specs_column(left_col, specs_left)

        # Rechte Spalte füllen
        self.create_specs_column(right_col, specs_right)

        # Performance Benchmark Section
        perf_frame = tk.LabelFrame(tab, text="BENCHMARK PERFORMANCE RTX 5060",
                                 font=("Arial", 16, "bold"), fg=self.colors['accent'],
                                 bg=self.colors['bg_dark'], relief=tk.GROOVE, bd=2)
        perf_frame.pack(fill=tk.X, padx=30, pady=20)

        perf_inner = tk.Frame(perf_frame, bg=self.colors['bg_card'], padx=20, pady=20)
        perf_inner.pack(fill=tk.X)

        # Performance Daten
        performance_data = [
            ("3DMark Time Spy Graphics Score", "~24,000 Punkte", "Gaming Performance Index"),
            ("Cinebench R23 Multi-Core", "~45,000 Punkte", "CPU Intensität Workloads"),
            ("Crystal Disk Mark Seq. Read", "~12,000 MB/s", "SSD Performance"),
            ("Unigine Superposition 1080p", "High: 240 FPS+", "Stresstest Performance"),
            ("FurMark 1080p Stress Test", "75°C GPU Temp Max", "Stability & Thermal")
        ]

        for title, value, desc in performance_data:
            perf_row = tk.Frame(perf_inner, bg=self.colors['bg_card'], pady=8)
            perf_row.pack(fill=tk.X)

            title_label = tk.Label(perf_row, text=title + ":",
                                 font=("Arial", 11, "bold"), fg=self.colors['text_light'],
                                 bg=self.colors['bg_card'], width=30, anchor="w")
            title_label.pack(side=tk.LEFT)

            value_label = tk.Label(perf_row, text=value,
                                 font=("Arial", 12, "bold"), fg=self.colors['accent'],
                                 bg=self.colors['bg_card'], width=15, anchor="w")
            value_label.pack(side=tk.LEFT, padx=(10, 0))

            desc_label = tk.Label(perf_row, text=desc,
                                font=("Arial", 10), fg=self.colors['text_light'],
                                bg=self.colors['bg_card'], anchor="w")
            desc_label.pack(side=tk.LEFT, padx=(15, 0))

    def create_specs_column(self, parent, specs_list):
        """Hilfsfunktion für Specs-Spalten"""
        for spec_name, spec_value, spec_desc in specs_list:
            spec_row = tk.Frame(parent, bg=self.colors['bg_card'], pady=8)
            spec_row.pack(fill=tk.X)

            # Spec Name
            name_label = tk.Label(spec_row, text=f"{spec_name}:",
                               font=("Arial", 11, "bold"), fg=self.colors['primary'],
                               bg=self.colors['bg_card'], width=20, anchor="w")
            name_label.pack(side=tk.LEFT)

            # Spec Value
            value_label = tk.Label(spec_row, text=spec_value,
                                 font=("Arial", 13, "bold"), fg=self.colors['success'],
                                 bg=self.colors['bg_card'], width=12, anchor="w")
            value_label.pack(side=tk.LEFT, padx=(10, 0))

            # Description
            desc_label = tk.Label(spec_row, text=spec_desc,
                               font=("Arial", 9), fg=self.colors['text_light'],
                               bg=self.colors['bg_card'], anchor="w")
            desc_label.pack(side=tk.LEFT, padx=(15, 0))

    def build_dlss_technology_tab(self, tab):
        """DLSS 4 Quantum Technology Erklärung"""

        tab.configure(bg=self.colors['bg_dark'])

        # Haupt-Header
        header_frame = tk.Frame(tab, bg=self.colors['bg_dark'])
        header_frame.pack(fill=tk.X, pady=30)

        dlss_icon = tk.Label(header_frame, text="⚡", font=("Arial", 48),
                           fg=self.colors['primary'], bg=self.colors['bg_dark'])
        dlss_icon.pack()

        dlss_title = tk.Label(header_frame, text="DLSS 4 QUANTUM TECHNOLOGY",
                            font=("Arial", 28, "bold"), fg=self.colors['primary'],
                            bg=self.colors['bg_dark'])
        dlss_title.pack(pady=(10, 0))

        dlss_subtitle = tk.Label(header_frame, text="Deep Learning Super Sampling - Transformer AI für Gaming",
                               font=("Arial", 16), fg=self.colors['text_light'], bg=self.colors['bg_dark'])
        dlss_subtitle.pack(pady=(10, 30))

        # DLSS Overview Card
        overview_card = tk.Frame(tab, bg=self.colors['bg_card'], relief=tk.RIDGE, bd=2, padx=30, pady=25)
        overview_card.pack(fill=tk.X, padx=30, pady=20)

        overview_title = tk.Label(overview_card, text="WAS IST DLSS 4?",
                                font=("Arial", 18, "bold"), fg=self.colors['secondary'],
                                bg=self.colors['bg_card'])
        overview_title.pack(anchor='w', pady=(0, 15))

        overview_text = """
DLSS 4 ist NVIDIA's revolutionäre KI-Technologie, die Framerates drastisch erhöht und Bildqualität verbessert.
Im Gegensatz zu traditionellen Upscaling-Methoden verwendet DLSS 4 fortschrittliche Vision Transformer-Modelle
(statte Convolutional Neural Networks), die globale Szenen-Kontexte verstehen und realistischere Ergebnisse liefern.

WICHTIG: DLSS 4 ist RTX 50-Serie EXKLUSIV mit bis zu 8x FPS-Boost bei 4K Path Tracing!"""

        overview_label = tk.Label(overview_card, text=overview_text.strip(),
                                font=("Arial", 12), fg=self.colors['text'], bg=self.colors['bg_card'],
                                justify=tk.LEFT, wraplength=1000)
        overview_label.pack(anchor='w')

        # Transformer Technology Section
        transformer_frame = tk.LabelFrame(tab, text="TRANSFORMER MODELLE: DIE REVOLUTION",
                                        font=("Arial", 16, "bold"), fg=self.colors['accent'],
                                        bg=self.colors['bg_dark'], relief=tk.GROOVE, bd=2)
        transformer_frame.pack(fill=tk.X, padx=30, pady=20)

        transformer_inner = tk.Frame(transformer_frame, bg=self.colors['bg_card'], padx=20, pady=20)
        transformer_inner.pack(fill=tk.X)

        # Vergleich CNN vs Transformer
        comparison_frame = tk.Frame(transformer_inner, bg=self.colors['bg_highlight'], padx=15, pady=15)
        comparison_frame.pack(fill=tk.X, pady=(0, 20))

        comp_title = tk.Label(comparison_frame, text="ARCHITEKTUR-VERGLEICH: CNN vs TRANSFORMER",
                            font=("Arial", 14, "bold"), fg=self.colors['warning'], bg=self.colors['bg_highlight'])
        comp_title.pack(anchor='w', pady=(0, 10))

        # CNN Column
        cnn_frame = tk.Frame(comparison_frame, bg=self.colors['bg_highlight'])
        cnn_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=(0, 20))

        cnn_title = tk.Label(cnn_frame, text="CNN (DLSS 1-3)",
                           font=("Arial", 12, "bold"), fg=self.colors['danger'], bg=self.colors['bg_highlight'])
        cnn_title.pack(anchor='w')

        cnn_points = [
            "Lokale Pixel-Verarbeitung (Kernel-Filter)",
            "Begrenzte Scene-Kontext Erkennung",
            "Häufig Ghosting bei schnellen Bewegungen",
            "Geringere Detail-Schärfe bei Upscaling",
            "Höherer Energieverbrauch pro Frame"
        ]

        for point in cnn_points:
            tk.Label(cnn_frame, text=f"• {point}", font=("Arial", 10),
                   fg=self.colors['text_light'], bg=self.colors['bg_highlight'], anchor="w").pack(fill=tk.X, pady=1)

        # VS Label
        vs_label = tk.Label(comparison_frame, text="VS", font=("Arial", 12, "bold"),
                          fg=self.colors['primary'], bg=self.colors['bg_highlight'])
        vs_label.pack(side=tk.LEFT, padx=20)

        # Transformer Column
        transformer_col = tk.Frame(comparison_frame, bg=self.colors['bg_highlight'])
        transformer_col.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        transformer_title = tk.Label(transformer_col, text="TRANSFORMER (DLSS 4)",
                                   font=("Arial", 12, "bold"), fg=self.colors['success'], bg=self.colors['bg_highlight'])
        transformer_title.pack(anchor='w')

        transformer_points = [
            "Globale Self-Attention (gesamte Scene)",
            "Kontextuelle Pixel-Beziehungen verstehen",
            "Reduziertes Ghosting durch Motion-Tracking",
            "Hochaufgelöste Details mit KI-Interpolation",
            "Effizientere Verarbeitung durch AI-Optimierung"
        ]

        for point in transformer_points:
            tk.Label(transformer_col, text=f"✓ {point}", font=("Arial", 10),
                   fg=self.colors['text'], bg=self.colors['bg_highlight'], anchor="w").pack(fill=tk.X, pady=1)

        # How It Works Section
        how_frame = tk.LabelFrame(transformer_inner, text="WIE FUNKTIONIERT DLSS 4?",
                                font=("Arial", 14, "bold"), fg=self.colors['accent'], bg=self.colors['bg_card'])
        how_frame.pack(fill=tk.X, pady=(20, 0))

        how_desc = """
1. LOW-RES FRAME INPUT: Spiel rendert Bild in niedriger Auflösung (z.B. 1080p)
2. PATCH TOKENIZATION: Frame wird in 16x16 Pixel-Patches zerlegt und in Tokens konvertiert
3. SELF-ATTENTION: Transformer analysiert globale Pixel-Beziehungen und Kontexte
4. UPSCALING: KI-generiert High-Res Frame mit schärferen Details
5. OUTPUT: Spiel erhält Upscaled Frame nahe nativer Qualität bei 4x-8x höherer FPS

VISION TRANSFORMER ADVANTAGES:
• Reduziert Megapixel-Parity (MP) Image von High-Res Training
• Skaliert besser mit mehr Training-Daten
• Bessere Generalisierung für verschiedene Spiel-Styles

DP4a Precision für RTX 30/40, FP8 für RTX 50 Blackwell-Architektur!"""

        how_label = tk.Label(how_frame, text=how_desc.strip(), font=("Arial", 11),
                           fg=self.colors['text'], bg=self.colors['bg_card'],
                           justify=tk.LEFT, wraplength=1200)
        how_label.pack(fill=tk.X, pady=15, padx=15)

        # Performance Examples
        perf_examples_frame = tk.LabelFrame(tab, text="REAL-WORLD PERFORMANCE BEISPIELE RTX 5060",
                                          font=("Arial", 16, "bold"), fg=self.colors['success'],
                                          bg=self.colors['bg_dark'], relief=tk.GROOVE, bd=2)
        perf_examples_frame.pack(fill=tk.X, padx=30, pady=20)

        perf_inner = tk.Frame(perf_examples_frame, bg=self.colors['bg_card'], padx=20, pady=20)
        perf_inner.pack(fill=tk.X)

        examples = [
            ("Cyberpunk 2077 - 4K Path Tracing", "Native: ~60 FPS", "DLSS 4 + MFG: 470+ FPS", "7.8x Boost"),
            ("Alan Wake 2 - Hybrid Ray Tracing", "Native: ~90 FPS", "DLSS 4 Quality: 240+ FPS", "2.7x Boost"),
            ("Baldur's Gate 3 - Ultra Settings", "Native: ~95 FPS", "DLSS 4 Balanced: 190+ FPS", "2.0x Boost"),
            ("Star Wars Outlaws - 4K Ultra", "Native: ~75 FPS", "DLSS 4 Performance: 180+ FPS", "2.4x Boost"),
            ("Indiana Jones - 4K RT Enabled", "Native: ~82 FPS", "DLSS 4 MFG: 260+ FPS", "3.2x Boost")
        ]

        for game, native, dlss, boost in examples:
            example_row = tk.Frame(perf_inner, bg=self.colors['bg_card'], pady=8, padx=10)
            example_row.pack(fill=tk.X)

            game_label = tk.Label(example_row, text=game,
                                font=("Arial", 11, "bold"), fg=self.colors['primary'],
                                bg=self.colors['bg_card'], width=35, anchor="w")
            game_label.pack(side=tk.LEFT)

            native_label = tk.Label(example_row, text=native,
                                  font=("Arial", 10), fg=self.colors['text_light'],
                                  bg=self.colors['bg_card'], width=15, anchor="center")
            native_label.pack(side=tk.LEFT, padx=(10, 0))

            dlss_label = tk.Label(example_row, text=dlss,
                                font=("Arial", 11, "bold"), fg=self.colors['accent'],
                                bg=self.colors['bg_card'], width=20, anchor="center")
            dlss_label.pack(side=tk.LEFT, padx=(10, 0))

            boost_label = tk.Label(example_row, text=boost,
                                 font=("Arial", 11, "bold"), fg=self.colors['success'],
                                 bg=self.colors['bg_card'], width=12, anchor="center")
            boost_label.pack(side=tk.LEFT, padx=(10, 0))

    def build_performance_calculator_tab(self, tab):
        """FPS Performance Calculator"""

        tab.configure(bg=self.colors['bg_dark'])

        # Header
        calc_header = tk.Label(tab, text="🎯 RTX 5060 FPS PERFORMANCE CALCULATOR",
                             font=("Arial", 24, "bold"), fg=self.colors['accent'], bg=self.colors['bg_dark'])
        calc_header.pack(pady=30)

        calc_sub = tk.Label(tab, text="Berechne deine Gaming-Performance mit DLSS 4 Technologie",
                          font=("Arial", 14), fg=self.colors['text_light'], bg=self.colors['bg_dark'])
        calc_sub.pack(pady=(0, 40))

        # Calculator Frame
        calc_frame = tk.Frame(tab, bg=self.colors['bg_card'], relief=tk.RIDGE, bd=2, padx=40, pady=30)
        calc_frame.pack(fill=tk.X, padx=40, pady=20)

        # Resolution Selection
        res_frame = tk.Frame(calc_frame, bg=self.colors['bg_card'])
        res_frame.pack(pady=(0, 30))

        res_label = tk.Label(res_frame, text="SPIELAUFLÖSUNG:",
                           font=("Arial", 14, "bold"), fg=self.colors['text'],
                           bg=self.colors['bg_card'])
        res_label.pack(anchor='w', pady=(0, 15))

        self.resolution_var = tk.StringVar(value="1080p")
        resolutions = [("1080p", "1920x1080"), ("1440p", "2560x1440"), ("4K", "3840x2160"), ("8K", "7680x4320")]

        for res_name, res_desc in resolutions:
            res_radio = tk.Radiobutton(res_frame, text=f"{res_name} ({res_desc})",
                                     variable=self.resolution_var, value=res_name,
                                     font=("Arial", 11), fg=self.colors['text'],
                                     bg=self.colors['bg_card'], selectcolor=self.colors['primary'])
            res_radio.pack(anchor='w', pady=5)

        # DLSS Quality Selection
        dlss_frame = tk.Frame(calc_frame, bg=self.colors['bg_card'])
        dlss_frame.pack(pady=(0, 30))

        dlss_label = tk.Label(dlss_frame, text="DLSS 4 QUALITÄT:",
                            font=("Arial", 14, "bold"), fg=self.colors['text'],
                            bg=self.colors['bg_card'])
        dlss_label.pack(anchor='w', pady=(0, 15))

        self.dlss_var = tk.StringVar(value="Quality")
        dlss_options = [
            ("Performance", "Maximale FPS-Steigerung"),
            ("Balanced", "Ausgewogene Qualität/FPS"),
            ("Quality", "Höhere Bildqualität"),
            ("Ultra Quality", "Maximale Qualität + MFG")
        ]

        for dlss_name, dlss_desc in dlss_options:
            dlss_radio = tk.Radiobutton(dlss_frame, text=f"{dlss_name} ({dlss_desc})",
                                      variable=self.dlss_var, value=dlss_name,
                                      font=("Arial", 11), fg=self.colors['text'],
                                      bg=self.colors['bg_card'], selectcolor=self.colors['primary'])
            dlss_radio.pack(anchor='w', pady=5)

        # Game Selection (popular titles)
        game_frame = tk.Frame(calc_frame, bg=self.colors['bg_card'])
        game_frame.pack(pady=(0, 30))

        game_label = tk.Label(game_frame, text="SPIEL AUSWÄHLEN:",
                            font=("Arial", 14, "bold"), fg=self.colors['text'],
                            bg=self.colors['bg_card'])
        game_label.pack(anchor='w', pady=(0, 15))

        self.game_var = tk.StringVar(value="Cyberpunk 2077")
        games = [
            ("Cyberpunk 2077", "Path Tracing Ready"),
            ("Alan Wake 2", "Remedy Entertainment"),
            ("Baldur's Gate 3", "Larian Studios"),
            ("Star Wars Outlaws", "Ubisoft Massive"),
            ("Indiana Jones", "MachineGames")
        ]

        game_combo = ttk.Combobox(game_frame, textvariable=self.game_var, values=[g[0] for g in games], state="readonly")
        game_combo.pack(pady=(0, 10))

        # Calculate Button
        calc_btn = tk.Button(calc_frame, text="🚀 FPS BERECHNEN", command=self.calculate_performance,
                           font=("Arial", 16, "bold"), bg=self.colors['success'], fg="black",
                           padx=30, pady=15, relief=tk.RAISED, bd=3)
        calc_btn.pack(pady=(20, 0))

        # Results Frame
        self.results_frame = tk.Frame(calc_frame, bg=self.colors['bg_highlight'],
                                    relief=tk.GROOVE, bd=2, padx=20, pady=20)
        self.results_frame.pack(fill=tk.X, pady=(30, 0))

        self.results_label = tk.Label(self.results_frame, text="Wähle Einstellungen und klicke 'Berechnen' für Ergebnisse",
                                    font=("Arial", 14, "bold"), fg=self.colors['text_light'],
                                    bg=self.colors['bg_highlight'])
        self.results_label.pack()

    def calculate_performance(self):
        """Berechne Gaming Performance basierend auf Auswahl"""

        resolution = self.resolution_var.get()
        dlss_quality = self.dlss_var.get()
        game = self.game_var.get()

        # Base performance values for RTX 5060
        base_fps = {
            "1080p": {
                "Cyberpunk 2077": 95,
                "Alan Wake 2": 110,
                "Baldur's Gate 3": 85,
                "Star Wars Outlaws": 92,
                "Indiana Jones": 105
            },
            "1440p": {
                "Cyberpunk 2077": 65,
                "Alan Wake 2": 78,
                "Baldur's Gate 3": 58,
                "Star Wars Outlaws": 62,
                "Indiana Jones": 71
            },
            "4K": {
                "Cyberpunk 2077": 42,
                "Alan Wake 2": 51,
                "Baldur's Gate 3": 38,
                "Star Wars Outlaws": 41,
                "Indiana Jones": 46
            }
        }

        # DLSS multipliers
        dlss_multipliers = {
            "Performance": 2.8,
            "Balanced": 2.4,
            "Quality": 2.0,
            "Ultra Quality": 1.6  # Mit MFG effektiver
        }

        native_fps = base_fps.get(resolution, {}).get(game, 60)
        multiplier = dlss_multipliers.get(dlss_quality, 2.0)

        # Calculate boosted FPS
        boosted_fps = int(native_fps * multiplier)

        # Special handling for 4K with MFG
        if resolution == "4K" and dlss_quality == "Ultra Quality":
            boosted_fps = int(native_fps * 4.5)  # Multi Frame Generation boost

        # Results
        results_text = f"""
🎮 RTX 5060 PERFORMANCE ERGEBNIS

Spiel: {game}
Auflösung: {resolution}
DLSS Quality: {dlss_quality}

📊 PERFORMANCE:
• Native FPS: {native_fps}
• Mit DLSS 4: {boosted_fps} FPS
• Steigerung: {multiplier:.1f}x ({int((multiplier-1)*100)}% mehr)

🎯 EMPFEHLUNGEN:
• Bei {boosted_fps}+ FPS: Vollgenuss-Gaming
• RTX 5060 Blackwell: Perfekt für {resolution} Gaming
• DLSS 4: Zukunftssicher bis 2030+
• Temperaturen: GPU max 72°C, CPU max 75°C

💡 TIPP: Verwende 'Balanced' für beste Balance zwischen Performance & Qualität!"""

        # Update results display
        self.results_label.config(text=results_text.strip(), fg=self.colors['text'])

        # Show popup with details
        messagebox.showinfo(f"🎮 {game} - {resolution} Performance",
                          f"Native: ~{native_fps} FPS\nDLSS 4 ({dlss_quality}): {boosted_fps} FPS\n\n"
                          f"{multiplier:.1f}x Steigerung durch KI-Upscaling!\n\n"
                          "RTX 5060 Blackwell ist bereit für Next-Gen Gaming!")

    def build_support_tab(self, tab):
        """Support und Kompatibilität"""

        tab.configure(bg=self.colors['bg_dark'])

        # Header
        support_header = tk.Label(tab, text="🛠️ SUPPORT & TECHNISCHE INFORMATIONEN",
                                font=("Arial", 24, "bold"), fg=self.colors['warning'], bg=self.colors['bg_dark'])
        support_header.pack(pady=30)

        sub_header = tk.Label(tab, text="Warranty, Compatibility & Technical Support",
                            font=("Arial", 14), fg=self.colors['text_light'], bg=self.colors['bg_dark'])
        sub_header.pack(pady=(0, 40))

        # Warranty Section
        warranty_frame = tk.LabelFrame(tab, text="GARANTIE INFORMATIONEN",
                                     font=("Arial", 16, "bold"), fg=self.colors['success'],
                                     bg=self.colors['bg_dark'], relief=tk.GROOVE, bd=2)
        warranty_frame.pack(fill=tk.X, padx=30, pady=20)

        warranty_inner = tk.Frame(warranty_frame, bg=self.colors['bg_card'], padx=20, pady=20)
        warranty_inner.pack(fill=tk.X)

        warranty_text = f"""
🛡️ HERSTELLERGARANTIE: {self.product_data['warranty']}

• Hardware-Defekte innerhalb 24 Monate kostenlos repariert
• Geprüfte Rückgabe: Zertifizierte, neuwertige Hardware
• Erweiterte Garantie: +12 Monate gegen Aufpreis verfügbar
• Technischer Support: Kostenlos per Telefon & E-Mail
• RMA-Prozess: Schnelle Bearbeitung & Ersatzteilversorgung

📞 SUPPORT-KONTAKTE:
• Hotline: +49 (0) 123-456789 (Mo-Sa 09:00-18:00)
• E-Mail: support@joule-performance.de
• Website: https://www.joule-performance.de/support
• Live-Chat: 24/7 für registrierte Kunden

🔧 TECHNISCHE SUPPORT LEISTUNGEN:
• Installation & Setup-Hilfe
• Treiber-Optimierungen
• Performance-Tuning
• Troubleshooting & Diagnose
• Software-Kompatibilität"""

        warranty_label = tk.Label(warranty_inner, text=warranty_text.strip(),
                                font=("Arial", 11), fg=self.colors['text'], bg=self.colors['bg_card'],
                                justify=tk.LEFT)
        warranty_label.pack(anchor='w')

        # Compatibility Section
        compat_frame = tk.LabelFrame(tab, text="SYSTEMVORAUSSETZUNGEN & KOMPATIBILITÄT",
                                   font=("Arial", 16, "bold"), fg=self.colors['primary'],
                                   bg=self.colors['bg_dark'], relief=tk.GROOVE, bd=2)
        compat_frame.pack(fill=tk.X, padx=30, pady=20)

        compat_inner = tk.Frame(compat_frame, bg=self.colors['bg_card'], padx=20, pady=20)
        compat_inner.pack(fill=tk.X)

        compat_text = """
🎯 MINIMALE SYSTEMVORAUSSETZUNGEN:

• Stromversorgung: 220-240V AC, 16A Sicherung empfohlen
• Internet: Für initiale Aktivierung & Treiber-Updates
• Betriebstemperatur: 5°C - 35°C Raumtemperatur
• Relative Luftfeuchtigkeit: 10% - 80%

💻 SOFTWARE-KOMPATIBILITÄT:

• Betriebssysteme: Windows 11 64-bit (vorinstalliert), Windows 10 kompatibel
• DirectX: Version 12 Ultimate mit Mesh Shading Support
• OpenGL: Version 4.6 mit erweiterten Shader-Modellen
• Vulkan: Version 1.3 mit RTX-Extensions
• PCIe: Generation 5.0 für maximale Bandbreite
• USB: 3.2 Gen2 mit 20 Gbps Transferrate

🎮 GAMING-SOFTWARE INTEGRATION:

• NVIDIA GeForce Experience für Optimierungen
• NVIDIA Ansel für Screenshots & Sharing
• NVIDIA Broadcast für KI-gestützte Webcam
• MSI Afterburner für Monitoring & Overclocking
• RTSS für Framerate-Lim
