#!/usr/bin/env python3
"""
Joule Performance High End Gaming PC Manager
Professionelle Desktop-Anwendung für Gaming PC Produktverwaltung
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import webbrowser
import platform

class JoulePerformancePCApp:
    """Professionelle Gaming PC Produkt-Manager App"""

    def __init__(self, root):
        self.root = root
        self.root.title("Joule Performance PC Manager v3.0 - RTX 5060 Edition")
        self.root.geometry("1200x900")
        self.root.configure(bg='#0a0a1a')  # Dark gaming theme
        self.root.minsize(1000, 700)

        # GPU/Product data with corrected RTX 5060 specs
        self.product_data = {
            "product_id": "L1138103",
            "name": "Joule Performance High End Gaming PC",
            "full_name": "Joule Performance High End Gaming PC RTX5060 i9 64GB 2TB",
            "brand": "Joule Performance",
            "category": "Gaming PC",
            "model": "High End Gaming Edition",
            "gpu_series": "RTX 5060",
            "original_price": 3399.00,
            "discount_price": 2318.80,
            "discount_percent": 17,
            "discount_amount": 1080.20,
            "currency": "EUR",
            "warranty": "24 Monate Garantie + Geprüfte Rückgabe (zertifizierter Rücklauf)",
            "availability": "Auf Lager - Sofort verfügbar",
            "delivery_time": "1-2 Werktage",
            "rating": 4.8,
            "review_count": 47,
            "benchmark_score": 98,
            "performance_rating": "★★★★★★☆☆☆☆ (9.8/10)",
            "specs": {
                "prozessor": "Intel® Core™ i9-14900KF (24 Kerne, 32 Threads)",
                "taktfrequenz": "bis zu 5.8 GHz Turbo Boost Max",
                "grafikkarte": "NVIDIA® GeForce RTX™ 5060 12GB GDDR6",
                "arbeitsspeicher": "64 GB DDR5 6000 MHz Dual-Channel (2x 32 GB)",
                "hauptplatine": "Z790 Gaming Mainboard (ATX Formfaktor)",
                "speichersystem": "2 TB NVMe PCIe 4.0 SSD (Gen4)",
                "netzteil": "850W 80PLUS Gold zertifiziert (Modular)",
                "gehaeuse": "Gaming Midi Tower - schwarz (RGB Lighting)",
                "kuehlung": "240 mm AIO Wasserkühlung + Lüfter",
                "betriebssystem": "Windows 11 Pro (vorinstalliert)",
                "netzwerk": "WiFi 6E + Bluetooth 5.3 + 2.5G LAN",
                "anschluesse": "HDMI 2.1, DP 1.4a, USB3.2 Gen2, RGB",
                "gewicht": "12.5 kg (komplett aufgebaut)"
            },
            "gpu_features": [
                "12 GB GDDR6 VRAM (192-bit)",
                "Ray Tracing Core Next Gen",
                "DLSS 3.0 & Frame Generation",
                "Shader Model 6.8",
                "NVIDIA Broadcast App support",
                "4K Gaming Ready",
                "VR Ready (Quest 2/3 optimiert)",
                "CUDA Cores: 3584",
                "Boost Clock: 2420 MHz",
                "Tensor Cores: 112 (4. Gen)",
                "RT Cores: 56 (3. Gen)"
            ],
            "performance": {
                "gaming_1080p": "240+ FPS (Ultra Settings)",
                "gaming_1440p": "144+ FPS (Ultra Settings)",
                "gaming_4k": "60+ FPS (High Settings)",
                "rt_1080p": "200+ FPS mit RT (Medium)",
                "rt_1440p": "120+ FPS mit RT (Medium)",
                "benchmark_cpu": "45,000+ Punkte (Cinebench R23 Multi)",
                "benchmark_gpu": "24,000+ Punkte (3DMark Time Spy)",
                "memory_bandwidth": "720 GB/s",
                "power_consumption": "650W Spitze (Gaming)",
                "idle_power": "85W (Desktop)",
                "temperature_cpu": "Max 75°C (Gaming)",
                "temperature_gpu": "Max 72°C (Gaming)",
                "noise_level": "32 dBA (Gaming), 25 dBA (Idle)"
            },
            "compatibility": [
                "Windows 11/10 (64-bit erforderlich)",
                "DirectX 12 Ultimate",
                "OpenGL 4.6",
                "Vulkan 1.3",
                "NVIDIA GeForce Experience",
                "MSI Afterburner Compatible",
                "VR-Headset Ready",
                "Streaming Software optimiert"
            ],
            "included_software": [
                "Windows 11 Pro License",
                "NVIDIA GeForce Experience",
                "Steam Gaming Platform",
                "Razer Synapse (RGB Control)",
                "Corsair iCUE (Kühlung)",
                "Benchmark Software Suite",
                "Gaming Optimierungs-Tools"
            ],
            "system_requirements": {
                "minimum": "220V Netzanschluss, Internet für Aktivierung",
                "recommended": "220V-240V, UPS empfohlen",
                "operating_temp": "5°C - 35°C Raumtemperatur",
                "humidity": "10% - 80% relative Luftfeuchtigkeit"
            },
            "support": {
                "warranty": "24 Monate Herstellergarantie + Geprüfte Rückgabe",
                "support_hotline": "+49 (0) 123-456789",
                "support_email": "support@joule-performance.de",
                "support_website": "https://www.joule-performance.de/support",
                "customer_service": "Mo-Sa 09:00-18:00 Uhr"
            },
            "shipping": {
                "method": "Versicherter Paketversand (DHL/GLS)",
                "packaging": "Spezielle Gaming PC Verpackung",
                "insurance": "Bis zu €10.000 Transportversicherung",
                "tracking": "Live-Tracking verfügbar"
            }
        }

        self.setup_styles()
        self.create_main_interface()
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)

        print("Joule Performance PC Manager gestartet!")
        print(f"RTX {self.product_data['gpu_series']} Gaming PC loaded")
        print(f" Preis: {self.product_data['discount_price']} € (-{self.product_data['discount_percent']}%)")

    def setup_styles(self):
        """Erstellt professionelle GUI-Styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Gaming-ähnliche Farbpalette
        self.colors = {
            'bg_dark': '#0a0a1a',
            'bg_darker': '#050510',
            'bg_card': '#1a1a2e',
            'bg_highlight': '#1f1f3f',
            'primary': '#00d4ff',     # Electric Blue (Gaming Tech)
            'secondary': '#ff6b9d',   # Neon Pink
            'accent': '#7bff8d',      # Electric Green
            'warning': '#ffa500',    # Orange
            'danger': '#ff4757',     # Red
            'text': '#ffffff',
            'text_light': '#b0b0cc',
            'text_dark': '#8080aa',
            'border': '#404060',
            'success': '#32cd32'
        }

        # Custom styles für Buttons
        self.style.configure(
            'Gaming.TButton',
            font=('Arial', 11, 'bold'),
            background=self.colors['primary'],
            foreground='black',
            relief='raised',
            borderwidth=2
        )

        self.style.configure(
            'Success.TButton',
            font=('Arial', 10, 'bold'),
            background=self.colors['success']
        )

        self.style.configure(
            'Warning.TButton',
            font=('Arial', 10, 'bold'),
            background=self.colors['warning']
        )

    def create_main_interface(self):
        """Erstellt die Haupt-GUI"""
        # Haupt-Container mit Scrollbar
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Canvas für Scrolling
        self.canvas = tk.Canvas(main_container, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg_dark'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Erstelle alle Sektionen
        self.create_header()
        self.create_price_panel()
        self.create_gpu_highlight()
        self.create_specs_grid()
        self.create_performance_dashboard()
        self.create_features_panel()
        self.create_compatibility_panel()
        self.create_support_panel()
        self.create_action_buttons()
        self.create_footer()

    def _on_mousewheel(self, event):
        """Smooth scrolling mit Maus"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_header(self):
        """Erstellt prominenten Gaming-PC Header"""
        header_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_dark'], height=150)
        header_frame.pack(fill=tk.X, padx=30, pady=(20, 10))
        header_frame.pack_propagate(False)

        # Logo und Branding
        logo_frame = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        logo_frame.pack(anchor='w')

        # Gaming Icon
        icon_label = tk.Label(
            logo_frame,
            text="🎮",
            font=("Arial", 48),
            fg=self.colors['primary'],
            bg=self.colors['bg_dark']
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 20))

        # Main Title
        title_text = tk.Label(
            logo_frame,
            text="JOULE PERFORMANCE",
            font=("Arial", 32, "bold"),
            fg=self.colors['primary'],
            bg=self.colors['bg_dark']
        )
        title_text.pack(side=tk.LEFT)

        # Subtitle
        subtitle = tk.Label(
            logo_frame,
            text="HIGH END GAMING PC",
            font=("Arial", 16, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        )
        subtitle.pack(side=tk.LEFT, padx=(20, 0))

        # RTX 5060 Highlight
        rtx_frame = tk.Frame(header_frame, bg=self.colors['bg_card'], relief=tk.RIDGE, bd=3)
        rtx_frame.pack(anchor='w', pady=(20, 0))

        rtx_label = tk.Label(
            rtx_frame,
            text=".2f"            font=("Arial", 20, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_card'],
            padx=20,
            pady=10
        )
        rtx_label.pack()

        # Product ID und Rating
        info_frame = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        info_frame.pack(anchor='w', pady=(15, 0))

        # Rating Stars
        rating_text = "★★★★★"[:int(self.product_data['rating'])] + "☆" * (5 - int(self.product_data['rating']))
        rating_label = tk.Label(
            info_frame,
            text=f"{rating_text} {self.product_data['rating']}/5 ({self.product_data['review_count']} Reviews)",
            font=("Arial", 12),
            fg=self.colors['accent'],
            bg=self.colors['bg_dark']
        )
        rating_label.pack(side=tk.LEFT)

        # Product ID
        id_label = tk.Label(
            info_frame,
            text=f"• Modell: {self.product_data['product_id']} • Benchmark: {self.product_data['benchmark_score']}/100",
            font=("Arial", 12),
            fg=self.colors['text_light'],
            bg=self.colors['bg_dark']
        )
        id_label.pack(side=tk.LEFT, padx=(20, 0))

    def create_price_panel(self):
        """Erstellt detaillierten Preis-Panel"""
        price_panel = tk.Frame(self.scrollable_frame, bg=self.colors['bg_card'], relief=tk.GROOVE, bd=2)
        price_panel.pack(fill=tk.X, padx=30, pady=15)

        inner_frame = tk.Frame(price_panel, bg=self.colors['bg_card'], padx=30, pady=25)
        inner_frame.pack(fill=tk.X)

        # Discount Badge
        discount_frame = tk.Frame(inner_frame, bg=self.colors['danger'], relief=tk.RAISED, bd=2)
        discount_frame.pack(anchor='w', pady=(0, 20))

        discount_label = tk.Label(
            discount_frame,
            text=f"🔥 EXKLUSIVER {self.product_data['discount_percent']}% RABATT 🔥",
            font=("Arial", 16, "bold"),
            fg='white',
            bg=self.colors['danger'],
            padx=20,
            pady=12
        )
        discount_label.pack()

        # Price Grid
        prices_frame = tk.Frame(inner_frame, bg=self.colors['bg_card'])
        prices_frame.pack(fill=tk.X)

        # Original Price (Durchgestrichen)
        orig_price_label = tk.Label(
            prices_frame,
            text=f"Originalpreis: {self.product_data['original_price']:,.2f} €".replace(",", "."),
            font=("Arial", 18, "overstrike"),
            fg=self.colors['text_light'],
            bg=self.colors['bg_card']
        )
        orig_price_label.pack(anchor='w', pady=(0, 10))

        # Discount Amount
        savings_label = tk.Label(
            prices_frame,
            text=f"Sie sparen: {self.product_data['discount_amount']:,.2f} €".replace(",", "."),
            font=("Arial", 14, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_card']
        )
        savings_label.pack(anchor='w', pady=(0, 20))

        # Current Price (Prominent)
        price_grid = tk.Frame(prices_frame, bg=self.colors['bg_card'])
        price_grid.pack(fill=tk.X)

        # "Ihr Preis" Label
        current_label = tk.Label(
            price_grid,
            text="Ihr Preis:",
            font=("Arial", 24, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_card']
        )
        current_label.pack(side=tk.LEFT, padx=(0, 30))

        # Price Amount (Huge)
        price_amount = tk.Label(
            price_grid,
            text="2318,80 €".replace(",", "."),
            font=("Arial", 48, "bold"),
            fg=self.colors['success'],
            bg=self.colors['bg_card']
        )
        price_amount.pack(side=tk.LEFT)

        # VAT Note
        vat_label = tk.Label(
            prices_frame,
            text="*Alle Preise inkl. MwSt. | Versandkostenfrei",
            font=("Arial", 11),
            fg=self.colors['text_light'],
            bg=self.colors['bg_card']
        )
        vat_label.pack(anchor='w', pady=(20, 0))

        # Availability & Shipping
        avail_frame = tk.Frame(inner_frame, bg=self.colors['success'], relief=tk.FLAT, bd=1)
        avail_frame.pack(fill=tk.X, pady=(20, 0))

        avail_label = tk.Label(
            avail_frame,
            text=f"📦 {self.product_data['availability']} | 🚚 {self.product_data['delivery_time']}",
            font=("Arial", 12, "bold"),
            fg='white',
            bg=self.colors['success'],
            padx=15,
            pady=10
        )
        avail_label.pack()

    def create_gpu_highlight(self):
        """Erstellt RTX 5060 GPU Highlight Panel"""
        gpu_panel = tk.LabelFrame(
            self.scrollable_frame,
            text=" 🎮 NVIDIA GEFORCE RTX 5060 FLAGSHIP GPU ",
            font=("Arial", 18, "bold"),
            fg=self.colors['primary'],
            bg=self.colors['bg_dark'],
            relief=tk.GROOVE,
            bd=3
        )
        gpu_panel.pack(fill=tk.X, padx=30, pady=15)

        inner_frame = tk.Frame(gpu_panel, bg=self.colors['bg_card'], padx=25, pady=20)
        inner_frame.pack(fill=tk.X)

        # GPU Specs Header
        header_text = tk.Label(
            inner_frame,
            text="NVIDIA Ada Lovelace Architecture - Next-Gen Gaming Performance",
            font=("Arial", 14, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_card']
        )
        header_text.pack(anchor='w', pady=(0, 15))

        # Key GPU Features Grid
        features_frame = tk.Frame(inner_frame, bg=self.colors['bg_card'])
        features_frame.pack(fill=tk.X)

        gpu_features = [
            ("CUDA Cores", "3,584", "Parallel Processing Power"),
            ("RT Cores Gen 3", "56", "Hardware Ray Tracing"),
            ("Tensor Cores Gen 4", "112", "AI & DLSS Processing"),
            ("VRAM GDDR6", "12 GB", "Ultra-Fast Memory"),
            ("Memory Bus", "192-bit", "High Bandwidth"),
            ("Boost Clock", "2,420 MHz", "Peak Performance"),
            ("Power Efficiency", "TGP 220W", "Optimal Performance/Watt"),
            ("Thermal Design", "Max 85°C", "Advanced Cooling Ready")
        ]

        # GPU Features in 2 Spalten
        left_col = tk.Frame(features_frame, bg=self.colors['bg_card'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        right_col = tk.Frame(features_frame, bg=self.colors['bg_card'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Linke Spalte füllen
        for i, (feature, value, desc) in enumerate(gpu_features[:4]):
            self.create_gpu_spec_row(left_col, feature, value, desc)

        # Rechte Spalte füllen
        for i, (feature, value, desc) in enumerate(gpu_features[4:]):
            self.create_gpu_spec_row(right_col, feature, value, desc)

        # RT & AI Features
        tech_frame = tk.Frame(inner_frame, bg=self.colors['bg_highlight'], relief=tk.RIDGE, bd=1)
        tech_frame.pack(fill=tk.X, pady=(20, 0))

        tech_label = tk.Label(
            tech_frame,
            text="NEXT-GEN TECHNOLOGIEN: Ray Tracing • DLSS 3.0 • Frame Generation • NVIDIA Broadcast • AI Upscaling",
            font=("Arial", 11, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_highlight'],
            padx=15,
            pady=12
        )
        tech_label.pack()

    def create_gpu_spec_row(self, parent, feature, value, desc):
        """Erstellt GPU Spec-Zeile"""
        row_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        row_frame.pack(fill=tk.X, pady=8)

        # Feature Name
        feature_label = tk.Label(
            row_frame,
            text=f"{feature}:",
            font=("Arial", 11, "bold"),
            fg=self.colors['primary'],
            bg=self.colors['bg_card'],
            width=18,
            anchor="w"
        )
        feature_label.pack(side=tk.LEFT)

        # Value (Highlighted)
        value_label = tk.Label(
            row_frame,
            text=value,
            font=("Arial", 12, "bold"),
            fg=self.colors['success'],
            bg=self.colors['bg_card'],
            width=12,
            anchor="w"
        )
        value_label.pack(side=tk.LEFT, padx=(10, 0))

        # Description
        desc_label = tk.Label(
            row_frame,
            text=desc,
            font=("Arial", 10),
            fg=self.colors['text_light'],
            bg=self.colors['bg_card'],
            anchor="w"
        )
        desc_label.pack(side=tk.LEFT, padx=(15, 0))

    def create_specs_grid(self):
        """Erstellt detaillierte Specs-Übersicht"""
        specs_panel = tk.LabelFrame(
            self.scrollable_frame,
            text=" 🔧 KOMPLETTE TECHNISCHE SPEZIFIKATIONEN ",
            font=("Arial", 18, "bold"),
            fg=self.colors['secondary'],
            bg=self.colors['bg_dark'],
            relief=tk.GROOVE,
            bd=3
        )
        specs_panel.pack(fill=tk.X, padx=30, pady=15)

        grid_frame = tk.Frame(specs_panel, bg=self.colors['bg_card'], padx=20, pady=20)
        grid_frame.pack(fill=tk.X)

        # Specs in 2 Spalten mit Hervorhebungen
        left_specs = tk.Frame(grid_frame, bg=self.colors['bg_card'])
        left_specs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        right_specs = tk.Frame(grid_frame, bg=self.colors['bg_card'])
        right_specs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0))

        specs_left = list(self.product_data['specs'].items())[:len(self.product_data['specs'])//2]
        specs_right = list(self.product_data['specs'].items())[len(self.product_data['specs'])//2:]

        self.create_spec_column(left_specs, specs_left)
        self.create_spec_column(right_specs, specs_right)

    def create_spec_column(self, parent, specs_list):
        """Erstellt Specs-Spalte"""
        for spec_key, spec_value in specs_list:
            spec_frame = tk.Frame(parent, bg=self.colors['bg_card'], pady=6)
            spec_frame.pack(fill=tk.X)

            # Spec Label
            spec_label = tk.Label(
                spec_frame,
                text=spec_key.replace("_", " ").title() + ":",
                font=("Arial", 11, "bold"),
                fg=self.colors['text_light'],
                bg=self.colors['bg_card'],
                width=20,
                anchor="w"
            )
            spec_label.pack(side=tk.LEFT)

            # Spec Value
            value_label = tk.Label(
                spec_frame,
                text=spec_value,
                font=("Arial", 11),
                fg=self.colors['text'],
                bg=self.colors['bg_card'],
                anchor="w",
                wraplength=300
            )
            value_label.pack(side=tk.LEFT)

    def create_performance_dashboard(self):
        """Erstellt Performance Dashboard"""
        perf_panel = tk.LabelFrame(
            self.scrollable_frame,
            text=" 📊 LEISTUNGS-DASHBOARD RTX 5060 ",
            font=("Arial", 18, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_dark'],
            relief=tk.GROOVE,
            bd=3
        )
        perf_panel.pack(fill=tk.X, padx=30, pady=15)

        inner_frame = tk.Frame(perf_panel, bg=self.colors['bg_card'], padx=20, pady=20)
        inner_frame.pack(fill=tk.X)

        # Performance Header
        perf_header = tk.Label(
            inner_frame,
            text="Benchmark Results & Gaming Performance Optimierung",
            font=("Arial", 14, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_card']
        )
        perf_header.pack(anchor='w', pady=(0, 20))

        # Performance Metrics
        metrics = [
            ("🎮 1080p Gaming", self.product_data['performance']['gaming_1080p'], "Ultra Preset, Max Settings"),
            ("🖥️ 1440p Gaming", self.product_data['performance']['gaming_1440p'], "Ultra Preset, Max Settings"),
            ("📺 4K Gaming", self.product_data['performance']['gaming_4k'], "High Preset, Ray Tracing OFF"),
            ("🎯 CPU Benchmark", "45,000+ Punkte", "Cinebench R23 Multi-Core"),
            ("⚡ GPU Benchmark", "24,000+ Punkte", "3DMark Time Spy Graphics"),
            ("🔊 Geräuschlevel", "32 dBA Gaming / 25 dBA Idle", "Optimierte Lüfterkurven"),
            ("🌡️ Temperaturen", "CPU 75°C / GPU 72°C Max", "Unter Volllast Gaming"),
            ("⚡ Stromverbrauch", self.product_data['performance']['power_consumption'], "Gaming Load Peak")
        ]

        for i, (icon_title, value, desc) in enumerate(metrics):
            metric_row = tk.Frame(inner_frame, bg=self.colors['bg_card'], pady=8)
            metric_row.pack(fill=tk.X, padx=10)

            # Icon & Title
            icon_label = tk.Label(
                metric_row,
                text=icon_title,
                font=("Arial", 12, "bold"),
                fg=self.colors['primary'],
                bg=self.colors['bg_card'],
                width=20,
                anchor="w"
            )
            icon_label.pack(side=tk.LEFT)

            # Performance Value (Highlighted)
            value_label = tk.Label(
                metric_row,
                text=value,
                font=("Arial", 13, "bold"),
                fg=self.colors['success'],
                bg=self.colors['bg_card'],
                width=18,
                anchor="w"
            )
            value_label.pack(side=tk.LEFT, padx=(20, 0))

            # Description
            desc_label = tk.Label(
                metric_row,
                text=desc,
                font=("Arial", 10),
                fg=self.colors['text_light'],
                bg=self.colors['bg_card'],
                anchor="w"
            )
            desc_label.pack(side=tk.LEFT, padx=(20, 0))

    def create_features_panel(self):
        """Erstellt Features Panel"""
        features_panel = tk.LabelFrame(
            self.scrollable_frame,
            text=" ✨ EXKLUSIVE FEATURES & VORTEILE ",
            font=("Arial", 18, "bold"),
            fg=self.colors['warning'],
            bg=self.colors['bg_dark'],
            relief=tk.GROOVE,
            bd=3
        )
        features_panel.pack(fill=tk.X, padx=30, pady=15)

        inner_frame = tk.Frame(features_panel, bg=self.colors['bg_card'], padx=20, pady=20)
        inner_frame.pack(fill=tk.X)

        # Features in Grid-Layout
        features = [
            "High-End RTX 5060 Graphics Card",
            "Intel i9-14900KF Processor (24 Cores)",
            "64 GB DDR5 High-Speed RAM",
            "2 TB NVMe Gen4 SSD Storage",
            "Ray Tracing & DLSS 3.0 Support",
            "Professional Wasserkühlung AIO",
            "RGB Gaming Case Illumination",
            "Windows 11 Pro vorinstalliert",
            "WiFi 6E & Bluetooth 5.3",
            "VR-Ready für Quest 2/3",
            "Streaming OS optimisiert",
            "Benchmarking Tools Suite"
        ]

        # Features in 2 Spalten layout
        left_col = tk.Frame(inner_frame, bg=self.colors['bg_card'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        right_col = tk.Frame(inner_frame, bg=self.colors['bg_card'])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0))

        # Linke Spalte (Features 1-6)
        for i, feature in enumerate(features[:6]):
            feat_label = tk.Label(
                left_col,
                text=f"✓ {feature}",
                font=("Arial", 11),
                fg=self.colors['text'],
                bg=self.colors['bg_card'],
                anchor="w",
                pady=4
            )
            feat_label.pack(fill=tk.X)

        # Rechte Spalte (Features 7-12)
        for i, feature in enumerate(features[6:]):
            feat_label = tk.Label(
                right_col,
                text=f"✓ {feature}",
                font=("Arial", 11),
                fg=self.colors['text'],
                bg=self.colors['bg_card'],
                anchor="w",
                pady=4
            )
            feat_label.pack(fill=tk.X)

    def create_compatibility_panel(self):
        """Erstellt Kompatibilität & Requirements Panel"""
        compat_panel = tk.LabelFrame(
            self.scrollable_frame,
            text=" 🔌 SYSTEMANFORDERUNGEN & KOMPATIBILITÄT ",
            font=("Arial", 16, "bold"),
            fg=self.colors['text'],
            bg=self.colors['bg_dark'],
            relief=tk.GROOVE,
            bd=2
        )
        compat_panel.pack(fill=tk.X, padx=30, pady=15)

        inner_frame = tk.Frame(compat_panel, bg=self.colors['bg_card'], padx=20, pady=15)
        inner_frame.pack(fill=tk.X)

        compatibility_items = [
            ("Windows 11 Pro 64-bit", "vorinstalliert und aktiviert"),
            ("DirectX 12 Ultimate", "vollständig unterstützt"),
            ("OpenGL 4.6+", "optimierte Grafik-API"),
            ("Vulkan 1.3", "modernste GPU-API"),
            ("PCIe 4.0", "höchste Datenübertragung"),
            ("USB 3.2 Gen2", "schnellste USB-Konnektivität"),
            ("WiFi 6E", "6 GHz WLAN-Standard"),
            ("HDR10", "Premium Display Support")
        ]

        # Erstellen Grid für Compatibility
        for i, (tech, desc) in enumerate(compatibility_items):
            compat_row = tk.Frame(inner_frame, bg=self.colors['bg_card'])
            compat_row.pack(fill=tk.X, pady=5)

            tech_label = tk.Label(
                compat_row,
                text=f"{tech}:",
                font=("Arial", 11, "bold"),
                fg=self.colors['primary'],
                bg=self.colors['bg_card'],
                width=25,
                anchor="w"
            )
            tech_label.pack(side=tk.LEFT)

            desc_label = tk.Label(
                compat_row,
                text=desc,
                font=("Arial", 11),
                fg=self.colors['text'],
                bg=self.colors['bg_card'],
                anchor="w"
            )
            desc_label.pack(side=tk.LEFT, padx=(10, 0))

    def create_support_panel(self):
        """Erstellt Support & Garantie Panel"""
        support_panel = tk.LabelFrame(
            self.scrollable_frame,
            text=" 🛠️ GARANTIE & SUPPORT-SERVICE ",
            font=("Arial", 16, "bold"),
            fg=self.colors['success'],
            bg=self.colors['bg_dark'],
            relief=tk.GROOVE,
            bd=2
        )
        support_panel.pack(fill=tk.X, padx=30, pady=15)

        inner_frame = tk.Frame(support_panel, bg=self.colors['bg_card'], padx=20, pady=15)
        inner_frame.pack(fill=tk.X)

        # Warranty Info
        warranty_text = f"""
Garantie: {self.product_data['support']['warranty']}

Support-Hotline: {self.product_data['support']['support_hotline']}
Support-E-Mail: {self.product_data['support']['support_email']}
Web-Support: {self.product_data['support']['support_website']}

Kundenservice: {self.product_data['support']['customer_service']}
"""

        support_label = tk.Label(
            inner_frame,
            text=warranty_text.strip(),
            font=("Arial", 11),
            fg=self.colors['text'],
            bg=self.colors['bg_card'],
            justify=tk.LEFT
        )
        support_label.pack(anchor='w', pady=(0, 15))

        # Shipping Info
        shipping_info = f"""
Versand: {self.product_data['shipping']['method']}
Verpackung: {self.product_data['shipping']['packaging']}
Versicherung: {self.product_data['shipping']['insurance']}
Tracking: {self.product_data['shipping']['tracking']}
"""

        shipping_label = tk.Label(
            inner_frame,
            text=shipping_info.strip(),
            font=("Arial", 11, "bold"),
            fg=self.colors['accent'],
            bg=self.colors['bg_card'],
            justify=tk.LEFT
        )
        shipping_label.pack(anchor='w')

    def create_action_buttons(self):
        """Erstellt Action Buttons"""
        button_panel = tk.Frame(self.scrollable_frame, bg=self.colors['bg_dark'], padx=30, pady=20)
        button_panel.pack(fill=tk.X)

        # Button Grid (3x2 Layout)
        top_row = tk.Frame(button_panel, bg=self.colors['bg_dark'])
        top_row.pack(fill=tk.X, pady=(0, 10))

        bottom_row = tk.Frame(button_panel, bg=self.colors['bg_dark'])
        bottom_row.pack(fill=tk.X)

        buttons_data = [
            ("🛒 IN WARENKORB LEZEN", self.add_to_cart, self.colors['success'], "Direkt bestellen"),
            ("📊 PERFORMANCE TEST", self.run_performance_test, self.colors['primary'], "Benchmark ausführen"),
            ("📋 SPECS EXPORTIEREN", self.export_specs, self.colors['secondary'], "Technische Daten speichern"),
            ("🔍 VERGLEICHEN", self.compare_products, self.colors['accent'], "Mit anderen PCs vergleichen"),
            ("📞 SUPPORT KONTAKT", self.contact_support, self.colors['warning'], "Technischen Support erreichen"),
            ("❌ SCHLIESSEN", self.confirm_exit, self.colors['danger'], "Programm beenden")
        ]

        # Obere Reihe (3 Buttons)
        for i, (text, command, color, tooltip) in enumerate(buttons_data[:3]):
            btn = tk.Button(
                top_row,
                text=text,
                command=command,
                font=("Arial", 12, "bold"),
                bg=color,
                fg="white",
                relief=tk.RAISED,
                bd=3,
                padx=20,
                pady=15,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            self.create_tooltip(btn, tooltip)

        # Untere Reihe (3 Buttons)
        for i, (text, command, color, tooltip) in enumerate(buttons_data[3:]):
            btn = tk.Button(
                bottom_row,
                text=text,
                command=command,
                font=("Arial", 12, "bold"),
                bg=color,
                fg="white",
                relief=tk.RAISED,
                bd=3,
                padx=20,
                pady=15,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            self.create_tooltip(btn, tooltip)

    def create_footer(self):
        """Erstellt Footer mit System-Info"""
        footer_panel = tk.Frame(self.scrollable_frame, bg=self.colors['bg_darker'], height=80)
        footer_panel.pack(fill=tk.X, padx=30, pady=(20, 30))
        footer_panel.pack_propagate(False)

        # Footer Content
        footer_text = f"© 2024 Joule Performance PC GmbH • RTX 5060 High End Gaming PC • Alle Preise inkl. MwSt. • Versandkostenfrei\nSystem: {platform.system()} {platform.release()} • Python {platform.python_version()} • Letzte Aktualisierung: {datetime.now().strftime('%d.%m.%Y %H:%M')}"

        footer_label = tk.Label(
            footer_panel,
            text=footer_text,
            font=("Arial", 9),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_darker'],
            justify=tk.CENTER
        )
        footer_label.pack(expand=True)

    def create_tooltip(self, widget, text):
        """Erstellt Tooltips für Buttons"""
        def show_tooltip(event):
            self.tooltip = tk.Toplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")

            tooltip_label = tk.Label(
                self.tooltip,
                text=text,
                font=("Arial", 8),
                bg="#ffffcc",
                relief=tk.SOLID,
                borderwidth=1,
                padx=5,
                pady=3
            )
            tooltip_label.pack()

        def hide_tooltip(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    # Button Action Methods
    def add_to_cart(self):
        messagebox.showinfo(
            "Warenkorb hinzufügen",
            f"✅ Joule Performance RTX 5060 PC wurde Ihrem Warenkorb hinzugefügt!\n\nPreis: {self.product_data['discount_price']:,.2f} €".replace(",", ".") +
            f"\nSie sparen: {self.product_data['discount_amount']:,.2f} €".replace(",", ".") +
            "\n\nWeiter zur Kasse?"
        )

    def run_performance_test(self):
        perf_info = f"""🎯 RTX 5060 PERFORMANCE TEST RESULTS:

🎮 Gaming Benchmarks:
• 1080p Ultra: {self.product_data['performance']['gaming_1080p']}
• 1440p Ultra: {self.product_data['performance']['gaming_1440p']}
• 4K Gaming: {self.product_data['performance']['gaming_4k']}

⚡ Hardware Scores:
• CPU: {self.product_data['performance']['benchmark_cpu']} (Cinebench R23)
• GPU: {self.product_data['performance']['benchmark_gpu']} (3DMark Time Spy)

🌡️ System Status:
• Temperature: CPU {self.product_data['performance']['temperature_cpu']}, GPU {self.product_data['performance']['temperature_gpu']}
• Noise Level: {self.product_data['performance']['noise_level']}
• Power Consumption: {self.product_data['performance']['power_consumption']}

Rating: {self.product_data['performance_rating']}"""
        messagebox.showinfo("Performance Test", perf_info)

    def export_specs(self):
        try:
            filename = f"Joule_PC_Specs_{self.product_data['product_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.product_data, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Export erfolgreich", f"Spezifikationen wurden als '{filename}' exportiert!")
        except Exception as e:
            messagebox.showerror("Export Fehler", f"Spezifikationen konnten nicht exportiert werden: {str(e)}")

    def compare_products(self):
        messagebox.showinfo(
            "Produktvergleich",
            f"""🎯 RTX 5060 im Vergleich zu anderen GPUs:

 RTX 5060     | RTX 4060      | RTX 3060      | RTX 2060
--------------|---------------|---------------|-----------
3,584 CUDA    | 3,072 CUDA    | 3,584 CUDA    | 1,920 CUDA
12 GB GDDR6   | 8 GB GDDR6    | 12 GB GDDR6   | 6 GB GDDR6
220W TGP      | 128W TGP      | 170W TGP      | 160W TGP
DLSS 3.0      | DLSS 3.0      | DLSS 2.0      | DLSS 1.0
Ray Tracing   | Ray Tracing   | Ray Tracing   | Ray Tracing

💎 Ihr Gewinn mit RTX 5060: +20-40% Performance-Steigerung!"""
        )

    def contact_support(self):
        support_info = f"""🔧 TECHNISCHER SUPPORT

📞 Telefon: {self.product_data['support']['support_hotline']}
📧 E-Mail: {self.product_data['support']['support_email']}
🌐 Website: {self.product_data['support']['support_website']}

⏰ Service-Zeiten: {self.product_data['support']['customer_service']}

🎮 Spezialisierte Gaming-PC Support-Techniker
💻 Fernwartung und Hardware-Diagnose verfügbar
🔄 RMA-Service für Garantie-Fälle

Support für:
• RTX 5060 Installation und Optimierung
• Wasserkühlung und Lüftersteuerung
• Windows 11 Gaming Optimierung
• RGB-Beleuchtung Programmierung
• Benchmark-Einrichtung und Troubleshooting

Wählen Sie Ihre bevorzugte Kontaktmethode!"""
        messagebox.showinfo("Technischer Support", support_info)

    def confirm_exit(self):
        """Bestätigt Programmende"""
        if messagebox.askyesno("Programm beenden",
                              "Möchten Sie Joule Performance PC Manager wirklich beenden?\n\n" +
                              "Ungespeicherte Daten gehen verloren."):
            print(f"Joule Performance PC Manager beendet - {datetime.now().strftime('%H:%M:%S')}")
            self.root.destroy()

def main():
    """Startet die Joule Performance PC Manager App"""
    print("="*70)
    print("🎮 JOULE PERFORMANCE HIGH END GAMING PC MANAGER")
    print("RTX 5060 EDITION - PROFESSIONELLE SPEZIFIKATIONS-APP")
    print("="*70)
    print("")

    root = tk.Tk()
    app = JoulePerformancePCApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
