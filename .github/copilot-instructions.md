# QuantumAvatar – Copilot-Instructions

## Big Picture (2 Sub-Systeme)
- **Quantum Avatar V5 Demo-Stack**: `CORE_LOGIC.py` erzeugt Snapshots in `data/` → `BACKEND_API.py` (FastAPI) und `DASHBOARD.py` (Streamlit) lesen diese Daten.
- **CashMoneyColors Desktop-App**: `CashMoneyColors_App/main.py` ist eine Tkinter-App mit SQLite-DB (`data/nexus.db`), AI-Agent-Orchestrierung und optionalen Real-Integrationen (z. B. PayPal via `requests`).

## Datenfluss (Demo-Stack)
- `CORE_LOGIC.py`:
	- `QuantumLogic.autonomous_decision_engine()` berechnet Zufalls-KPIs und schreibt via `persist_results()` nach `data/quantum_results.json`.
	- `PayPalLogic.auto_transfer_logic(total_profit + total_revenue_increase)` erzeugt Events, `record_transfer()` hängt sie an `data/paypal_transfers.json` an.
- `BACKEND_API.py`:
	- liest Snapshots via `load_quantum_snapshot()` / `load_paypal_transfers()`; falls Dateien fehlen/defekt sind, gibt es **statische/in-memory** Fallbacks.
	- `system_metrics` ist der einzige globale Mutable-State (Overlay, wenn kein Snapshot da ist).
- `DASHBOARD.py` zeigt aktuell **statische** KPIs/Streams (kein echter API-Call). Wenn du Stream-Namen/Labels änderst, halte API und Dashboard konsistent.

## Entwickler-Workflows (Windows)
- Setup:
	- Demo: `python -m venv .venv` → `\.venv\Scripts\activate` → `pip install -r requirements.txt`
	- Desktop-App (breiter): `pip install -r CashMoneyColors_App/requirements.txt`
- Demo-Engine ausführen (produziert Snapshots): `python CORE_LOGIC.py`
- API starten: `uvicorn BACKEND_API:app --reload --port 8000` (Docs unter `/docs`)
- Dashboard starten: `streamlit run DASHBOARD.py`
- Desktop-App starten: `python CashMoneyColors_App/main.py`

## Konfiguration & Secrets (CashMoneyColors_App)
- Keys kommen aus Env-Vars in `CashMoneyColors_App/core/config.py`:
	- `GROK_API_KEY`, `DEEPSEEK_API_KEY`, `BLACKBOX_API_KEY`, `ANTHROPIC_API_KEY`
	- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
	- `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`
- Keine Secrets hardcoden; orientiere dich an `.env.example` / `CashMoneyColors_App/core/config.py:create_config_structure()`.

## Repo-spezifische Patterns
- **Async-first** bei QuantumAvatar-Skripten: `asyncio.gather(...)` + kurze Sleeps, Console-Logs oft in GROSSBUCHSTABEN/Emoji-Stil.
- **Tolerante Bootstraps** in der Desktop-App: `safe_execute()` aus `CashMoneyColors_App/utils/helpers.py` statt harte Abbrueche.
- **Optionale Dependencies**: `CashMoneyColors_App/core/chatbot.py` faellt bei fehlendem `openai`/`anthropic` auf Mocks zurueck (ImportError-Handling).
- **Persistenz-Orte**: Demo-Snapshots unter `data/`; Desktop-App-DB/Artefakte ebenfalls unter `data/`/`logs/`. Wenn du Schema/Pfade aenderst, aktualisiere alle Leser.

## Tests / Smoke-Checks
- Unit-Tests (stdlib): `python -m unittest tests/test_core_logic.py`
- Optional (wenn installiert): `python -m pytest tests/test_core_logic.py -v`