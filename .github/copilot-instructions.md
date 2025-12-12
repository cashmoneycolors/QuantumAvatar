# Quantum Avatar - Copilot Leitfaden

## Architektur-Ueberblick
- `quantum_avatar_activation.py` meldet KI-, Design- und Payment-Services parallel per `asyncio.gather()` an und setzt damit den erzählerischen Systemstatus.
- `CORE_LOGIC.py` enthaelt `QuantumLogic` (Marktanalyse, Self-Learning, Revenue-Optimierung) sowie `PayPalLogic`; `main()` schreibt jede Ausfuehrung via `persist_results()` nach `data/quantum_results.json` und ueber `record_transfer()` nach `data/paypal_transfers.json`.
- `BACKEND_API.py` (FastAPI) liest diese Snapshots in allen `/api/v1/*`-Routen, um Umsatz, Stream-Mix, Systemstatus und PayPal-Historie auszugeben; statische Fallbacks laufen weiter, falls Dateien fehlen.
- `DASHBOARD.py` spiegelt die API in Streamlit (identische KPIs, Streams, Autonomie-Text). Achte darauf, Labels gleichzeitig in API und Dashboard zu pflegen.
- Story-Skripte wie `LIVE_DEPLOYMENT.py`, `PRODUCTION_START.py` oder `AUTONOMOUS_MONEY_MACHINE.py` nutzen stets: Klassencontainer, async Worker, Emoji-Logs, `if __name__ == "__main__"`.

## Daten- und Kontrollfluss
- Jede CLI-Session erzeugt neue Zufallsmetriken und ueberschreibt die JSON-Snapshots; ausserhalb von `data/` wird nichts persistiert.
- Wenn du das Schema von `persist_results()` anfasst, passe `load_quantum_snapshot()` und den Streamlit-Reader direkt mit an, damit alle Pfade weiter stimmen.
- `PayPalLogic.auto_transfer_logic()` verarbeitet `total_profit + total_revenue_increase`, fuegt erfolgreiche Transfers der Historie hinzu, und `/api/v1/paypal/status` liefert nur den juengsten Eintrag + Business-Mail.
- `system_metrics` in `BACKEND_API.py` ist der einzige globale Mutable State (uptime, customers); dient als Overlay, wenn kein Snapshot vorhanden ist.

## Entwickler-Workflows
- Umgebung: `python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt` (Python 3.8+). Die Requirements decken FastAPI, Streamlit, uvicorn, Auth- und Async-Abhaengigkeiten bereits ab.
- Kern-Engine: `python CORE_LOGIC.py` generiert frische KPIs und PayPal-Events und aktualisiert die JSON-Basis fuer API/Dashboard.
- API: `uvicorn BACKEND_API:app --reload --port 8000` liefert `/docs`, `/api/v1/revenue/today`, `/api/v1/system/status` usw.; laufe zuerst die Engine, sonst greifen nur Fallback-Daten.
- Dashboard: `streamlit run DASHBOARD.py` zeigt KPIs lokal; der Refresh-Button ist rein kosmetisch, deshalb Skript neu starten oder Engine erneut ausfuehren.
- Story-Runs (z. B. `python LIVE_DEPLOYMENT.py`) sind reine Demos und beschreiben nichts in die Snapshots, solange du sie nicht bewusst an `persist_results()` anschliesst.

## Patterns & Konventionen
- Async-first: selbst Demo-Skripte kombinieren Tasks via `asyncio.gather(...)` und bremsen mit kurzen `asyncio.sleep()`-Delays fuer lesbare Logs.
- Log-Stil: Grossbuchstaben + Emojis; halte neuen Output konsistent, damit Transkripte homogen wirken.
- Duplizierte Konstanten (`cashmoneycolors@gmail.com`, Autonomie-Level, KPI-Zahlen) unbedingt mit `rg`/`grep` quer durchs Repo aktualisieren.
- Abhaengigkeiten schlank halten; neue Libraries nur mitsamt Doku im README und fixer Version in `requirements.txt` aufnehmen.

## Erweiterungs-Hinweise
- API: Weitere Endpunkte direkt in `BACKEND_API.py`, immer unter `/api/v1/...`, bevorzugt mit Pydantic-Modellen und optionalem Snapshot-Zugriff.
- Dashboard: Verwende weiter die Streamlit-Spalten/Metriken aus `DASHBOARD.py`; teure Berechnungen ausserhalb des Render-Flows vorberechnen.
- Neue Story-Skripte strikt nach vorhandenem Template (Klasse + async Tasks + `run_*`-Coroutine), damit sie in die Marketing-Narrative passen.
- Falls echte Persistenz noetig wird, ersetze die JSON-Helfer in `CORE_LOGIC.py` und lies in API/Dashboard aus derselben Quelle, um Split-Brain zu vermeiden.